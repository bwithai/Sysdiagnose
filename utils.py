import os
import shutil
import tempfile
import zipfile
from pathlib import Path


def get_log_file():
    logfile_directory = "storage/parse_shutdown"

    # Get a list of all files in the specified directory
    files = os.listdir(logfile_directory)

    # Filter the list to include only files with a .log extension
    log_files = [file for file in files if file.endswith(".log")]

    if len(log_files) == 1:
        log_file = log_files[0]
        log_file = f"{logfile_directory}/{log_file}"
        return log_file
    else:
        return False


def remove_content_in_directory(dist_path):
    # Clear the contents of the existing directory
    for file_name in os.listdir(dist_path):
        file_path = os.path.join(dist_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Error clearing directory: {e}")
            raise


def maintain_dir_for_each_upload(dir_name):
    dist_path = os.path.join(os.getcwd(), dir_name)
    if not os.path.exists(dist_path):
        os.makedirs(dist_path)
    else:
        remove_content_in_directory(dist_path)
    return dist_path


def get_files():
    data_directory = 'storage/parse_shutdown'
    dist_path = os.path.join(os.getcwd(), data_directory)
    if not os.path.exists(dist_path):
        return False

    # List all files in the directory
    data_files = [os.path.join(data_directory, filename) for filename in os.listdir(data_directory) if
                  os.path.isfile(os.path.join(data_directory, filename))]

    return data_files


# Helper function to create a zip file containing multiple files
def create_zip_archive(files_to_return):
    zip_filename = "storage/parse_shutdown_zip"
    with tempfile.TemporaryDirectory() as temp_dir:
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in files_to_return:
                zipf.write(file_path, arcname=os.path.basename(file_path))

    print("zip file created successfully")
    return zip_filename
