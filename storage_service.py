import os

import pandas as pd


class StorageService:
    file_path_config = "ams_server_config.json"
    file_path_users = "users.json"
    file_path_history = "email_history.json"
    config = {}

    def init_storage(self):
        self.config = pd.read_json(self.file_path_config)
        if self.config is not None:
            return True
        else:
            return False

    def get_email(self):
        return self.config.email.user

    def get_password(self):
        return self.config.email.password

    def get_imap(self):
        return self.config.email.imap

    def get_server_key(self):
        return self.config.fcm.serverkey

    def get_user_tokens(self):
        users = pd.read_json(self.file_path_users)
        tokens = []
        for key in users.keys():
            user = users.loc(axis=1)[key]
            if bool(user['activate']) is True:
                tokens.append(user['token'])
        return tokens

    def add_new_user(self, name: str, activate: bool, email: str, token: str):
        try:
            users = pd.read_json(self.file_path_users)
            new_user = [name, activate, email, token]
            users[token] = new_user
            users.to_json(self.file_path_users)
            message = 'New user added successfully'
            return message, 200
        except pd.errors.ParserError:
            message = 'Error during the creation of a new user'
            return message, 500

    def register_new_email(self, email_id):
        email_history = {}
        if not os.path.exists(self.file_path_history):
            email_history = {
                email_id: {
                    "email_id": email_id,
                    "expired": 3
                }
            }
            email_df: pd.DataFrame = pd.DataFrame(email_history)
            email_df.to_json(self.file_path_history)
            return 3
        else:
            email_history = pd.read_json(self.file_path_history)
            email_df = email_history.loc(axis=1)[email_id]
            if email_df['expired'] > 0:
                email_history.at['expired', email_id] = email_df['expired'] - 1
            email_history.to_json(self.file_path_history)


