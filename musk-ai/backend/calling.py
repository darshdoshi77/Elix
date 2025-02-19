from fastapi import FastAPI, HTTPException, APIRouter, Query
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from twilio.rest import Client
from fastapi.responses import Response
import urllib.parse
from OpenAI import *
from MongoDBclient import *

load_dotenv()

router = APIRouter()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


def call_request(request):
    
    calling_function = {
        "name": "contact_details",
        "description": "Extracts the name, number and message based on the user's request.",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "The recipient of the email"
                },
                "number":{
                    "type": "string",
                    "description": "The subject of the email",
                    "default" : "",
                },
                "message":{
                    "type": "string",
                    "description": "The message of the email"
                },
             },
            "required": ["name","number","message"]
        },
            
    }
    context_str = "extract the relevant details regarding the call request"
    
    gpt_output = run_gpt_function_call(request, context_str, [calling_function])
    name = gpt_output[0]['name']
    number = gpt_output[0].get('number','')
    message = gpt_output[0]['message']
    
    if check_name_in_db(name) and get_number(name) is not None:
        number = get_number(name)
    elif check_name_in_db(name) and get_number(name) is None:
        update_user_info_with_number(name,number)
    else:
        add_user_info(name,number,"")
    
    
    encoded_message = urllib.parse.quote(message)
    try:
       
        client.calls.create(
            to=number,
            from_=TWILIO_PHONE_NUMBER,
            url=f"https://a869-2601-644-401-b120-4527-8b23-98ec-1376.ngrok-free.app/twiml/?message={encoded_message}",
            method = "GET"
        )

        return f"Called {name} successfully"
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@router.get("/twiml/")

async def twiml_response(message: str = Query(...)):
    """
    Twilio webhook to generate TwiML (Text-to-Speech).
    """
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>{message}</Say>
    </Response>
    """
    return Response(content=twiml, media_type="application/xml")



    
    
  







