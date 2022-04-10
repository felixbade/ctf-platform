SCRIPT_DIR=$(dirname "${BASH_SOURCE[0]}")
cd $SCRIPT_DIR
venv/bin/gunicorn ctf_platform:app
