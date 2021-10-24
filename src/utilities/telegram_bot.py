import os
import apprise
from config import config


class Bot:

    def __init__(self):
        c = config.Config()
        association_configs = c.get_associations_configs()
        self.apobj = apprise.Apprise()
        self.token = os.environ.get("TELEGRAM_BOT_TOKEN")
        for association, a_config in association_configs.items():
            self.apobj.add("tgram://%s/%s" %
                           (self.token, a_config["chat_id"]), tag=association)

    def notify(self, title, message, association):
        self.apobj.notify(
            body=message,
            title=title,
            tag=association
        )
