import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys


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

    response = client.models.generate_content(
        model=model,
        contents=messages,
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
            
    print(response.text)


if __name__ == "__main__":
    main()
