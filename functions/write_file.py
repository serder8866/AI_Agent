import os

def write_file(working_directory, file_path, content):
    abs_wd = os.path.abspath(working_directory)
    target_directory = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_directory.startswith(abs_wd):
        return f"Error: Cannot write to {file_path}, as it is outside the permitted working directory"
    try:
        if not os.path.exists(os.path.dirname(target_directory)):
            os.makedirs(os.path.dirname(target_directory))
            
    
        with open(target_directory, "w") as f:
            length = f.write(content)
            return f"Successfully wrote to '{file_path}' ({len(content)} characters written)"
    except Exception as e:
        return f"Error: {e}, targer_directory: {targer_directory}"