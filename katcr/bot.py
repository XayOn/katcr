#!/usr/bin/env python3.5
"""Telegram bot to query KickassTorrents."""
import re
from katcr import search
from docopt import docopt
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import urllib
class KATBot(telepot.Bot):
    """KAT.cr search bot, looks only for the first page."""

    # pylint: disable=too-few-public-methods
    def on_chat_message(self, msg):
        """Answer only chat messages."""
        if msg['text'] == "/start":
            return
        _, _, chat_id = telepot.glance(msg)
        self.sendMessage(chat_id, "Results for: {}".format(msg['text']))
        key = []
        for a,b in search(msg['text'], 1):                       
            key.append([InlineKeyboardButton(text=a, callback_data=a[:63])])
        keyboard = InlineKeyboardMarkup(inline_keyboard=key)
        self.sendMessage(chat_id,  "Results for: {}".format(msg['text']), reply_markup=keyboard, parse_mode="html")

    def on_callback_query(self,msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        name = re.search(r"-(.*)-",query_data).group(1)
        for a,b in search(name, 1):
            self.sendMessage(from_id, b)

def main():
    """Run telegram bot.

    Usage: katcr_bot [options]

    Options:
        --token=<BOT_TOKEN> Telegram bot token
    """
    bot = KATBot(docopt(main.__doc__, version="0.0.1")["--token"])
    MessageLoop(bot).run_forever()
