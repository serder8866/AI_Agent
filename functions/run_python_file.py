import os
import subprocess
from google import genai
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python script specified by file_path relative to the working directory. It will return STDOUT and/or STDERR, or if there is neither it will simply inform that the process had no output",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to the python script that is to be run"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                default=None,
                description="Optional arguments that are passed to the python script if they are provided",
                items=types.Schema(
                    type=types.Type.STRING
                )
            )
        },
        required=["file_path"]
    )
)


def run_python_file(working_directory, file_path, args=None):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abs_working_dir, file_path))
        valid_target_file = os.path.commonpath([abs_working_dir, target_file]) == abs_working_dir
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        if args:
            command.extend(args)
        completed_process = subprocess.run(command, capture_output=True, timeout=30, text=True)
        
        return_code = completed_process.returncode
        stdout = completed_process.stdout
        stderr = completed_process.stderr
        feedback = ""
        if return_code != 0:
            feedback += f"Process exited with code {return_code}\n"
        if not stderr and not stdout:
            feedback += f"No output produced\n"
        elif stdout:
            feedback += f"STDOUT: {stdout}\n"
        elif stderr:
            feedback += f"STDERR: {stderr}"
        return feedback
        
    except Exception as e:
        return f"Error: {e}"