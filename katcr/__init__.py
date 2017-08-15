#!/usr/bin/env python3.5
"""Easy async python3.5 library to search magnets."""

import re
import asyncio
import itertools
from inquirer import List, prompt
from docopt import docopt
from blessings import Terminal
from tabulate import tabulate
import robobrowser
import torrentmirror


def search_magnets(query: str, page: int):
    """Return all links found in a single KAT page.

    This works by simple applying a regular expression to the page HTML
    (either for magnet or torrent).
    """
    def make_printable(link):
        """Make a given a href link parsed on bs4 printable."""
        name = link.find(class_='cellMainLink').text
        size = link.find_all('td')[1].text
        return ('{} - {}'.format(name, size),
                link.find('a', title='Torrent magnet link')['href'])

    # pylint: disable=not-callable
    base_url = torrentmirror.get_proxies()['Kickass Torrents'][0][0]
    http = '' if 'http' in base_url else 'http://'
    page = robobrowser.RoboBrowser()
    page.open('{}{}/search.php?q={}&p={}'.format(http, base_url, query, page))
    torrents = page.find_all(id=re.compile('torrent_latest_torrents(.*)'))
    return [make_printable(torrent) for torrent in torrents]


def search(query: str, pagelen: int = 1):
    """Manage complete search for specified pages."""
    return itertools.chain(*(search_magnets(query, page + 1)
                             for page in range(0, pagelen)))


def main():
    """Search in KickAssTorrents.

    Usage: katcr [options]

    Options:
        --search=<SEARCH_TERM>   Search term(s)
        --pages=<PAGES_NUM>      Number of pages to lookup
        -i --interactive         Enable interactive menu
        -h --help                Show this screen
    """
    opt = docopt(main.__doc__, version="0.0.1")
    search_res = search(opt["--search"], int(opt["--pages"]))
    if not opt['--interactive']:
        return print(tabulate(search_res))
    results = {a[:Terminal().width - 4]: b for a, b in search_res}
    print(results[prompt([List('Torrent', message="Choose",
                               choices=results.keys())])['Torrent']])
