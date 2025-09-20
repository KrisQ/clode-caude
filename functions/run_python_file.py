import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run file along with passing arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The file path, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="arguments passed to the function call",
                items=types.Schema(type=types.Type.STRING),
            ),
        },
    ),
)


def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        absolule_wd_path = os.path.abspath(working_directory)
        absolute_full_path = os.path.abspath(full_path)
        if absolute_full_path != absolule_wd_path and not absolute_full_path.startswith(
            absolule_wd_path
        ):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(absolute_full_path):
            return f'Error: File "{file_path}" not found.'
        if not absolute_full_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file.'

        completed_process = subprocess.run(
            timeout=30.0,
            capture_output=True,
            cwd=working_directory,
            args=["uv", "run", absolute_full_path, *args],
        )

        if completed_process.stderr:
            return f"STDERR: {completed_process.stderr}"

        if completed_process.stdout:
            return f"STDOUT: {completed_process.stdout}"

        return "No output produced"
    except subprocess.CalledProcessError as e:
        return f"Process exited with code {e.returncode}"
    except Exception as e:
        return f"Error: executing Python file: {e}"
