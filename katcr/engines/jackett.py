import os
from feedparser import parse
from .base import BaseSearch

HOST = os.getenv('JACKETT_HOST')
APIKEY = os.getenv('JACKETT_APIKEY')


class Jackett(BaseSearch):
    """Use jackett's all search engines feature"""

    proxy_name = None
    url_format = '{}{}&q={}&p={}'

    @property
    def url(self):
        """Return formatted url extracting host and key from config or env."""
        if not self.option:
            self.option = 'all'
        if not self.config.has_section('jackett'):
            self.config.add_section('jackett')
        host = os.getenv('JACKETT_HOST',
                         self.config.get('jackett', 'host', fallback=None))
        apikey = os.getenv('JACKETT_APIKEY',
                           self.config.get('jackett', 'apikey', fallback=None))
        return (f"{host}/api/v2.0/indexers/"
                f"{self.option}/results/torznab?apikey={apikey}")

    async def search_site(self, url):
        """Search jackett using feedparser"""
        return [[item.title, item.link] for item in parse(url).entries]
