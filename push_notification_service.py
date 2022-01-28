import json
import requests
import firebase_admin
from firebase_admin import credentials, messaging

serverToken = 'AAAAHeELsu0:APA91bHScmxbmvSuVYswsd5Y2hIUZnwW2yWzVsKILHrRScVvK6vyAjllNcpbWRe3l0aLKZjkK' \
              '-d8c59iJCVZ3ZI67riMYDwxX5K9hJr3xBA_tjlwC23dHH5LdDEsvGQuNw2UrNUDfPTB '

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'key=' + serverToken,
}


def init_service(credentialKeyPath):
    cred = credentials.Certificate(credentialKeyPath)
    firebase_admin.initialize_app(cred)


def send_notification(to: list, message, priority='high', title='Reply AMS'):
    tokens = []
    for token in to:
        tokens.append(token)
    message = messaging.MulticastMessage(
        data={
            'title': title,
            'body': message,
            'type': 'WAKEUP'
        },
        tokens=tokens,
        android=messaging.AndroidConfig(
            priority='high'
        )
    )
    response = messaging.send_multicast(message)
    print('{0} messages were sent successfully'.format(response.success_count))
