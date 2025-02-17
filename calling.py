from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from twilio.rest import Client
from fastapi.responses import Response
import urllib.parse


load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")


client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class CallRequest(BaseModel):
    name: str
    number: str
    message: str

app = FastAPI()

@app.post("/make_call/")


async def make_call(request: CallRequest):
    encoded_message = urllib.parse.quote(request.message)
    try:
       
        call = client.calls.create(
            to=request.number,
            from_=TWILIO_PHONE_NUMBER,
            url=f"https://eeb6-2601-644-401-b120-fc26-e02-c859-15a6.ngrok-free.app/twiml/?message={encoded_message}",
            method = "GET"
        )

        return {"status": f"Call initiated to {request.name}", "call_sid": call.sid}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    
@app.get("/twiml/")

async def twiml_response(message: str):
    """
    Twilio webhook to generate TwiML (Text-to-Speech).
    """
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Say>{message}</Say>
    </Response>
    """
    return Response(content=twiml, media_type="application/xml")



    
    
  







