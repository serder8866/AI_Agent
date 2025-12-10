import os
import subprocess

def run_python_file(working_directory, file_path, args=[]):
    abs_wd = os.path.abspath(working_directory)
    target_path = os.path.join(working_directory, file_path)
    target_directory = os.path.abspath(target_path)
    
    if not target_directory.startswith(abs_wd):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_directory):
        return f'Error: File "{file_path}" not found.'
    if not target_directory[-3:] == ".py":
        return f'Error: "{file_path}" is not a Python file.'
    try:
        completed_process = subprocess.run(["python", f"{file_path}", *args], timeout=30, capture_output=True, cwd=os.path.dirname(target_directory))
        return_string = f"STDOUT: {completed_process.stdout}, STDERR: {completed_process.stderr}. The completed_process object has a stdout and stderr attribute."
        if completed_process.returncode != 0:
            return return_string + f" Process exited with code {completed_process.stderr}"
        elif completed_process.stdout == None:
            return "No output produced"
        if completed_process.returncode == 0:
            return return_string
    except Exception as e:
        return f"Error: executing Python file: {e}"