import os
import apprise

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


class Bot:

    def __init__(self):
        self.apobj = apprise.Apprise()
        token = TELEGRAM_BOT_TOKEN
        chat_id = TELEGRAM_CHAT_ID
        self.apobj.add("tgram://%s/%s" % (token, chat_id))

    def notify(self, title, message):
        self.apobj.notify(
            body=message,
            title=title,
        )
