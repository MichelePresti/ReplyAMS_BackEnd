import json
import requests
import firebase_admin
from firebase_admin import credentials
import push_notification_service
import storage_service as ss
import email_service as es
import web_api
import time

keyPath = 'C:/Users/Michele/Downloads/replyams-64832-firebase-adminsdk-2t25c-48f5992cbb.json'
unread_message = 0


def get_unread_message():
    global unread_message
    return unread_message


def set_unread_message(message):
    global unread_message
    unread_message = message


storage = ss.StorageService()
api = web_api.AppAPI()
api.init_api()
api.run()

if storage.init_storage():
    email_service = es.EmailService(storage.get_email(), storage.get_password(), storage.get_imap())
    fcm_service = push_notification_service
    fcm_service.init_service(keyPath)
    while True:
        time.sleep(90)
        new_email = email_service.get_emails()
        if new_email:
            unread_message = 1
            tokens = storage.get_user_tokens()
            fcm_service.send_notification(tokens, 'New very high ticket opened')

