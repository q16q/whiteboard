# whiteboard
source code repo for https://t.me/customwhiteboardbot \
no telemetry, no logging
## installation
1. install [python](https://python.org)
2. install dependencies:
```
pip install python-dotenv python-telegram-bot python-dateutil
```
3. create an .env file with contents:
```
TOKEN=(telegram bot token)
CHAT_ID=(telegram chat id)
```
4. run bot with
```
python main.py
```
## usage
just send the message and it will be automatically posted to the channel
