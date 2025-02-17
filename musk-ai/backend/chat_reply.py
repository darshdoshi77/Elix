import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPEN_AI_KEY"))


def chat_response(request):  
   response = client.chat.completions.create(
       model="gpt-4",
       temperature=0.8,
       messages=[{"role": "user", "content": request.message}]
   )
   return {"response": response.choices[0].message.content}


