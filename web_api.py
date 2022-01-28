from flask import Flask
from flask_restful import Resource, Api, reqparse
import pandas as pd
from main import get_unread_message, set_unread_message
import ast


class Message(Resource):
    @staticmethod
    def get():
        set_unread_message(0)
        return str(get_unread_message()), 200


class AppAPI:

    def __init__(self):
        self.app = Flask('ReplyAMS')
        self.api = Api(self.app)

    def init_api(self):
        self.api.add_resource(Message, '/message')

    def run(self):
        self.app.run()


