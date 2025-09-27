import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from call_function import call_function

MODEL_NAME = "gemini-2.0-flash-001"
VALID_FLAGS = ['--verbose']

def parse_arguments():
    args = []
    flags = []
    for arg in sys.argv[1:]:
        if arg.startswith('--'):
            flags.append(arg)
        else:
            args.append(arg)
    
    # Validate flags
    for flag in flags:
        if flag not in ['--verbose']:
            raise Exception(f"Unknown flag: {flag}. Only --verbose is supported.")
    
    if not args:
        raise Exception("Please provide a prompt as a command line argument.")
    
    return ' '.join(args), '--verbose' in flags

def create_client():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    return genai.Client(api_key=api_key)

def get_system_prompt():
    return """
    You are a helpful AI coding agent.
    
    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    
    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files
    
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

def main():
    # parse arguments and get prompt
    prompt, verbose_flag = parse_arguments()
    # create the client
    client = create_client()
    # initial message list
    messages = [types.Content(role="user", parts=[types.Part(text=prompt)])]

    # available functions
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file,
    ])
    
    for i in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], 
                    system_instruction=get_system_prompt()
                ),
            )

            for cand in response.candidates:
                messages.append(cand.content)

            if response.function_calls:
                for fc in response.function_calls:
                    if verbose_flag:
                        print(f"- Calling function: {fc.name}")
                    tool_msg = call_function(fc, verbose=verbose_flag)
                    messages.append(tool_msg)
                continue

            if verbose_flag:
                print(f"User prompt: {prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

            if response.text:
                print("Final response:\n" + response.text)
                break
        
        except Exception as e:
            print(f"Error during model generation: {e}")
            return
    


if __name__ == "__main__":
    main()
