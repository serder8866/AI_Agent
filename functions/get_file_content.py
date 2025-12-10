import os
from functions.config import MAX_CHAR
def get_file_content(working_directory, file_path):
    
    abs_wd = os.path.abspath(working_directory)
    target_path = os.path.join(working_directory, file_path)
    abs_file_path = os.path.abspath(target_path)
    
    if not abs_file_path.startswith(abs_wd):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(abs_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(abs_file_path) as f:
            file_content_string = f.read(MAX_CHAR)
            leftover = f.read(1)
            if leftover:
                return file_content_string + f"...File '{file_path}' truncated at {MAX_CHAR} characters"
            return file_content_string
    except Exception as e:
        return f"Error reading file: {e}"