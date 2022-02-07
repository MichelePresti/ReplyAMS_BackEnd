from googleapiclient.discovery import build, Resource
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path
import base64
import email
from bs4 import BeautifulSoup
import pandas as pd

from storage_service import StorageService

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class EmailManager:

    def __init__(self):
        self.newEmail = False
        self.totalEmailNumber = 0

    def get_unread_message(self):
        return self.newEmail

    def set_unread_message(self, message):
        self.newEmail = message
        if message is True:
            self.totalEmailNumber += 1


class EmailService:

    def __init__(self, e_mail, password, imap, storage: StorageService):
        self.e_mail = e_mail
        self.password = password
        self.imap = imap,
        self.storage = storage

    def get_emails(self):
        creds = None

        if os.path.exists('token.pickle'):
            # Read the token from the file and store it in the variable creds
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)

            # If credentials are not available or are invalid, ask the user to log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle file for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

            # Connect to the Gmail API
        service = build('gmail', 'v1', credentials=creds)

        # request a list of all the messages
        result = service.users().messages().list(userId='me', q='is: unread').execute()

        # We can also pass maxResults to get any number of emails. Like this:
        # result = service.users().messages().list(maxResults=200, userId='me').execute()
        messages = result.get('messages')
        # messages is a list of dictionaries where each dictionary contains a message id.

        # iterate through all the messages
        if messages is not None:
            for msg in messages:
                if self.storage.register_new_email(msg['id']) > 0:
                    # Get the message from its id
                    txt = service.users().messages().get(userId='me', id=msg['id']).execute()
                    print(txt)
                    # Use try-except to avoid any Errors
                    try:
                        # Get value of 'payload' from dictionary 'txt'
                        payload = txt['payload']
                        email_id = txt['id']
                        headers = payload['headers']

                        # The Body of the message is in Encrypted format. So, we have to decode it.
                        # Get the data and decode it with base 64 decoder.
                        parts = payload.get('parts')[0]
                        data = parts['body']['data']
                        data = data.replace("-", "+").replace("_", "/")
                        decoded_data = base64.b64decode(data)
                        print(parts)
                        print('############################')
                        print(headers)

                        if str(decoded_data).lower().find('very high') > 0:
                            return True, data
                        else:
                            return False, ''

                    except:
                        print('Error in SOUP')
