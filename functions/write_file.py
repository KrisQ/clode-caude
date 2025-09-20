import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write in the specified file with specified content",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="What to write in the file",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content):
    try:
        full_path = os.path.join(working_directory, file_path)
        absolule_wd_path = os.path.abspath(working_directory)
        absolute_full_path = os.path.abspath(full_path)
        if absolute_full_path != absolule_wd_path and not absolute_full_path.startswith(
            absolule_wd_path
        ):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        with open(full_path, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"
