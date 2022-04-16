import requests

from app import app

class Telegram:
    def __init__(self):
        self.api = 'https://api.telegram.org/bot' + app.config['TELEGRAM_TOKEN']

    def send_message(self, content):
        # currently no error handling
        requests.post(self.api + '/sendMessage', data={
            'chat_id': app.config['TELEGRAM_CHAT_ID'],
            'text': content,
            'parse_mode': 'MarkdownV2',
        })

TG = Telegram()
