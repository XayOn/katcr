import html.parser
from .base import BaseSearch


class Skytorrents(BaseSearch):
    """Skytorrents.in torrent search engine."""

    proxy_name = ''
    url = 'https://skytorrents.lol/'
    url_format = '{}{}/?query={}&page={}'

    @staticmethod
    def parse_magnet(magnet):
        """Skytorrents magnets are html-scaped"""
        return BaseSearch.parse_magnet(html.parser.unescape(magnet))
