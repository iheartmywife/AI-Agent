import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
    # Will be True or False
    in_working_dir = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
    if not in_working_dir:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: "{file_path}" does not exist or is not a regular file'
    if file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_file]
    if args != None:
        print(f'all args: {args}')
        command.extend(args)
    try:
        cp = subprocess.run(command, cwd=working_dir_abs, capture_output=True, text=True, timeout=30)
        output_string = ""
        if cp.returncode != 0:
            output_string += f"Process exited with code {cp.returncode}\n"
        if not cp.stdout and not cp.stderr:
            output_string += "No output produced\n"
        else:
            if cp.stdout:
                output_string += f"STDOUT: {cp.stdout}\n"
            if cp.stderr:
                output_string += f"STDERR: {cp.stderr}\n"
        return output_string
    except Exception as e:
        return f"Error: executing Python file: {e}"
            