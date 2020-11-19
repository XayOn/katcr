from .base import BaseSearch


class Katcr(BaseSearch):
    """KickAssTorrents search engine.

    Search on any of the pirate bay proxies or thepiratebay itself if
    available. Extract torrents, description and return it tabulated and ready
    to be printed
    """

    proxy_name = 'Kickass'
    url_format = '{}{}/usearch/{}/{}/'
    url = 'https://kat.cd'
