from openai import OpenAI
from dotenv import load_dotenv
import json
import os

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

def run_llm_function_call(text, context, functions, temperature, model="gpt-4"):
    
    content_str = f"{context} \n {text}"
    messages = [{"role": "user", "content": content_str}]
    tools = [{
        "type": "function",
        "function": func 
        } for func in functions]
    response = client.chat.completions.create(
    model=model,
    messages=messages,
    tools=tools,
    tool_choice="required",  
    temperature=temperature,
    )

    tool_calls = response.choices[0].message.tool_calls
    if tool_calls is None:
        return []

    return [json.loads(call.function.arguments) for call in tool_calls]



