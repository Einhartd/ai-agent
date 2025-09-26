import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    
    try:
        ret_string = ""
        
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_directory = os.path.abspath(working_directory)
        
        if os.path.commonpath([abs_file_path, 
            abs_working_directory]) != abs_working_directory:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(abs_file_path):
            return f'Error: File "{file_path}" not found.'
        
        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file.'
        
        # run subprocess
        
        args = args or []
        
        completed = subprocess.run(
            args=["python3", abs_file_path] + args,
            timeout=30,
            capture_output=True,
            text=True,
            cwd=abs_working_directory,
            )
        
        stdout = completed.stdout or ""
        stderr = completed.stderr or ""
        
        if not stdout and not stderr:
            return "No output produced."
        
        ret_string += f"STDOUT:\n{stdout}STDERR:\n{stderr}"
        
        if completed.returncode != 0:
            ret_string += f"\nProcess exited with code {completed.returncode}"
            
        return ret_string
    
    except Exception as e:
        ret_string+=f"Error: executing Python file: {e}"
        return ret_string
    
    
schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Execute a Python file with optional arguments, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Optional list of string arguments to pass to the Python script.",
            ),
        },
    ),
)