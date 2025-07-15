from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

def run_gpt_function_call(text, context="", functions=None, temperature = 0.2, model="gpt-4"):
    if functions is None:
        functions = []
        
    client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))
        
    content_str = f"{context} \n {text}"
    messages = [{"role": "user", "content": content_str}]
    tools = [{"type": "function","function": func} for func in functions]
    
    response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools if tools else None,
    tool_choice="required" if tools else None,  
    temperature=temperature,
    )

    if not functions or not hasattr(response.choices[0].message, "tool_calls"):
        return response.choices[0].message.content
    
    tool_calls = response.choices[0].message.tool_calls
    
    return [json.loads(call.function.arguments) for call in tool_calls] if tool_calls else response.choices[0].message.content


