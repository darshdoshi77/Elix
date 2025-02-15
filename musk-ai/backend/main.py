from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import pickle
from googleapiclient.discovery import build
from integrations import *

load_dotenv()

app = FastAPI()

app.add_middleware(
   CORSMiddleware,
   allow_origins=["*"],
   allow_credentials=True,
   allow_methods=["*"],
   allow_headers=["*"],
)


client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))


class ChatRequest(BaseModel):
   message: str
  
class EmailRequest(BaseModel):
   recepient: str
   subject: str
   message: str


actions = ['get_stock_info', 'get_weather', 'web_search','send_email', 'chat_response','get_news','call_response']


@app.post("/send_email")


async def send_email(request: EmailRequest):
   with open("token.pickle", "rb") as token:
       creds = pickle.load(token)
   service = build("gmail", "v1", credentials=creds)
   try:
       send_message = service.users().messages().send(
           userId="me", body={"raw": message}
       ).execute()
       print(f"Email sent successfully! Message ID: {send_message['id']}")
   except Exception as e:
       print(f"Error sending email: {e}")




@app.post("/chat")
async def chat(request: ChatRequest):
   system_prompt = f"Based on the user's request, return the correct function name. Options:{actions}. Respond with ONLY one of these actions."

   response = client.chat.completions.create(
       model="gpt-4",
       temperature=0.2,
       messages=[
           {"role": "system", "content": system_prompt},
           {"role": "user", "content": request.message}
       ]
   )
  
   action = response.choices[0].message.content.strip()

   if action == 'chat_response':
        return chat_response(request)
      
   elif action == 'call_response':
        return call_response(request)
      
   elif action == 'get_weather':
        return get_weather(request)
      
   elif action == 'get_stock_info':
        return get_stock_info(request)
      
   elif action == 'send_email':
        return send_email(request)
                 
   elif action == 'web_search':
        return web_search(request)
          
   elif action == 'get_news':
        return get_news(request)
    
    
 
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
  
  

