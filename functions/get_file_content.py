import os
from functions.config import FILE_MAX_TRUNCATE_SIZE

def get_file_content(working_directory, file_path):
    
    try:
        ret_string = ""
            
        abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
        abs_working_directory = os.path.abspath(working_directory)

        if os.path.commonpath([abs_file_path, abs_working_directory]) != abs_working_directory:
            ret_string+=f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
            return ret_string
        elif not os.path.exists(abs_file_path):
            ret_string+=f'Error: File not found or is not a regular file: "{file_path}"'
            return ret_string
        
        
        with open(abs_file_path, 'r') as file:
            file_content = file.read(FILE_MAX_TRUNCATE_SIZE)
            ret_string += file_content
            if file.read(1) != "":
                ret_string += f'[...File "{file_path}"" truncated at 10000 characters]'    
    
        return ret_string    
        
    except Exception as e:
        ret_string+=f"Error: {str(e)}"
        return ret_string