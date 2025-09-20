import os
from google.genai import types


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_files_info(working_directory, directory="."):
    try:
        full_path = os.path.join(working_directory, directory)
        absolute_path_working_directory = os.path.abspath(working_directory)
        absolute_full_path = os.path.abspath(full_path)
        if (
            absolute_full_path != absolute_path_working_directory
            and not absolute_full_path.startswith(absolute_path_working_directory)
        ):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(full_path):
            return f'Error: "{directory}" is not a directory'
    except Exception as e:
        return f"Error: {e}"

    dir_content = os.listdir(full_path)
    results = ""
    for d in dir_content:
        path = os.path.join(full_path, d)
        results += f"- {d}: file_size={os.path.getsize(path)} bytes, is_dir={os.path.isdir(path)} \n"
    return results
