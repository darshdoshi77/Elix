from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from OpenAI import *
from exa import *
from email_fetchandsend import *
from calling import *
from openai import OpenAI
import os
from google_calendar import *  
from google_calendar import router as gc_router
from calling import router as twilio_router 
from texting import * 
import asyncio


load_dotenv()

app = FastAPI()
app.include_router(twilio_router)
app.include_router(gc_router, prefix="/calendar")

client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)

actions = ['web_search','chat_response','send_email','call_response','text','fetch_latest_emails','fetch_specific_email_from','create_event', 'check_availability','delete_event']

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
   determine_action_function = {
    "name": "determine_action",
    "description": "Decides the correct function/s to call based on the user's request.",
    "parameters": {
        "type": "object",
        "properties": {
            "actions": {
                "type": "array",
                "items": {
                        "type": "string",
                        "description": "the function to be executed"
                    }
                }
            },
        "required": ["actions"]
    }
}


   context_str = f"Based on the user's request, return the list of functions to be executed. Options:{actions}."

   gpt_output = run_gpt_function_call(request,context_str,[determine_action_function],temperature=0.2)
   print("gpt_output", gpt_output)
   list_actions = gpt_output[0]['actions']
   
   responses = []
   
   for action in list_actions:
    print("Action selection response:", action)

    if action == 'web_search':
       responses.append({"response" : web_search(request.message)})
   
    elif action == 'send_email':
       responses.append({"response": send_email(request.message)})
   
    elif action == 'call_response':
       responses.append({"response": call_request(request.message)})
   
    elif action == 'text':
       responses.append({"response" : send_text(request.message)})
   
    elif action == 'fetch_latest_emails':
       responses.append({"response" : fetch_recent_emails(request.message)})
   
    elif action == 'fetch_specific_email_from':
       responses.append({"response" : fetch_specific_email(request.message)})
   
    elif action == 'create_event':
        responses.append({"response" : await create_gc_event(request.message)})
    
    elif action == 'check_availability':
        responses.append({"response" : await check_gc_availability(request.message)})
    
    elif action == 'delete_event':
       responses.append({"response" : await delete_gc_event(request.message)})
   
    else:
       responses.append({"response": run_gpt_function_call(request.message,temperature=1)})
        
   return {"responses": responses}

@app.post("/transcribe")

async def voicechat(file: UploadFile = File(...)):
   try:
       file_location = f"temp_audio.wav"
       with open(file_location, "wb") as buffer:
           buffer.write(await file.read())


       with open(file_location, "rb") as audio_file:
           response = client.audio.transcriptions.create(
               model="whisper-1",
               file=audio_file
           )


       return {"text": response.text}


   except Exception as e:
       return {"error": str(e)}
  
  

