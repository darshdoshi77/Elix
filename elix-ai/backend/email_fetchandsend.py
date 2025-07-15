import base64
import pickle
import os
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from OpenAI import *
from bs4 import BeautifulSoup
import json
from MongoDBclient import *

def send_email(request):
    email_function = {
        "name": "email_details",
        "description": "Extracts the name, recipient, subject and message based on the user's request.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name of the recipient",
                    "default" : ""
                },
                "recipient": {
                    "type": "string",
                    "description": "The recipient of the email",
                    "default": ""
                },
                "subject":{
                    "type": "string",
                    "description": "The subject of the email",
                    "default": ""     
                },
                "message_text":{
                    "type": "string",
                    "description": "The message of the email" 
                },
             },
             "required": ["name","recipient","subject","message_text"]
        },
           
    }
    context_str = "extract the relevant details regarding the email request"
    
    gpt_output = run_gpt_function_call(request, context_str, [email_function])
    name = gpt_output[0]['name']
    recipient = gpt_output[0]['recipient']
    subject = gpt_output[0]['subject']
    message_text = gpt_output[0]['message_text']
    
    if check_name_in_db(name) and get_email_id(name) is not None:
        recipient = get_email_id(name)
    elif check_name_in_db(name) and get_email_id(name) is None:
        update_user_info_with_email(name,recipient)
    else:
        add_user_info(name,"",recipient)
        
    
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


def fetch_recent_emails(request):
    latest_email_function = {
        "name": "no_of_latest_emails",
        "description": "Extracts the number of latest emails based on the user's request.",
        "parameters": {
            "type": "object",
            "properties": {
                "number_of_emails": {
                    "type": "integer",
                    "description": "The number of latest emails required."
                },
             },
        },
            "required": ["number_of_emails"]
    }
    context_str = "extract the number of latest emails"
    
    gpt_output = run_gpt_function_call(request, context_str, [latest_email_function])
    k = gpt_output[0]['number_of_emails']
  
    service = get_gmail_service()

    try:
        results = service.users().messages().list(userId="me", maxResults=k).execute()
        messages = results.get("messages", [])

        if not messages:
            return "No recent emails found"

        emails = []
        for msg in messages:
            msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()

            headers = msg_data["payload"]["headers"]
            subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
            sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")

            email_body = ""
            if "data" in msg_data["payload"]["body"]:
                body_data = msg_data["payload"]["body"]["data"]
                email_body = base64.urlsafe_b64decode(body_data).decode("utf-8")

            email_text = BeautifulSoup(email_body, "html.parser").get_text()

            emails.append({"sender": sender, "subject": subject, "preview": email_text[:150]}) 

        return "\n\n".join(f'Sender: {email["sender"]}\nSubject: {email["subject"]}\nPreview: {email["preview"]}'
        for email in emails)


    except Exception as e:
        return json.dumps([{"status": "Error fetching emails", "error": str(e)}])


def fetch_specific_email(request):
    specific_email_function = {
        "name": "specific_email",
        "description": "Extracts name and email address based on the user's request.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The name associated with the specific email.",
                    "default" : ""
                },
                
                "specific_email_id": {
                    "type": "string",
                    "description": "The specific email id.",
                    "default" : ""
                },
             },
            "required": ["name", "specific_email_id"]
        },
        
    }
    context_str = "extract the name and specific email id"
    
    gpt_output = run_gpt_function_call(request, context_str, [specific_email_function])
    print("gpt out", gpt_output)
    name = gpt_output[0].get('name','')
    sender_email = gpt_output[0].get('specific_email_id','')
   
    if check_name_in_db(name) and get_email_id(name) is not None:
        sender_email = get_email_id(name)
    elif check_name_in_db(name) and get_email_id(name) is None:
        update_user_info_with_email(name,sender_email)
    else:
        add_user_info(name,"",sender_email)
   
   
    service = get_gmail_service()

    try:
        
        query = f"from:{sender_email}"
        results = service.users().messages().list(userId="me", maxResults=1, q=query).execute()
        messages = results.get("messages", [])

        if not messages:
            return f"No emails found from {sender_email}"

        msg_data = service.users().messages().get(userId="me", id=messages[0]["id"]).execute()

        headers = msg_data["payload"]["headers"]
        subject = next((h["value"] for h in headers if h["name"] == "Subject"), "No Subject")
        sender = next((h["value"] for h in headers if h["name"] == "From"), "Unknown Sender")

        email_body = ""
        if "data" in msg_data["payload"]["body"]:
            body_data = msg_data["payload"]["body"]["data"]
            email_body = base64.urlsafe_b64decode(body_data).decode("utf-8")

        email_text = BeautifulSoup(email_body, "html.parser").get_text()

        return f"""Sender: {sender}
            Subject: {subject}
            Preview: {email_text[:250]+"..."}
            """

    except Exception as e:
        return {"status": "Error fetching email", "error": str(e)}



def get_gmail_service():
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
        return build("gmail", "v1", credentials=creds)
    else:
        raise Exception("No token.pickle found! Run authentication script first.")

