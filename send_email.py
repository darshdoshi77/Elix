import base64
import pickle
import os
from email.mime.text import MIMEText
from googleapiclient.discovery import build

# Load credentials from token.pickle
def get_gmail_service():
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
        return build("gmail", "v1", credentials=creds)
    else:
        raise Exception("❌ No token.pickle found! Run authentication script first.")

# Function to send an email
def send_email(recipient, subject, message_text):
    service = get_gmail_service()

    # Create email message
    message = MIMEText(message_text)
    message["to"] = recipient
    message["subject"] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    # Send email
    try:
        send_message = service.users().messages().send(
            userId="me", body={"raw": raw_message}
        ).execute()
        print(f"✅ Email sent successfully! Message ID: {send_message['id']}")
    except Exception as e:
        print(f"❌ Error sending email: {e}")

# Example usage
if __name__ == "__main__":
    recipient_email = "darshdoshi16@berkeley.edu"  # Change to actual recipient
    subject = "Test Email from Gmail API"
    body = "Hello! This is a test email sent via Gmail API.Kem Party"

    send_email(recipient_email, subject, body)
