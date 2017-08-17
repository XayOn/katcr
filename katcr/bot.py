#!/usr/bin/env python3.5
"""Telegram bot to query KickassTorrents."""

import gc
from katcr import Katcr
from docopt import docopt
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton


class KATBot(telepot.Bot):
    """KAT.cr search bot, looks only for the first page."""

    def __init__(self, token):
        """Initialize of KATBot."""
        super().__init__(token)
        self.katcr = Katcr()
        self.torrent_by_name_dict = {}

    # pylint: disable=too-few-public-methods
    def on_chat_message(self, msg):
        """Answer only chat messages."""
        if msg['text'] == "/start":
            return
        _, _, chat_id = telepot.glance(msg)
        self.sendMessage(chat_id, "Results for: {}".format(msg['text']))
        keys = []
        for key, value in self.katcr.search(msg['text'], 1):
            self.torrent_by_name_dict[key[:63]] = value
            keys.append([
                InlineKeyboardButton(text=key, callback_data=key[:63])])
        keyboard = InlineKeyboardMarkup(inline_keyboard=keys)
        self.sendMessage(chat_id, "Results for: {}".format(msg['text']),
                         reply_markup=keyboard, parse_mode="html")
        gc.collect()

    def on_callback_query(self, msg):
        """Get the button data."""
        _, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        self.sendMessage(from_id, self.torrent_by_name_dict[query_data])
        gc.collect()


def main():
    """Run telegram bot.

    Usage: katcr_bot [options]

    Options:
        --token=<BOT_TOKEN> Telegram bot token
    """
    bot = KATBot(docopt(main.__doc__, version="0.0.1")["--token"])
    MessageLoop(bot).run_forever()
