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


class BaseSearch(metaclass=abc.ABCMeta):
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
    """ThePirateBay search engine.

    Search on any of the pirate bay proxies or thepiratebay itself if
    available. Extract torrents, description and return it tabulated and ready
    to be printed
    """

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
    """KickAssTorrents search engine.

    Search on any of the pirate bay proxies or thepiratebay itself if
    available. Extract torrents, description and return it tabulated and ready
    to be printed
    """

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


def get_from_short(shortener, search_res):
    """Get new search res from shortened urls."""
    for elem in search_res:
        yield elem[:-1] + (get_short(shortener, elem[-1]),)


def main():
    """Search in multiple torrent sites.

    Usage: katcr [options] [interactive options] <SEARCH_TERM>

    Currently available search engines:

    - Katcr
    - ThePirateBay

    Options:
        -e --search-engine=<SearchEngine>  Torrent search engine to use
                                           [default: Any].
        -p --pages=<PAGES_NUM>             Number of pages to lookup
                                           [default: 1]
        -d --disable-shortener             Disable url shortener
        -s --sortener=<SHORTENER_URL>      Use given magnet shortener to
                                           prettify urls.
                                           [default: http://www.shortmag.net]

    Interactive Options:
        -i --interactive                   Enable interactive mode
        -o --open                          Launch with default torrent app
                                           in interactive mode [default: True]
        -h --help                          Show this help screen
        -d --debug                         Enable debug mode
    """
    opt = docopt(main.__doc__, version="0.0.1")

    if opt['-d']:
        logging.basicConfig(level=logging.DEBUG)

    search_res = list(globals()[opt['--plugin']]().search(
        opt["<SEARCH_TERM>"], int(opt.get("--pages"))))

    if opt['--enable-shortener']:
        search_res = list(get_from_short(opt['--shortener'], search_res))

    if not search_res:
        return

    if not opt['--interactive']:
        lengths = [max(len(a[pos]) for a in search_res)
                   for pos in range(0, len(search_res[0]))]
        return tableprint.table(search_res, ['Description', 'Size', 'Link'],
                                width=lengths)
    res = {a[:Terminal().width - 20]: b for a, b in search_res}
    result = res[prompt([List('Link', message="",
                              choices=res.keys())])['Link']]

    if opt['--open']:
        return subprocess.check_call(['xdg-open', result])

    print(result)
