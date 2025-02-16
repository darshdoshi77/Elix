import base64
import pickle
import os
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from OpenAI import *


def send_email(request):
    email_function = {
        "name": "email_details",
        "description": "Extracts the recipient, subject and message based on the user's request.",
        "parameters": {
            "type": "object",
            "properties": {
                "recipient": {
                    "type": "string",
                    "description": "The recipient of the email"
                },
                "subject":{
                    "type": "string",
                    "description": "The subject of the email" 
                },
                "message_text":{
                    "type": "string",
                    "description": "The message of the email" 
                },
             },
        },
            "required": ["recipient","subject","message_text"]
    }
    context_str = "extract the relevant details regarding the email request"
    
    gpt_output = run_gpt_function_call(request, context_str, [email_function])
    recipient = gpt_output[0]['recipient']
    subject = gpt_output[0]['subject']
    message_text = gpt_output[0]['message_text']
    
    service = get_gmail_service()

    message = MIMEText(message_text)
    message["to"] = recipient
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    
    try:
        service.users().messages().send(
            userId="me", body={"raw": raw_message}
        ).execute()
        response = "Email sent successfully!"
    except Exception as e:
        response = "Error sending email"
        
    return response

def get_gmail_service():
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
        return build("gmail", "v1", credentials=creds)
    else:
        raise Exception("No token.pickle found! Run authentication script first.")
