# Elix AI: Personal AI Assistant

## Overview
Elix AI is a personal assistant designed to streamline your daily tasks by integrating essential productivity tools into a single, modern web application. With support for calling, texting, email management, and Google Calendar integration, Elix AI helps you stay organized and efficient. The platform is built for extensibility, enabling future integration of additional smart features and services.

## Features
- **Voice Calling**: Make and receive calls directly from the assistant.
- **Text Messaging**: Send and receive SMS messages.
- **Email Management**: Fetch, read, and send emails using your connected account.
- **Google Calendar Integration**: View, create, and manage calendar events.
- **Modern Web Interface**: Built with Next.js and Tailwind CSS for a responsive, user-friendly experience.
- **Extensible Architecture**: Designed to easily incorporate new features and third-party integrations.

## Setup
### Prerequisites
- Node.js (v16+ recommended)
- Python 3.8+
- pip (Python package manager)
- Google API credentials (for Calendar and Gmail)

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

5. **Start the backend server:**
   ```bash
   python backend/main.py
   ```
6. **Start the frontend:**
   ```bash
   npm run dev
   ```

## Usage
- Once both the backend and frontend are running, access the web interface through your browser.
- Use the assistant to make calls, send texts, manage emails, and interact with your calendar—all from one place.

## Future Potential
Musk AI is designed with extensibility in mind. Planned and potential future enhancements include:
- Integration with additional productivity and communication platforms
- Advanced automation and smart scheduling features
- Personalized notifications and reminders
- Support for more natural voice and text interactions
- Enhanced security and privacy controls

## Contributing
Contributions are welcome! Please open issues or submit pull requests for new features, bug fixes, or improvements.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.



