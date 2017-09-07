#!/usr/bin/env python3
"""Python library and CLI to search in multiple torrent sources.

Uses torrentmirror to get the first open mirror for any of the
supported sites.

Currently supported sites:

- ThePirateBay
- KickAssTorrents
"""

from contextlib import suppress
import abc
import itertools
import logging
import re
import subprocess

from blessings import Terminal
from docopt import docopt
from inquirer import List, prompt

from requests import Session
import requests

import robobrowser
import tableprint
import torrentmirror


class BaseSearch:
    """Base Search."""

    def __init__(self):
        """Initialize browser instance."""
        session = Session()
        session.verify = False
        self.browser = robobrowser.RoboBrowser(
            session=session, parser='html.parser', timeout=50)

    @abc.abstractproperty
    def url(self):
        """Search on given url by default."""

    @abc.abstractproperty
    def proxy_name(self):
        """Proxy name to use from torrentmirror."""

    @abc.abstractproperty
    def url_format(self):
        """Url formatter to add to base_url."""

    @abc.abstractmethod
    def get_torrents(self):
        """Return a list of torrents."""

    def search_magnets(self, query: str, page: int):
        """Return the list of magnets from a specific page."""
        proxies = torrentmirror.get_proxies()[self.proxy_name]
        proxies.insert(0, [self.url, None])
        for site, _ in proxies:
            with suppress(requests.exceptions.ReadTimeout, AssertionError):
                http = '' if site.startswith('http') else 'http://'
                self.browser.open(self.url_format.format(
                    http, site, query, page))
                torrents = self.get_torrents()
                assert torrents
                return torrents

    def search(self, query: str, pagelen: int = 1):
        """Manage complete search for specified pages."""
        return itertools.chain(*(self.search_magnets(query, page + 1)
                                 for page in range(0, pagelen)))


class ThePirateBay(BaseSearch):
    """Katcr main class."""

    proxy_name = 'The Pirate Bay'
    url_format = '{}{}/search/{}/{}/99'
    url = 'https://thepiratebay.org/'

    @staticmethod
    def tabulate(link):
        """Make a given a href link parsed on bs4 printable."""
        return (link.parent.find(class_='detName').text,
                link.parent.find(class_='detDesc').text,
                link['href'])

    def get_torrents(self):
        """Return a list of torrents, printable."""
        # pylint: disable=not-callable
        torrents = self.browser.find_all(
            'a', title='Download this torrent using magnet')
        return [self.tabulate(torrent) for torrent in torrents]


class Katcr(BaseSearch):
    """Katcr main class."""

    proxy_name = 'Kickass Torrents'
    url_format = '{}{}/search.php?q={}&p={}'
    url = 'https://kat.cd'

    @staticmethod
    def tabulate(link):
        """Make a given a href link parsed on bs4 printable."""
        magnet = link.find('a', title='Torrent magnet link')
        return (link.find(class_='cellMainLink').text,
                link.find_all('td')[1].text,
                magnet['href'])

    def get_torrents(self):
        """Return a list of torrents, printable."""
        # pylint: disable=not-callable
        torrents = self.browser.find_all(id=re.compile(
            'torrent_latest_torrents(.*)'))
        return [self.tabulate(torrent) for torrent in torrents]


def get_short(where, what):
    """Get magnet short link."""
    return '{}/{}'.format(
        where, requests.post(where, data={'magnet': what}).text)


def main():
    """Search in multiple torrent sites.

    Usage: katcr [options] <SEARCH_TERM>

    Options:
        --search=<SEARCH_TERM>             Search term(s)
        --pages=<PAGES_NUM>                Number of pages to lookup
        -i --interactive                   Enable interactive menu
        -p --plugin=<Katcr|ThePirateBay>   Download method [default: Katcr]
        --enable-shortener                 Enable url shortener
        -s --sortener=<SHORTENER_URL>      Use given magnet shortener
                                           [default: shortmag.net]
        -h --help                          Show this screen
        -o --open                          Launch with default torrent app
        -d                                 Debug mode.
    """
    opt = docopt(main.__doc__, version="0.0.1")

    if opt['-d']:
        logging.basicConfig(level=logging.DEBUG)

    search_res = list(globals()[opt['--plugin']]().search(
        opt["<SEARCH_TERM>"], int(opt.get("--pages") or 1)))

    if opt['--enable-shortener']:
        def get_from_short(search_res):
            """Get new search res from shortened urls."""
            for elem in search_res:
                yield elem[:-1] + (get_short(opt['--sortener'], elem[-1]),)

        search_res = list(get_from_short(search_res))

    if not search_res:
        return

    lengths = [max(len(a[pos]) for a in search_res)
               for pos in range(0, len(search_res[0]))]

    if not opt['--interactive']:
        return tableprint.table(search_res, ['Description', 'Size', 'Link'],
                                width=lengths)

    results = {a[:Terminal().width - 4]: b for a, b in search_res}
    result = results[prompt([List('Torrent', message="Choose",
                                  choices=results.keys())])['Torrent']]

    if opt['--open']:
        return subprocess.check_call(['xdg-open', result])
