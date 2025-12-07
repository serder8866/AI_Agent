import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types




def main():
    print("Hello from ai-agent!")
    # Reads all the lines from .env file
    load_dotenv()
    # os.environ.get accesses those lines
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("There is no API key in the .env file")
    
    #Create an instance of an argument parser
    parser = argparse.ArgumentParser(description="Chatbot")
    # Add individual arguments that can be expected / that are needed
    parser.add_argument("prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    # all the arguments from the CLI input are parsed and placed in args.
    # They can be accessed by args.argument_name (the first argument you give to add_argument)
    args = parser.parse_args()
    # Now we can access `args.prompt`
    
    client = genai.Client(api_key=api_key)
    # I need to spend some time understanding these objects. Why is there .Part inside .Content? What wierd style is this?
    messages = [types.Content(role="user", parts=[types.Part(text=args.prompt)])]
    
    # GeneratedContentResponse object
    response = client.models.generate_content(model="gemini-2.5-flash", contents=messages)
    if not response.usage_metadata:
        raise RuntimeError("failed API request")
    if args.verbose:
        print(f"User prompt: {args.prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
    print(response.text)

if __name__ == "__main__":
    main()
