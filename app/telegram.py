import requests

from app import app

api_prefix = 'https://api.telegram.org/bot' + app.config['TELEGRAM_TOKEN']

def send_message(content):
    # currently no error handling
    requests.post(api_prefix + '/sendMessage', data={
        'chat_id': app.config['TELEGRAM_CHAT_ID'],
        'text': content,
        'parse_mode': 'MarkdownV2',
    })

def escapeMarkdown(content):
    characters = '\\*_`}{][)(#+-.!|'
    for c in characters:
        content = content.replace(c, '\\' + c)
    return content