import base64
import json

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Resource, Api, reqparse
import pandas as pd
from email_service import EmailManager, EmailService
from storage_service import StorageService


class AppAPI:

    def __init__(self, email_manager: EmailManager, email_service: EmailService, info_storage: StorageService):
        self.app = Flask('ReplyAMS')
        CORS(self.app)
        self.api = Api(self.app)
        self.EmailManager = email_manager
        self.EmailService = email_service
        self.StorageService = info_storage

    def init_api(self):
        @self.app.route('/message')
        def get_message():
            new_email, body = self.EmailService.get_emails()
            if new_email:
                message = body
            else:
                message = 'There are not new e-mails'
            response = self.api.make_response(json.dumps({'new_email': new_email, 'message': message}), code=200)
            response.headers['Content-Type'] = 'application/json'
            response.headers['Access-Control-Allow-Origin'] = '*'
            return response

        @self.app.route('/message/reset', methods=['POST'])
        def reset_message():
            data = request.json
            print(data)
            self.EmailManager.set_unread_message(False)

        @self.app.route('/users/new', methods=['POST'])
        def add_new_users():
            data = request.json
            print(data['name'])
            message, code = self.StorageService.add_new_user(data['name'], data['activate'], data['email'], str(base64.b64decode(data['token'])))
            return self.api.make_response(data=message, code=code)

    def run(self):
        self.app.run()


