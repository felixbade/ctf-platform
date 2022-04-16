import os

def env_or_exit(name):
    value = os.environ.get(name)
    if not value:
        exit('{} is not set'.format(name))
    return value

class Config:
    SECRET_KEY = env_or_exit('SECRET_KEY')
    TELEGRAM_TOKEN = env_or_exit('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = env_or_exit('TELEGRAM_CHAT_ID')

    SQLALCHEMY_DATABASE_URI = env_or_exit('DB_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
