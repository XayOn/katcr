#!/usr/bin/env python3.5
"""Telegram bot to query KickassTorrents."""

from katcr import search
from docopt import docopt
import telepot
from telepot.loop import MessageLoop


class KATBot(telepot.Bot):
    """KAT.cr search bot, looks only for the first page."""

    # pylint: disable=too-few-public-methods
    def on_chat_message(self, msg):
        """Answer only chat messages."""
        if msg['text'] == "/start":
            return
        _, _, chat_id = telepot.glance(msg)
        self.sendMessage(chat_id, "Results for: {}".format(msg['text']))
        for magnet in search(msg['text'], 1):
            self.sendMessage(chat_id, "<a href=\"{}\">{}</a>".format(*magnet),
                             parse_mode="html")


def main():
    """Run telegram bot.

    Usage: katcr_bot [options]

    Options:
        --token=<BOT_TOKEN> Telegram bot token
    """
    bot = KATBot(docopt(main.__doc__, version="0.0.1")["--token"])
    MessageLoop(bot).run_forever()
