# Musk AI: Personal AI Assistant

## Overview
Musk AI is a personal AI assistant designed to streamline your daily tasks by integrating advanced AI capabilities with essential productivity tools. With support for calling, texting, email management, Google Calendar integration, and OpenAI-powered intelligence, Musk AI helps you stay organized and efficient.

## Features
- **Voice Calling**: Make and receive calls directly from the assistant.
- **Text Messaging**: Send and receive SMS messages.
- **Email Management**: Fetch, read, and send emails using your connected account.
- **Google Calendar Integration**: View, create, and manage calendar events.
- **OpenAI Integration**: Leverage powerful AI for natural language understanding and task automation.
- **Modern Web Interface**: Built with Next.js and Tailwind CSS for a responsive, user-friendly experience.

## Setup
### Prerequisites
- Node.js (v16+ recommended)
- Python 3.8+
- pip (Python package manager)
- Google API credentials (for Calendar and Gmail)
- OpenAI API key

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/musk-ai.git
   cd musk-ai
   ```
2. **Install Node.js dependencies:**
   ```bash
   npm install
   ```
3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables:**
   - Place your Google API credentials in `backend/credentials-google_api.json`.
   - Set your OpenAI API key in the appropriate config or environment variable.

5. **Start the backend server:**
   ```bash
   python backend/main.py
   ```
6. **Start the frontend:**
   ```bash
   npm run dev
   ```

## Usage
- Access the web interface at `http://localhost:3000`.
- Use the assistant to make calls, send texts, manage emails, and interact with your calendar.
- All AI-powered features are enabled via OpenAI integration.

## Contributing
Contributions are welcome! Please open issues or submit pull requests for new features, bug fixes, or improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



