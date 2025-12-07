import os


def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)

        abs_path_directory = os.path.abspath(full_path)
        if not abs_path_directory.startswith(os.path.abspath(working_directory)):
            return f"Error: Cannot list '{directory}' as it is outside the permitted working directory"
        if not os.path.isdir(full_path):
            return f"Error: '{directory}' is not a directory"
        
        lines = []
        for item in os.listdir(abs_path_directory):
            filepath = os.path.join(full_path, item)
            line = f"    - {item}: file_size={str(os.path.getsize(filepath))} bytes, is_dir={str(os.path.isdir(filepath))}"
            lines.append(line)
        joined_lines = '\n'.join(lines)

        
        if directory == ".":
            return f"Results for current directory:\n{joined_lines}"
        else:
            return f"Results for {directory} directory:\n{joined_lines}"
    except Exception as e:
        return f"Error: {e}"
    