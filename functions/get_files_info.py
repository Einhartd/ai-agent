import os

def get_files_info(working_directory, directory="."):
    try:

        ret_string = ""
        ret_string += "Result for "
        if directory == ".":
            ret_string += "current directory:\n"
        else:
            ret_string += f"'{directory}' directory:\n"
            
        target_directory = os.path.abspath(os.path.join(working_directory, directory))
        abs_working_directory = os.path.abspath(working_directory)

        if os.path.commonpath([target_directory, abs_working_directory]) != abs_working_directory:
            ret_string+=f'Error: Cannot list "{directory}" as it is outside the permitted working directory\n'
            return ret_string
        elif not os.path.exists(target_directory) or not os.path.isdir(target_directory):
            ret_string+=f'Error: "{directory}" is not a directory'
            return ret_string
        
        content = os.listdir(target_directory)
        for element in content:
            element_path = os.path.join(target_directory, element)
            size = os.path.getsize(element_path)
            is_dir = os.path.isdir(element_path)
            ret_string+= f"- {element}: file_size={size} bytes, is_dir={is_dir}\n"

        return ret_string
    
    except Exception as e:
        ret_string+=f"Error: {str(e)}"
        return ret_string

