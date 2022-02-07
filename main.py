import json
import requests
import firebase_admin
from firebase_admin import credentials
import push_notification_service
import storage_service as ss
import email_service as es
import web_api
import time
from threading import Thread

keyPath = 'API_Key.json'


def api_thread(email_manager_thread: es.EmailManager, storage_service: ss.StorageService):
    print("Api Thread Activated")
    email_service_t1 = es.EmailService(storage_service.get_email(), storage_service.get_password(), storage_service.get_imap())
    api = web_api.AppAPI(email_manager_thread, email_service_t1, storage_service)
    api.init_api()
    api.run()


def email_service_thread(email_manager_thread: es.EmailManager, storage_thread: ss.StorageService):
    print("Email Thread Activated")
    email_service_t2 = es.EmailService(storage_thread.get_email(), storage_thread.get_password(), storage_thread.get_imap(), storage_thread)
    fcm_service = push_notification_service
    fcm_service.init_service(keyPath)
    while True:
        print("new cycle")
        time.sleep(5)
        new_email, message = email_service_t2.get_emails()
        if new_email:
            print('new email arrived')
            email_manager_thread.set_unread_message(new_email)
            # tokens = storage.get_user_tokens()
            # print(tokens)
            fcm_service.send_broadcast_notification('alert', message)


storage = ss.StorageService()
email_manager = es.EmailManager()
storage.register_new_email('C01')
if storage.init_storage():
    # t1 = Thread(target=api_thread, args=(email_manager, storage,))
    t2 = Thread(target=email_service_thread, args=(email_manager, storage, ))
    # t1.start()
    t2.start()
