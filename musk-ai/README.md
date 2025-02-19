
# Musk AI - AI Chatbot with Web Search, Calls, Texting & Calendar Integration

Musk AI is an AI-powered assistant built using **Next.js (React + TypeScript) for the frontend** and **FastAPI (Python) for the backend**. It integrates **OpenAI's GPT, Twilio (for calls and texting), Google Calendar API (for event management), and Exa (for web search).**

## Features
- **Chat with AI** powered by OpenAI (GPT-4).
- **Web Search** using Exa API.
- **Send Emails** via Gmail API.
- **Text Messages & Calls** using Twilio.
- **Google Calendar Integration**:
  - Create events
  - Check availability
  - Delete events
- **Voice Input & Transcription** using Whisper AI.

---

## Tech Stack
| Component     | Technology |
|--------------|------------|
| **Frontend** | Next.js (React + TypeScript), Tailwind CSS |
| **Backend**  | FastAPI (Python) |
| **Database** | MongoDB (for storing user data) |
| **APIs Used** | OpenAI, Twilio, Google Calendar, Exa |

---

## Installation & Setup
### Clone the Repository
```bash
git clone https://github.com/yourusername/musk-ai.git
cd musk-ai
```

### Backend Setup (FastAPI)
#### Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Set up environment variables
Create a `.env` file inside the `backend/` directory and add:
```ini
OPEN_AI_KEY=your-openai-api-key
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-auth-token
TWILIO_PHONE_NUMBER=your-twilio-phone-number
DATABASE_URI=your-mongodb-uri
EXA_API_KEY=your-exa-api-key
```

#### Run FastAPI server
```bash
uvicorn main:app --reload
```
Your backend is now running at `http://127.0.0.1:8000`

---

### Frontend Setup (Next.js)
#### Install dependencies
```bash
cd app
npm install
```

#### Run Next.js Development Server
```bash
npm run dev
```
Your frontend is now running at `http://localhost:3000`

---

## API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| `POST` | `/chat` | Process chat requests and decide the correct AI action |
| `POST` | `/transcribe` | Convert voice input to text using Whisper AI |
| `POST` | `/create_event` | Create a Google Calendar event |
| `GET`  | `/check_availability` | Check if a time slot is free on Google Calendar |
| `DELETE` | `/delete_event` | Delete a calendar event by title |
| `POST` | `/send_email` | Send an email using Gmail API |
| `POST` | `/text` | Send a text message using Twilio |
| `POST` | `/call` | Make a phone call using Twilio |

---

## Project Structure
```
musk-ai/
│── app/                  # Next.js frontend
│   ├── globals.css       # Styling
│   ├── layout.tsx        # Main layout
│   ├── page.tsx          # Chat UI
│   ├── recorder.tsx      # Voice input UI
│
│── backend/              # FastAPI backend
│   ├── integrations/     # External API integrations
│   ├── calling.py        # Twilio call handling
│   ├── texting.py        # Twilio SMS handling
│   ├── google_calendar.py # Google Calendar API integration
│   ├── email_fetchsend.py # Gmail API integration
│   ├── OpenAI.py         # OpenAI API integration
│   ├── main.py           # FastAPI app entry point
│   ├── MongoDBclient.py  # MongoDB user storage
│   ├── token.pickle      # Google API credentials
│
└── README.md             # Project documentation
```

---

## Example Usage
### Chatting with AI
Send a `POST` request to `/chat` with:
```json
{
  "message": "Schedule a meeting with John at 3 PM tomorrow"
}
```
AI will process the request and create a Google Calendar event.

---

### Making a Call via Twilio
Send a `POST` request to `/call` with:
```json
{
  "name": "John Doe",
  "message": "Hello, this is an automated call!"
}
```
AI will fetch John’s phone number from MongoDB and place the call.

---

### Sending a Text Message
Send a `POST` request to `/text` with:
```json
{
  "name": "John Doe",
  "message": "Hey John, let's meet at 5 PM!"
}
```
AI will retrieve John’s number and send the message via Twilio.

---

## Future Improvements
- Add OAuth-based user authentication.
- Improve AI’s ability to process complex requests.
- Enhance error handling for external API failures.

---

## License
This project is licensed under the **MIT License**.

---

## Contributing
Want to contribute? Fork the repo, create a feature branch, and submit a pull request.

---

## Author
Darsh Doshi  
Email: darshdoshi16@berkeley.edu  
[LinkedIn](https://linkedin.com/in/darsh-doshi) | [GitHub](https://github.com/darshdoshi16)



