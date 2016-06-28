#!/usr/bin/env python3.5
"""
Easy-as-it-gets python3.5 library to search magnets
in kickasstorrents (kat.cr)

Usage:
    katcr --search=<SEARCH_TERM> --pages=<PAGES_NUM> --type="magnet"

Options:
    --search=<SEARCH_TERM>   Search term(s)
    --pages=<PAGES_NUM>      Number of pages to lookup
    --type=<magnet|torrent>  Type

Examples:
    katcr --search "Search terms" --pages 3
    katcr --search "Search terms" --pages 1
    katcr --search "Search terms" --pages 1 --type=magnet
    katcr --search "Search terms" --pages 1 --type=torrent
    katcr --pages 1
"""

import re
import urllib
from docopt import docopt
import asyncio
import aiohttp

TYPES = {
    'magnet': re.compile(r'\"magnet:\?xt=urn:(.+?)\"'),
    'torrent': re.compile(r'\"//torcache.net(.+?)\"')}


async def search_magnets(query, page, type_):
    """
        Coroutine that searches in kat.cr and returns
        all links

        This works by simple applying a regular expression
        to the page HTML (either for magnet or torrent).
    """

    def parse_url(url):
        """
            Parse url, either a magnet or a normal url.
            Returns the query string and the torrent title

            returns url, torrenttitle
        """
        url = urllib.parse.urlparse(url)
        query = urllib.parse.parse_qs(url.query)
        query_ = query.get('dn', query.get('title', ''))[0]
        if url.scheme == "magnet":
            return "magnet:xt={}".format(query['xt'][0]), query_
        return "http://{}{}{}".format(*url[0:3]), query_

    with aiohttp.ClientSession() as session:
        url = 'https://kat.cr/usearch/{}/{}/'.format(query, page)
        async with session.get(url) as response:
            assert response.status == 200
            iter_ = TYPES[type_].finditer(
                await response.text(), re.IGNORECASE)
            return [parse_url(url.group(0)[1:-1]) for url in iter_]


def execute_search(query, pagelen=1, type_="magnet"):
    """
        Simple search manager, runs loop and gets all
        the results back.

        Be careful with pagelength as I'm not
        implementing proper page handling or groups,
        so all the pages are going to be queried at
        the same time

    """
    tasks = []
    loop = asyncio.get_event_loop()

    for page in range(0, pagelen):
        future = asyncio.ensure_future(
            search_magnets(query, page + 1, type_))
        tasks.append(future)

    loop.run_until_complete(asyncio.wait(tasks))

    for task in tasks:
        for magnet in task.result():
            yield magnet


def main():
    """
        Entry point
    """
    opts = docopt(__doc__, version="0.0.1")
    opts = (opts["--search"], int(opts["--pages"]), opts['--type'])

    for (url, qst) in execute_search(*opts):
        print("{} - {}".format(url, qst))
