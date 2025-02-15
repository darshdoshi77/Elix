import os.path
import pickle
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

def setup_gmail_api(credentials_path='credentials-gmail_api.json'):
    """
    Setup Gmail API authentication and return the service object.
    
    Args:
        credentials_path (str): Path to your credentials.json file
                              Defaults to 'credentials-gmail_api.json'
    
    Returns:
        service: Authenticated Gmail API service object
    """
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly',
              'https://www.googleapis.com/auth/gmail.send']
    
    creds = None
    # Check if we have valid token.pickle
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If credentials don't exist or are invalid
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Create the flow instance with specific port
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path, SCOPES)
            
            # Print the redirect URI that will be used
            port = 8080 # Using a fixed port for predictability
            redirect_uri = f'http://localhost:{port}/'
            print(f"Please add this redirect URI to Google Cloud Console: {redirect_uri}")
            
            # Run the server with the specified port
            creds = flow.run_local_server(port=port)
            
        # Save credentials for future use
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Build and return the Gmail service
    service = build('gmail', 'v1', credentials=creds)
    return service

def test_gmail_connection(service):
    """
    Test the Gmail API connection by retrieving user profile.
    
    Args:
        service: Authenticated Gmail API service object
    """
    try:
        user_profile = service.users().getProfile(userId='me').execute()
        print(f"Successfully connected to Gmail API for: {user_profile['emailAddress']}")
        return True
    except Exception as e:
        print(f"Error connecting to Gmail API: {str(e)}")
        return False

if __name__ == "__main__":
    print("Starting Gmail API setup...")
    print("Make sure this redirect URI is added to your Google Cloud Console OAuth 2.0 Client ID:")
    print("http://localhost:8080/")
    
    # Initialize the Gmail API service
    gmail_service = setup_gmail_api()
    
    # Test the connection
    test_gmail_connection(gmail_service)