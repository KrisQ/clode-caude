import os
from .config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Read file content in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path):
    try:
        full_path = os.path.join(working_directory, file_path)
        absolule_wd_path = os.path.abspath(working_directory)
        absolute_full_path = os.path.abspath(full_path)
        if absolute_full_path != absolule_wd_path and not absolute_full_path.startswith(
            absolule_wd_path
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(absolute_full_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        with open(full_path, "r") as file:
            file_content_string = file.read(MAX_CHARS)
            if len(file_content_string) >= MAX_CHARS:
                file_content_string += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return file_content_string
    except Exception as e:
        return f"Error: {e}"
