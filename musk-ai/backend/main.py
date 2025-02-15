from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from openai import OpenAI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
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
    

@app.post("/chat")
async def chat(request: ChatRequest):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": request.message}]
    )
    return {"response": response.choices[0].message.content}

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
    
    