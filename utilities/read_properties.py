import configparser

config = configparser.RawConfigParser()
config.read(".\\configurations\\config.ini")

class Read_config():
    def __init__(self):
        self.config = configparser.RawConfigParser()

    @staticmethod
    def get_url():
        url = config.get("login info", "Url")
        return url

    @staticmethod
    def get_username():
        username = config.get("login info", "username")
        return username

    @staticmethod
    def get_password():
        password = config.get("login info", "password")
        return password

    @staticmethod
    def get_invalid_password():
        invalid_password = config.get("login info", "invalid_password")
        return invalid_password

    @staticmethod
    def get_invalid_username():
        invalid_username = config.get("login info", "invalid_username")
        return invalid_username