import os

def get_files_info(working_directory, directory="."):

    target_directory = os.path.abspath(os.path.join(working_directory, directory))
    abs_working_directory = os.path.abspath(working_directory)
    print(f"Target directory: {target_directory}")
    print(f"Working directory: {abs_working_directory}")

    if os.path.commonpath([target_directory, abs_working_directory]) != abs_working_directory:
        raise Exception(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    elif not os.path.exists(target_directory) or not os.path.isdir(target_directory):
        raise Exception(f'Error: "{directory}" is not a directory')
    
    content = os.listdir(target_directory)
    print(content)

    return



get_files_info(".", ".")