import shutil

from fastapi import UploadFile, File, APIRouter, BackgroundTasks
from exceptions import file_extension_exception, file_not_uploaded_exception
from iShutdown_KasperskyLab.iShutdown_parse import parse_log_files
from utils import maintain_dir_for_each_upload

upload_file_router = APIRouter(prefix="", tags=["Upload File to Parse"])

# Define the allowed file extension
ALLOWED_EXTENSIONS = {".tar.gz"}


def is_valid_file_extension(filename: str):
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)


@upload_file_router.post("/upload_file/")
async def create_upload_file(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # Check if no file is provided
    if not file:
        raise file_not_uploaded_exception

    # Check if the file extension is valid
    if not is_valid_file_extension(file.filename):
        raise file_extension_exception

    dist_path = maintain_dir_for_each_upload(dir_name='storage')

    try:
        with open(f"{file.filename}", "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        new_file_src = f"{file.filename}"
        tar_file_path = f"{dist_path}/{new_file_src}"

        # analysts and users want to share their log files and parse them for different purposes.
        # Schedule the background task to process the tar file for parsing
        background_tasks.add_task(parse_log_files, tar_file_path)

        store_new_file_at_dist = f"{dist_path}"
        shutil.move(new_file_src, store_new_file_at_dist)

        # call iShutdown_detect.py
        # response = detect_sys_diagnose(tar_file_path)

        return {"message": "File Uploaded Successfully"}

    except Exception as e:
        # Handle any exceptions that might occur during file processing
        return {"message": f"Error processing file: {e}"}
