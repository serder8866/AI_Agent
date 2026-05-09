import os
from google import genai
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)




def get_files_info(working_directory, directory="."):
    try:
        abs_working_dir = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
        valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        target_dir_list = os.listdir(target_dir)
        target_dir_content = []
        for item in target_dir_list:
            item_path = os.path.join(target_dir, item)
            item_is_file = os.path.isdir(item_path)
            target_dir_content.append(f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={item_is_file}")
        return "\n".join(target_dir_content)
    except Exception as e:
        return f"Error: {e}"
    