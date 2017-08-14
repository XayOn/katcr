#!/usr/bin/env python3.5
"""Easy async python3.5 library to search magnets."""

import re
import urllib
import asyncio
import itertools
from inquirer import List, prompt
from docopt import docopt
from blessings import Terminal
from tabulate import tabulate
import aiohttp

TYPES = {'magnet': re.compile(r'\"magnet:\?xt=urn:(.+?)\"'),
         'torrent': re.compile(r'\"//torcache.net(.+?)\"')}


async def search_magnets(query, page, type_):
    """Return all links found in a single KAT page.

    This works by simple applying a regular expression to the page HTML
    (either for magnet or torrent).
    """
    def parse_url(url):
        """Parse url, either a magnet or a normal url.

        Returns the query string and the torrent title
        """
        url = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(url.query)
        query_ = query.get('dn', query.get('title', ''))[0]
        if url.scheme == "magnet":
            return "magnet:?xt={}".format(query['xt'][0]), query_
        return "http://{}{}{}".format(*url[0:3]), query_

    with aiohttp.ClientSession() as session:
        url = 'https://thekat.info/usearch/{}/{}/'.format(query, page)
        async with session.get(url) as response:
            assert response.status == 200
            iter_ = TYPES[type_].finditer(
                await response.text(), re.IGNORECASE)
            return [parse_url(url.group(0)[1:-1]) for url in iter_]


def search(query, pagelen=1, type_="magnet"):
    """Manage complete search for specified pages."""
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(search_magnets(query, page + 1, type_))
             for page in range(0, pagelen)]
    loop.run_until_complete(asyncio.wait(tasks))
    return itertools.chain(*(a.result() for a in tasks))


def main():
    """Search in KickAssTorrents.

    Usage: katcr [options]

    Options:
        --search=<SEARCH_TERM>   Search term(s)
        --pages=<PAGES_NUM>      Number of pages to lookup
        --type=<magnet|torrent>  Preferred magnet type to look for
        -i --interactive         Enable interactive menu
        -h --help                Show this screen
    """
    opt = docopt(main.__doc__, version="0.0.1")
    search_res = search(opt["--search"], int(opt["--pages"]), opt['--type'])
    if not opt['--interactive']:
        return print(tabulate(search_res))
    results = {b[:Terminal().width - 4]: a for a, b in search_res}
    print(results[prompt([List('Torrent', message="Choose",
                               choices=results.keys())])['Torrent']])
