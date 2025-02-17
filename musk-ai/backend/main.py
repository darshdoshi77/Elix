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
        "description": "Decides the correct function to call based on the user's request.",
        "parameters": {
            "type": "object",
            "properties": {
                "action": {
                    "type": "string",
                    "description": "The function name that should be executed."
                }
             },
            "required": ["action"]
         }
    }

   context_str = f"Based on the user's request, return the correct function name. Options:{actions}. Respond with ONLY one of these actions."

   gpt_output = run_gpt_function_call(request,context_str,[determine_action_function],temperature=0.2)
   action = gpt_output[0]['action']
   print("Action selection response:", action)

   if action == 'web_search':
       return {"response" : web_search(request.message)}
   
   elif action == 'send_email':
       return {"response": send_email(request.message)}
   
   elif action == 'call_response':
       return {"response": call_request(request.message)}
   
   elif action == 'text':
       return {"response" : send_text(request.message)}
   
   elif action == 'fetch_latest_emails':
       return {"response" : fetch_recent_emails(request.message)}
   
   elif action == 'fetch_specific_email_from':
       return {"response" : fetch_specific_email(request.message)}
   
   elif action == 'create_event':
        return {"response" : await create_gc_event(request.message)}
    
   elif action == 'check_availability':
        return {"response" : await check_gc_availability(request.message)}
    
   elif action == 'delete_event':
       return {"response" : await delete_gc_event(request.message)}
   
   else:
       return {"response": run_gpt_function_call(request.message,temperature=1)}
        
 
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
  
  

