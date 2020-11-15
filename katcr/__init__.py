#!/usr/bin/env python3
"""Python library and CLI to search in multiple torrent sources.

Uses torrentmirror to get the first open mirror for any of the
supported sites.
"""

from contextlib import suppress
from pathlib import Path
import functools
import os
import shutil
import subprocess

from cleo import Command
from cleo import Application
from pygogo import Gogo
import cutie
import requests

from . import engines

DEFAULT_ENGINES = ['Katcr', 'ThePirateBay']
MAX_SIZE = shutil.get_terminal_size().columns - 20


@functools.lru_cache()
def get_engine(name, session, logger):
    """Cached engine extraction by name.

    Passing the logger down.
    """
    if not hasattr(engines, name):
        raise RuntimeError('Wrong engine provided')
    return getattr(engines, name)(session, logger)


class Result:
    def __init__(self, session, result, shortener, token, interactive):
        self.result = result
        self.session = session
        if shortener:
            shortener = shortener.format(os.getenv('KATCR_TOKEN', token))
        self.shortener = shortener
        self.is_interactive = interactive

    def __repr__(self):
        """Get new search res from shortened urls and adjust term output."""
        if not self.shortener:
            if self.is_interactive:
                return ' | '.join((self.result[0][:MAX_SIZE], self.result[1]))
            return ' | '.join(self.result)
        clean = self.result[:-1]
        result = self.session.post(self.shortener, data={'magnet': clean})
        return ''.join(clean) + f'{self.shortener}/{result.text}'

    def open(self):
        return subprocess.check_call(['xdg-open', self.result[-1]])


class CLICommand(Command):
    """Search in multiple torrent sites.

    search

        {search : Search term}

        {--pages=1 : Pages to search on search engines}
        {--token=? : Token to use on URL shortener as AUTH}
        {--shortener=? : URL Shortener}
        {--engines=Katcr,ThePirateBay,NyaaSi,Skytorrents : Engines}

        {--interactive=? : Allow the user to choose a specific magnet}
        {--open=? : Open selected magnet with xdg-open}

    """

    def handle(self):
        """Handler."""
        logger = Gogo(__name__, verbose=self.io.verbosity).logger
        session = requests.Session()
        session.verify = None

        engine_names = self.option('engines').split(',') or DEFAULT_ENGINES
        engines = (get_engine(a, session, logger) for a in engine_names)

        shortener = self.option('shortener')
        token = self.option('token')
        is_interactive = self.option('interactive')
        search_term = self.argument('search')
        pages = self.option('pages')

        search_res = []

        self.line('<info>Starting search on {}</info>'.format(
            ', '.join(engine_names)))

        # progress = self.progress_bar(len(engine_names))

        for engine in engines:
            # progress.advance(0.9)
            engine_result = engine.search(search_term, int(pages))
            search_res.extend((Result(session, a, shortener, token,
                                      is_interactive) for a in engine_result))

        # progress.finish()

        if not search_res:
            return

        if not is_interactive:
            return self.render_table(['Description', 'Size', 'Link'],
                                     [a.result for a in search_res])

        result = search_res[cutie.select(search_res, selected_prefix="☛")]

        if self.option('open'):
            return result.open()


def main():
    """Main entry point"""
    application = Application()
    application.add(CLICommand())
    application.run()
