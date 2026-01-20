import os
import argparse
import sys
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function


def main():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    print("Hello from aiagent!")
    try:
        i = 0
        for i in range(20):
            response = client.models.generate_content(
                model='gemini-2.5-flash', 
                contents= messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt),
            )
            if len(response.candidates) > 0:
                for candidate in response.candidates:
                    messages.append(candidate.content)


            if args.verbose and response.usage_metadata is not None:
                print(f'User prompt: {args.user_prompt}')
                print(f'Prompt tokens: {response.usage_metadata.prompt_token_count}')
                print(f'Response tokens: {response.usage_metadata.candidates_token_count}')
            
            if response.function_calls:
                function_results = []
                for function_call in response.function_calls:
                    function_call_result = call_function(function_call, args.verbose)
                    if len(function_call_result.parts) < 1:
                        raise Exception
                    if not function_call_result.parts[0].function_response:
                        raise Exception
                    if not function_call_result.parts[0].function_response.response:
                        raise Exception
                    function_results.append(function_call_result.parts[0])
                    if args.verbose:
                        print(f"-> {function_call_result.parts[0].function_response.response}")        
                messages.append(types.Content(role="user", parts=function_results))
                i += 1
            else:
                print(response.text)
                break
        if i >= 20:
            print(f"model failed to produce a final result")
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        return


if __name__ == "__main__":
    main()
