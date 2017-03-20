#!/usr/bin/env python3.5
"""
Telegram bot to query KickassTorrents

Usage:
    katcr_bot --token <BOT_TOKEN>

Options:
    --token=<BOT_TOKEN> Telegram bot token

Examples:
    katcr_bot --token 123123:123123
"""

import asyncio
import telepot
from katcr import search_magnets
from docopt import docopt
import telepot.async


class KATBot(telepot.async.Bot):
    """
        KAT.cr search bot, looks only for the first
        page.
    """
    loop = False
    async def on_chat_message(self, msg):
        """ Answer only chat messages """
        _, _, chat_id = telepot.glance(msg)
        if msg['text'] == "/start":
            return
        magnets = search_magnets(msg['text'], 1, "torrent")
        await self.sendMessage(chat_id, "Results for: {}".format(msg['text']))

        for magnet in await magnets:
            response = "<a href=\"{}\">{}</a>".format(*magnet)
            await self.sendMessage(chat_id, response, parse_mode="html")


def main():
    """
        Starts bot.
    """
    opts = docopt(__doc__, version="0.0.1")
    bot = KATBot(opts["--token"])
    loop = asyncio.get_event_loop()
    bot.loop = loop
    loop.create_task(bot.message_loop())
    loop.run_forever()
