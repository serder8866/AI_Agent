import os
import argparse
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from prompts import system_prompt
from call_function import available_functions, call_function


def main():
    
    parser = argparse.ArgumentParser(description="Chatbot", epilog="Th Th Th That's all folks!")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key is None:
        raise RuntimeError("The API key was not found")
    
    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")
    
    for _ in range(20):
        code = generate_content(client, messages, args.verbose)
        if code == 0:
            break
    if code != 0:
        print("The agent needs more then 20 function calls for this task.")
        sys.exit(1)
    

def generate_content(client, messages, verbose):
    response = client.models.generate_content(
        model="gemini-2.5-flash", 
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt, temperature=0
            )
        )
    
    if not response.usage_metadata:
        raise RuntimeError("Failed API Request")
    
    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if not response.function_calls:
        print("Response:")
        print(response.text)
        return 0
    
    function_results = []
    for function_call in response.function_calls:
        function_call_result = call_function(function_call, verbose)
        if not function_call_result.parts:
            raise Exception(f"There is no response from the {function_call.name}")
        if function_call_result.parts[0].function_response == None:
            raise Exception(f"FunctionResponse Object of {function_call.name} is None")
        if function_call_result.parts[0].function_response.response == None:
            raise Exception(f"Function response of {function_call.name} is None")
        function_results.append(function_call_result.parts[0])
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
    
    messages.append(types.Content(role="user", parts=function_results))

if __name__ == "__main__":
    main()