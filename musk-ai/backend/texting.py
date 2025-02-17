import subprocess
from OpenAI import * 

def send_text(request):
    text_function = {
        "name": "text_details",
        "description": "Extracts the number and message based on the user's request.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the recipient"
                },
                "phone_number": {
                    "type": "string",
                    "description": "The phone number of the recipient"
                },
                "message":{
                    "type": "string",
                    "description": "The message of the text" 
                },
             },
        },
            "required": ["name","phone_number","message"]
    }
    context_str = "extract the relevant details regarding the call request"
    
    gpt_output = run_gpt_function_call(request, context_str, [text_function])
    name = gpt_output[0]['name']
    phone_number = gpt_output[0]['phone_number']
    message = gpt_output[0]['message']
    
    script = f'''
    tell application "Messages"
        send "{message}" to buddy "{phone_number}"
    end tell
    '''
    subprocess.run(["osascript", "-e", script])
    return f"Texted {name} successfully"
