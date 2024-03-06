import os
import tempfile
import zipfile

from fastapi import APIRouter
from starlette.responses import StreamingResponse

from exceptions import not_found_exception
from utils import get_files

parse_router = APIRouter(prefix="", tags=["process the tar file for parsing"])

# Define the allowed file extension
ALLOWED_EXTENSIONS = {".tar.gz"}


def is_valid_file_extension(filename: str):
    return any(filename.endswith(ext) for ext in ALLOWED_EXTENSIONS)


@parse_router.get("/log-parsing/")
async def get_log_extraction_parsing():
    files_to_return = get_files()
    if not files_to_return:
        raise not_found_exception

    zip_filename = "parse_shutdown.zip"
    headers = {"Content-Disposition": f"attachment; filename={zip_filename}"}

    async def stream_zip():
        with tempfile.TemporaryDirectory() as temp_dir:
            zip_path = os.path.join(temp_dir, zip_filename)
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in files_to_return:
                    zipf.write(file_path, arcname=os.path.basename(file_path))

            with open(zip_path, "rb") as zip_file:
                while chunk := zip_file.read(8192):
                    yield chunk

    return StreamingResponse(stream_zip(), headers=headers, media_type="application/zip")
