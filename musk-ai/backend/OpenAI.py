from openai import OpenAI
from dotenv import load_dotenv
import json
load_dotenv()


def run_llm_function_call(text, context, functions, temperature, model="gpt-4"):
    client = OpenAI()
    content_str = f"{context} \n {text}"
    content = [{"type": "text", "text": content_str}]
    messages = [{"role": "user", "content": content}]
    
    response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=functions,
    tool_choice="required",  
    temperature=temperature,
    )

    return [
        call.function
        for call in response.choices[0].message.tool_calls
        ]


def get_function_arguments(response):
    
    return [
        json.loads(call.arguments)
        for call in response
    ]