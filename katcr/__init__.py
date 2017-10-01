#!/usr/bin/env python3
"""Python library and CLI to search in multiple torrent sources.

Uses torrentmirror to get the first open mirror for any of the
supported sites.

Currently supported sites:

- ThePirateBay
- KickAssTorrents
"""

from contextlib import suppress
from pathlib import Path
import abc
import itertools
import re
import subprocess

from blessings import Terminal
from docopt import docopt
from inquirer import List
from inquirer import prompt
from pygogo import Gogo

from requests import Session
import requests

import robobrowser
import tableprint
import torrentmirror


class BaseSearch(metaclass=abc.ABCMeta):
    """Base Search."""

    def __init__(self, logger):
        """Initialize browser instance."""
        session = Session()
        session.verify = False
        self.logger = logger
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
        proxies = torrentmirror.get_proxies().get(self.proxy_name, [])
        proxies.insert(0, [self.url, None])
        for site, _ in proxies:
            self.logger.debug("Searching in %s", site)
            with suppress(requests.exceptions.ReadTimeout,
                          requests.exceptions.SSLError, AssertionError):
                http = '' if site.startswith('http') else 'http://'
                self.browser.open(self.url_format.format(
                    http, site, query, page))
                torrents = self.get_torrents()
                assert torrents
                self.logger.debug("Got torrents %s", torrents)
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


class NyaaSi(BaseSearch):
    """Nyaa.Si torrent search engine."""

    proxy_name = ''
    url = 'https://nyaa.si'
    url_format = '{}{}/?f=0&c=0_0&q={}&p={}'

    @staticmethod
    def tabulate(link):
        """Extract all information from each href."""
        row = link.parent.parent.parent
        cols = row.find_all('td')

        def _nocomments(where):
            return where != 'comments'

        name = ''.join((cols[1].find('a', class_=_nocomments).text.strip(),
                        ' ', cols[0].find('img')['alt'].strip()))
        return (name, cols[3].text.strip(), link.parent['href'])

    def get_torrents(self):
        """Return torrents."""
        # pylint: disable=not-callable
        links = self.browser.find_all(class_='fa-magnet')
        return [self.tabulate(link) for link in links]


class Skytorrents(BaseSearch):
    """Skytorrents.in torrent search engine."""

    proxy_name = ''
    url = 'https://skytorrents.in/'
    url_format = '{0}{1}search/all/ed/{3}/?l=en-us&q={2}'

    @staticmethod
    def tabulate(row):
        """Extract all information from each href."""
        with suppress(IndexError):
            cols = row.find_all('td')
            links = cols[0].find_all('a')
            return (links[0].text, cols[1].text, links[1]['href'])

    def get_torrents(self):
        """Return torrents."""
        # pylint: disable=not-callable
        return list(filter(
            None, [self.tabulate(l) for l in self.browser.find_all('tr')]))


class DigBt(BaseSearch):
    """Digbt DHT search engine."""

    proxy_name = ''
    url = 'https://digbt.org/'
    url_format = '{0}{1}search/{2}-relevance-{3}/'

    @staticmethod
    def tabulate(row):
        """Extract all information from each href."""
        with suppress(IndexError, TypeError):
            tail = row.find(class_='tail')
            return (row.find('div').find('a').text.strip(),
                    list(filter(lambda x: x, tail.text.split(' ')))[4].strip(),
                    tail.find('a')['href'].strip())

    def get_torrents(self):
        """Return torrents."""
        # pylint: disable=not-callable
        return list(filter(
            None, [self.tabulate(l) for l in self.browser.find_all('tr')]))


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


def limit_terminal_size(what, limit=-20):
    """Limit a string to current terminal size, plus limit."""
    return what[:Terminal().width + limit]


def get_shortener_from_opts(opt):
    """Return shortener with token if needed."""
    shortener = opt['--shortener'][0]
    token = opt.get('--token')
    if not token and opt.get('--token_file'):
        token = Path(opt.get('--token_file')).read_text()
    if token:
        shortener = shortener.format(token)
    return shortener


def search_in_engines(logger, engines, search_term, pages):
    """Search in engines."""
    search_res = None

    if engines == ["All"]:
        engines = ("Katcr", "ThePirateBay")

    for engine in engines:
        with suppress(TypeError):
            search_res = list(globals()[engine](logger).search(
                search_term, pages))
            if search_res:
                return search_res


def main():
    """Search in multiple torrent sites.

    Usage: katcr [options] [interactive options] <SEARCH_TERM>

    Currently available search engines:

    - Katcr
    - ThePirateBay
    - Nyaa
    - Skytorrents
    - Digbt

    Options:
        -e --search-engines=<SearchEngine>  Torrent search engine to use
                                            [default: All].
        -p --pages=<PAGES_NUM>              Number of pages to lookup
                                            [default: 1]
        -d --disable-shortener              Disable url shortener
        -s --shortener=<SHORTENER_URL>      Use given magnet shortener to
                                            prettify urls.
                                            [default: http://www.shortmag.net]
        -t --token=<SHORTENER_TOKEN>        Shortener token to use, if required
        -t --token_file=<S_TOKEN_FILE>      Shortener token file

    Interactive Options:
        -i --interactive                    Enable interactive mode
        -o --open                           Launch with default torrent app
                                            in interactive mode [default: True]
        -h --help                           Show this help screen
        -v --verbose                        Enable debug mode


    katcr  Copyright (C) 2017 David Francos Cuartero
    This program comes with ABSOLUTELY NO WARRANTY; This is free software, and
    you are welcome to redistribute it under certain conditions;
    """
    opt = docopt(main.__doc__, version="1.0.1")
    logger = Gogo(__name__, verbose=opt.get('--verbose')).logger

    search_res = search_in_engines(logger, opt['--search-engines'],
                                   opt["<SEARCH_TERM>"],
                                   int(opt.get("--pages")[0]))

    if not opt['--disable-shortener']:
        shortener = get_shortener_from_opts(opt)
        with suppress(TypeError):
            search_res = list(get_from_short(shortener, search_res))

    if not search_res:
        return

    if not opt['--interactive']:
        return tableprint.table(search_res, ['Description', 'Size', 'Link'],
                                width=[max(len(a[p]) for a in search_res)
                                       for p in range(0, len(search_res[0]))])

    res = {limit_terminal_size(a): b for a, _, b in search_res}
    result = res[prompt([List('Link', message="",
                              choices=res.keys())])['Link']]

    if opt['--open']:
        return subprocess.check_call(['xdg-open', result])
