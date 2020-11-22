#!/usr/bin/env python3
"""Python library and CLI to search in multiple torrent sources.

Uses torrentmirror to get the first open mirror for any of the
supported sites.
"""

import os
import xdg
import warnings
import shutil
import subprocess
import asyncio
import urllib.parse
from configparser import ConfigParser

import cutie
import aiohttp
from cleo import Command
from cleo import Application
from pygogo import Gogo

from . import engines
from .bot import BotHandler
from .engines.base import BaseSearch

try:
    from torrentstream import stream_torrent
except ImportError:
    warnings.warn("Could not import torrentstream, streaming is disabled")

    def stream_torrent(torrent):
        """Stream torrents"""


CONFIG_FILE = xdg.XDG_CONFIG_HOME / 'katcr.ini'
DEFAULT_ENGINES = ['Katcr', 'ThePirateBay']
MAX_SIZE = shutil.get_terminal_size().columns - 20


class Result:
    """Represents a result, results are shortened and cleanly printable."""
    session = None

    def __init__(self, result, interactive):
        self.result = result
        self.is_interactive = interactive

    def __repr__(self):
        """Get new search res from shortened urls and adjust term output."""
        if self.is_interactive:
            return self.result[0][:MAX_SIZE]
        return ' | '.join(self.result)

    def open(self):
        """Open with xdg-open"""
        return subprocess.check_call(['xdg-open', self.result[-1]])


class SearcherCommand(Command):
    async def setup_sessions(self):
        """Setup client session as singleton"""
        self.logger = Gogo(__name__, verbose=self.io.verbosity).logger
        BaseSearch.session = aiohttp.ClientSession(raise_for_status=True)
        BaseSearch.logger = self.logger
        BaseSearch.config = ConfigParser()
        BaseSearch.config.read(CONFIG_FILE)
        Result.session = BaseSearch.session

    @staticmethod
    async def teardown_sessions():
        BaseSearch.session.close()

    async def search(self, enames, search_term, pages, is_interactive, stream):
        """Search on all engines."""

        eng = (getattr(engines, a)() for a in enames)
        search_term = urllib.parse.quote(search_term)
        await self.setup_sessions()
        search_res = []
        for engine in eng:
            engine_result = await engine.search(search_term, int(pages))
            search_res.extend(
                (Result(a, is_interactive) for a in engine_result))

        await self.teardown_sessions()
        if not search_res:
            return

        if not is_interactive:
            self.render_table(['Description', 'Link'],
                              [a.result for a in search_res])
            return search_res

        result = search_res[cutie.select(search_res, selected_prefix="[☛]")]
        if not result.result[1].startswith('magnet'):
            # Allow jackett redirect to magnet uri.
            resp = await BaseSearch.session.get(result.result[1],
                                                allow_redirects=False)
            result.result[1] = resp.headers['Location']

        if self.option('open'):
            return result.open()
        if stream:
            await stream_torrent(result.result[1])
        self.line(result.result[1])


class BotCommand(SearcherCommand):
    """Launch bot

    bot

        {--token=? : Bot token. Ask BotFather}
    """
    async def run_bot(self):
        await self.setup_sessions()
        if 'bot' not in BaseSearch.config.sections():
            BaseSearch.config.add_section('bot')

        token = os.getenv(
            'KATCR_TOKEN',
            BaseSearch.config['bot'].get('token', self.option('token')))

        await BotHandler(self).start(token)
        await self.teardown_sessions()

    def handle(self):
        return asyncio.run(self.run_bot())


class CLICommand(SearcherCommand):
    """Search in multiple torrent sites.

    search

        {search : Search term}

        {--pages=1 : Pages to search on search engines}
        {--engines=Katcr,ThePirateBay,Eztv,NyaaSi,Skytorrents : Engines}
        {--nointeractive=? : Print resuls directly to stdout}
        {--open=? : Open selected magnet with xdg-open}
        {--stream=? : Stream with torrentstream, uses PLAYER env or xdg-open }

    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = None

    def handle(self):
        """Handler."""
        engine_names = self.option('engines').split(',')
        is_interactive = not self.option('nointeractive')

        self.line(f'<info>Starting search on {", ".join(engine_names)}</info>')

        coro = self.search(engine_names, self.argument('search'),
                           self.option('pages'), is_interactive,
                           self.option('stream'))
        return asyncio.run(coro)


def main():
    """Main entry point"""
    application = Application()
    application.add(CLICommand())
    application.add(BotCommand())
    application.run()
