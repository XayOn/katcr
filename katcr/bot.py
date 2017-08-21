#!/usr/bin/env python3.5
"""Telegram bot to query KickassTorrents."""

from katcr import Katcr
from docopt import docopt
import requests
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


class KATBot(telepot.Bot):
    """KAT.cr search bot, looks only for the first page."""

    def __init__(self, token):
        """Initialize of KATBot."""
        super().__init__(token)
        self.katcr = Katcr()
        self.responses = {}

    # pylint: disable=too-few-public-methods
    def on_chat_message(self, msg):
        """Answer only chat messages."""
        if msg['text'] == "/start":
            return

        chat_id = telepot.glance(msg)[2]
        res = tuple(self.katcr.search(msg['text'], 1))

        keyboard = InlineKeyboardMarkup(inline_keyboard=list(
            [InlineKeyboardButton(text=k, callback_data=str(r))]
            for r, (k, _) in enumerate(res)))

        self.responses[chat_id] = {r: (k, v) for r, (k, v) in enumerate(res)}
        self.sendMessage(chat_id, "Results for: {}".format(msg['text']),
                         reply_markup=keyboard, parse_mode="html")

    def on_callback_query(self, msg):
        """Get the button data."""
        _, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        key, value = self.responses[from_id][int(query_data)]
        res = requests.get('http://mgnet.me/api/create?m={}'.format(value))
        url = res.json()['shorturl']
        self.sendMessage(from_id, "<a href=\"{}\">{}</a>".format(url, key),
                         parse_mode="html")


def main():
    """Run telegram bot.

    Usage: katcr_bot [options]

    Options:
        --token=<BOT_TOKEN> Telegram bot token
    """
    bot = KATBot(docopt(main.__doc__, version="0.0.1")["--token"])
    MessageLoop(bot).run_forever()
