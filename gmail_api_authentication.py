import os.path
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def setup_gmail_api(credentials_path='credentials-gmail_api.json'):
    """
    Setup Gmail & Google Calendar API authentication and return service objects.

    Args:
        credentials_path (str): Path to your credentials.json file.

    Returns:
        tuple: (Gmail API service object, Google Calendar API service object)
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
              'https://www.googleapis.com/auth/gmail.send',
              'https://www.googleapis.com/auth/calendar.events']

    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            creds = flow.run_local_server(port=8080)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Build both Gmail & Google Calendar API services
    gmail_service = build('gmail', 'v1', credentials=creds)
    calendar_service = build('calendar', 'v3', credentials=creds)

    return gmail_service, calendar_service


def test_gmail_connection(service):
    """
    Test the Gmail API connection by retrieving user profile.

    Args:
        service: Authenticated Gmail API service object
    """
    try:
        user_profile = service.users().getProfile(userId='me').execute()
        print(f"✅ Successfully connected to Gmail API for: {user_profile['emailAddress']}")
        return True
    except Exception as e:
        print(f"❌ Error connecting to Gmail API: {str(e)}")
        return False


def test_calendar_connection(service):
    """
    Test the Google Calendar API connection by retrieving upcoming events.

    Args:
        service: Authenticated Google Calendar API service object
    """
    try:
        events_result = service.events().list(calendarId='primary', maxResults=5).execute()
        events = events_result.get('items', [])
        if not events:
            print("📅 No upcoming events found.")
        else:
            print("📅 Upcoming events:")
            for event in events:
                print(f"  - {event['summary']}")
        return True
    except Exception as e:
        print(f"❌ Error connecting to Google Calendar API: {str(e)}")
        return False


if __name__ == "__main__":
    print("🚀 Starting Google API setup...")
    print("🔗 Ensure this redirect URI is added to Google Cloud Console OAuth 2.0 Client ID:")
    print("   ➤ http://localhost:8080/")

    # Initialize Gmail & Calendar services
    gmail_service, calendar_service = setup_gmail_api()

    # Test Gmail API
    test_gmail_connection(gmail_service)

    # Test Google Calendar API
    test_calendar_connection(calendar_service)
