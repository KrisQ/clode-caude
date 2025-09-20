import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function


def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if len(sys.argv) < 1:
        sys.exit(1)

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
        ]
    )

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    user_prompt = sys.argv[1]

    verbose = "--verbose" in sys.argv

    messages = [types.Content(role="user", parts=[types.Part(text=user_prompt)])]

    client = genai.Client(api_key=api_key)
    for i in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(
                    system_instruction=system_prompt, tools=[available_functions]
                ),
            )
            if response.text:
                print(response.text)
                break
            if response.candidates:
                for c in response.candidates:
                    if c.content:
                        messages.append(c.content)

            if response.usage_metadata is not None:
                if response.function_calls:
                    for f in response.function_calls:
                        result = call_function(
                            {"name": f.name, "args": f.args}, verbose
                        )
                        if not result.parts[0].function_response.response:
                            raise Exception("Oh no")
                        if verbose:
                            print(f"-> {result.parts[0].function_response.response}")

                        message = types.Content(
                            role="user",
                            parts=[
                                types.Part(
                                    text=result.parts[0].function_response.response
                                )
                            ],
                        )
                        messages.append(message)

                print(response.text)
                if verbose:
                    print(f"User prompt: {user_prompt}")
                    print(
                        f"Prompt tokens: {response.usage_metadata.prompt_token_count}"
                    )
                    print(
                        f"Response tokens: {response.usage_metadata.candidates_token_count}"
                    )
            else:
                print("something went wrong")
        except Exception as e:
            print(e)


if __name__ == "__main__":
    main()
