# ctf-platform

## Installation
- `python3 -m venv venv`
- `. venv/bin/activate`
- `pip install -r requirements`
- add a secure secret key to `.env`
- add `TELEGRAM_CHAT_ID` and `TELEGRAM_TOKEN`
- create an admin user with `flask create-admin-user`

## Running

### Development
`flask run`

### Production
`./run-production.sh`
