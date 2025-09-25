import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import get_files_info, schema_get_files_info




def main():
    load_dotenv()
    key = os.environ.get("GEMINI_API_KEY")

    client = genai.Client(api_key=key)

    model = "gemini-2.0-flash-001"

    if len(sys.argv) < 2:
        raise Exception("Please provide a prompt as a command line argument.")  
    

    prompt = sys.argv[1]

    messages = [
        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]
    
    # system prompt example
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    

    # available functions
    available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)


    response = client.models.generate_content(
        model=model,
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt),
    )

    if len(sys.argv) > 2:
        match sys.argv[2]:
            case "--verbose":
                user_prompt = response.usage_metadata.prompt_token_count
                response_tokens = response.usage_metadata.candidates_token_count
                print(f"User prompt: {prompt}")
                print(f"Prompt tokens: {user_prompt}")
                print(f"Response tokens: {response_tokens}")
                return 0
            case _:
                raise Exception("Unknown flag. Only --verbose is supported.")
            
    

    if len(response.function_calls) > 0:
        for function_call in response.function_calls:
            print(f"calling function: {function_call.name}({function_call.args})")
    else:
        print(response.text)



if __name__ == "__main__":
    main()
