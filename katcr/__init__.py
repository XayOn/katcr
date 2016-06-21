#!/usr/bin/env python3.5
"""
Easy-as-it-gets python3.5 library to search magnets
in kickasstorrents (kat.cr)

Usage:
    katcr --search <SEARCH_TERM> --pages <PAGES_NUM>

Options:
    --search=<SEARCH_TERM>   Search term(s)
    --pages=<PAGES_NUM>      Number of pages to lookup

Examples:
    katcr --search "Search terms" --pages 3
    katcr --search "Search terms" --pages 1
    katcr --pages 1
"""

import re
import urllib
from docopt import docopt
import asyncio
import aiohttp

MAGNET_RE = re.compile(r'\"magnet:\?xt=urn:(.+?)\"')


async def search_magnets(query, page, loop):
    """
        Coroutine that searches in kat.cr and returns
        all magnet links, no more info, just the magnet links.
    """
    with aiohttp.ClientSession(loop=loop) as session:
        url = 'https://kat.cr/usearch/{}/{}/'.format(query, page)
        async with session.get(url) as response:
            assert response.status == 200
            content = await response.text()
            return MAGNET_RE.finditer(content, re.IGNORECASE).group(0)


def execute_search(query, pagelen=1):
    """
        Example manager, if possible, implement your own.
        The magic is in search_magnets coroutine.
    """
    tasks = []
    loop = asyncio.get_event_loop()

    for page in range(0, pagelen):
        future = asyncio.ensure_future(search_magnets(query, page + 1, loop))
        tasks.append(future)

    loop.run_until_complete(asyncio.wait(tasks))

    for task in tasks:
        for magnet in task.result():
            yield urllib.parse.parse_qs(magnet)


def main():
    """
        Entry point
    """
    opts = docopt(__doc__, version="0.0.1")
    for magnet in execute_search(opts["--search"], int(opts["--pages"])):
        print("magnet:?xt={} - {}".format(magnet["\"magnet:?xt"][0],
                                          magnet['dn'][0]))
