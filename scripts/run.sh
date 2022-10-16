export SECRET_KEY=dfc5e53d46f7038b955ccbae977fe657e4da15cf8ab444c1be200030ab4d62e0
export MAIL_NAME="Your Name"
export MAIL_PASSWORD="MAIL_PASSWORD"
export MAIL_HOST="MAIL_HOST"
export MAIL_PORT="MAIL_PORT"
export MAIL_RECEIVER="MAIL_RECEIVER"
uvicorn app:app  --host 0.0.0.0  --port 8000  \
 --log-config configs/logs.ini