import pandas as pd


class StorageService:
    file_path_config = "ams_server_config.json"
    file_path_users = "users.json"
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
        for user in users.keys():
            tokens.append(user.token)

        return tokens
