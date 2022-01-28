from flask import Flask, request
from flask_restful import Resource, Api, reqparse
import pandas as pd
from main import get_unread_message, set_unread_message
import ast


class AppAPI:

    def __init__(self):
        self.app = Flask('ReplyAMS')
        self.api = Api(self.app)

    def init_api(self):
        @self.app.route('/message')
        def get_message():
            return get_unread_message(), 200

        @self.app.route('/message/reset', method='POST')
        def reset_message():
            set_unread_message(0)

    def run(self):
        self.app.run()


