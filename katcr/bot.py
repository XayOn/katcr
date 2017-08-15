#!/usr/bin/env python3.5
"""Telegram bot to query KickassTorrents."""

import asyncio
from katcr import search_magnets
from docopt import docopt
import telepot
import telepot.aio


class KATBot(telepot.aio.Bot):
    """KAT.cr search bot, looks only for the first page."""

    # pylint: disable=too-few-public-methods

    async def on_chat_message(self, msg):
        """Answer only chat messages."""
        if msg['text'] == "/start":
            return
        _, _, chat_id = telepot.glance(msg)
        await self.sendMessage(chat_id, "Results for: {}".format(msg['text']))
        for magnet in await search_magnets(msg['text'], 1):
            await self.sendMessage(
                chat_id, "<a href=\"{}\">{}</a>".format(*magnet),
                parse_mode="html")


def main():
    """Run telegram bot.

    Usage: katcr_bot [options]

    Options:
        --token=<BOT_TOKEN> Telegram bot token
    """
    token = docopt(__doc__, version="0.0.1")["--token"]
    loop = asyncio.get_event_loop()
    loop.create_task(KATBot(token).message_loop())
    loop.run_forever()
