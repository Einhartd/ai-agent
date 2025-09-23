import os


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


