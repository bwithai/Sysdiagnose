import os
import shutil
import tempfile
import zipfile
from pathlib import Path


def get_target_file(dist_dir, extension):
    # Get a list of all files in the specified directory
    files = os.listdir(dist_dir)

    # Filter the list to include only files with a .log extension
    target_files = [file for file in files if file.endswith(extension)]

    if len(target_files) == 1:
        file_to_return = target_files[0]
        file_to_return = f"{dist_dir}/{file_to_return}"
        return file_to_return
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


def parse_shutdown():
    log_lines, txt_lines, csv_lines = "", "", ""
    parse_files = get_files()
    for file in parse_files:
        if file.endswith(".log"):
            log_lines = get_file_data(file)
        elif file.endswith('.txt'):
            txt_lines = get_file_data(file)
        elif file.endswith('.csv'):
            csv_lines = get_file_data(file)

    return log_lines, txt_lines, csv_lines


def convert_csv_to_html():
    log_file_path = "storage/parse_shutdown/parsed_shutdown.csv"  # Replace with the actual path to your log file

    try:
        csv_data = []
        with open(log_file_path, 'r') as log_file:
            count = 1
            for line in log_file:
                if line == "":
                    continue
                if count > 4:
                    csv_data.append(line)
                else:
                    print(line.strip())
                count += 1

        # Convert csv_data to HTML table
        html_table = "<table border='1'>\n"
        for csv_line in csv_data:
            html_table += "<tr>"
            for cell in csv_line.strip().split(','):
                html_table += f"<td>{cell}</td>"
            html_table += "</tr>\n"
        html_table += "</table>"

        return html_table

    except FileNotFoundError:
        print(f"The file {log_file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def get_file_data(file_path):
    lines = []
    try:
        with open(file_path, 'r') as log_file:
            for line in log_file:
                if line == "":
                    continue
                lines.append(line.strip())
                # print(line.strip())
        return lines
    except FileNotFoundError:
        print(f"The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


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
