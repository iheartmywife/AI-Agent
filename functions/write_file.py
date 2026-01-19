import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes to a file in a specified file path relative to the working directory",
    parameters=types.Schema(
        required=["file_path", "content"],
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="content to be written to the specified file path"
            )
        },
    ),
)

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    in_working_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not in_working_dir:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        return f'Error: Cannot write to "{file_path}" as it is a directory'
    os.makedirs(working_dir_abs, exist_ok=True)
    print(f"Ensured {working_directory} exists")

    try:
        with open(target_file, "w") as f:
            f.write(content)
        with open(target_file, "r") as ff:
            if ff.read(len(content)) == content:
                return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f'Error: {e}'