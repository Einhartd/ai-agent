import os
from google.genai import types


def write_file(working_directory, file_path, content):
    
    try:
        ret_string = ""
        
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_directory = os.path.abspath(working_directory)
        
        # Check if path is within working directory
        if os.path.commonpath([abs_file_path, 
            abs_working_directory]) != abs_working_directory:
            
            ret_string+=f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
            
            
            return ret_string
        
        # Check if file exists
        if not os.path.exists(os.path.dirname(abs_file_path)):
            # Create file
            os.makedirs(os.path.dirname(abs_file_path), exist_ok=True)
            
        with open(abs_file_path, 'w') as file:
            file.write(content)
            ret_string += f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
                            
        return ret_string
    
    except Exception as e:
        ret_string+=f"Error: {str(e)}"
        return ret_string
    


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write or overwrite a file with specified content, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The Python file to execute, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content to write to the file.",
            ),
        },
    ),
)
