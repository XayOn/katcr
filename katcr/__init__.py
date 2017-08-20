#!/usr/bin/env python3.5
"""Easy async python3.5 library to search magnets."""

import re
import itertools
from inquirer import List, prompt
from docopt import docopt
from blessings import Terminal
from tabulate import tabulate
import robobrowser
import torrentmirror


class BaseSearch:
    """Base Search."""

    def __init__(self):
        """Initialize browser instance."""
        self.browser = robobrowser.RoboBrowser(parser='html.parser')

    def search_magnets(self, query: str, page: int):
        """Return the list of magnets from a specific page."""
        raise NotImplementedError()

    def search(self, query: str, pagelen: int = 1):
        """Manage complete search for specified pages."""
        return itertools.chain(*(self.search_magnets(query, page + 1)
                                 for page in range(0, pagelen)))


class ThePirateBay(BaseSearch):
    """Katcr main class."""

    def search_magnets(self, query: str, page: int):
        """Return all links found in a single KAT page.

        This works by simple applying a regular expression to the page HTML
        (either for magnet or torrent).
        """
        def make_printable(link):
            """Make a given a href link parsed on bs4 printable."""
            print(link.parent)
            name = link.parent.find(class_='detName').text
            desc = link.parent.find(class_='detDesc').text
            return ('{} - {}'.format(name, desc), link['href'])

        # pylint: disable=not-callable
        base_url = torrentmirror.get_proxies()['The Pirate Bay'][0][0]
        http = '' if 'http' in base_url else 'http://'
        self.browser.open('{}{}/search/{}/{}/99'.format(http, base_url, query,
                                                        page))
        torrents = self.browser.find_all(
            'a', title='Download this torrent using magnet')

        return [make_printable(torrent) for torrent in torrents]


class Katcr(BaseSearch):
    """Katcr main class."""

    def search_magnets(self, query: str, page: int):
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
        self.browser.open('{}{}/search.php?q={}&p={}'.format(http,
                                                             base_url,
                                                             query,
                                                             page))
        torrents = self.browser.find_all(id=re.compile(
            'torrent_latest_torrents(.*)'))
        return [make_printable(torrent) for torrent in torrents]


def main():
    """Search in KickAssTorrents.

    Usage: katcr [options]

    Options:
        --search=<SEARCH_TERM>   Search term(s)
        --pages=<PAGES_NUM>      Number of pages to lookup
        -i --interactive         Enable interactive menu
        -p --plugin=<PLUGIN>     Plugin to use for search <Katcr|ThePirateBay>
        -h --help                Show this screen
        -o --open                Use xdg-open to launch the default torrent app
    """
    opt = docopt(main.__doc__, version="0.0.1")
    search_res = globals()[opt['--plugin']]().search(
        opt["--search"], int(opt["--pages"]))
    if not opt['--interactive']:
        return print(tabulate(search_res))
    results = {a[:Terminal().width - 4]: b for a, b in search_res}
    print(results[prompt([List('Torrent', message="Choose",
                               choices=results.keys())])['Torrent']])
