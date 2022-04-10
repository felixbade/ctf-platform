source .env

HOST="$SSH_USER@$DOMAIN"

# https://stackoverflow.com/a/63438492
rsync -vhra . $HOST:$APP_DIR --include='**.gitignore' --exclude='/.git' --filter=':- .gitignore' --delete-after

COMMAND="cd $APP_DIR"
COMMAND="$COMMAND && venv/bin/pip install -r requirements.txt"
COMMAND="$COMMAND && venv/bin/flask db upgrade"
COMMAND="$COMMAND && pm2 startOrRestart ecosystem.config.js --update-env"

ssh -t $HOST "$COMMAND"