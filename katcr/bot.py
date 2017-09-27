#!/usr/bin/env python3.5
"""Telegram bot to query KickassTorrents."""

from pathlib import Path

from katcr import Katcr
from katcr import ThePirateBay
from katcr import get_short

from docopt import docopt
from pygogo import Gogo
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
import telepot


class KATBot(telepot.Bot):
    """KAT.cr search bot, looks only for the first page."""

    def __init__(self, opts):
        """Initialize of KATBot."""
        token = opts.get('--token')
        if not token:
            token = Path(opts.get('--token-file')).read_text().strip()
        super().__init__(token)
        self.logger = Gogo(__name__, verbose=True).logger
        self.logger.debug("Starting service.")
        self.shortener = opts['--shortener']
        self.katcr = Katcr(self.logger)
        self.thepiratebay = ThePirateBay(self.logger)
        self.responses = {}

    # pylint: disable=too-few-public-methods
    def on_chat_message(self, msg):
        """Answer only chat messages."""
        if msg['text'] == "/start":
            return

        chat_id = telepot.glance(msg)[2]

        for engine in (self.katcr, self.thepiratebay):
            res = tuple(engine.search(msg['text'], 1))
            if res:
                break

        keyboard = InlineKeyboardMarkup(inline_keyboard=list(
            [InlineKeyboardButton(text=k, callback_data=str(r))]
            for r, (k, _, _) in enumerate(res)))

        self.responses[chat_id] = {r: (k, v) for r, (k, _, v)
                                   in enumerate(res)}
        self.sendMessage(chat_id, "Results for: {}".format(msg['text']),
                         reply_markup=keyboard, parse_mode="html")

    def on_callback_query(self, msg):
        """Get the button data."""
        _, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        key, value = self.responses[from_id][int(query_data)]
        href = "<a href=\"{}\">{}</a>".format(
            get_short(self.shortener, value), key)
        self.sendMessage(from_id, href, parse_mode="html")


def main():
    """Run telegram bot.

    Usage: katcr_bot [options]

    Options:
        --token=<BOT_TOKEN>             Telegram bot token
        --token-file=<FILE>             Telegram bot token file
        --shortener=<URL_SHORTENER>     Url shortener to use
                                        [default: http://shortmag.net]
    """
    bot = KATBot(docopt(main.__doc__, version="0.0.1"))
    MessageLoop(bot).run_forever()
