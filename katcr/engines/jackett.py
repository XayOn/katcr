import os
from feedparser import parse
from .base import BaseSearch

HOST = os.getenv('JACKETT_HOST')
APIKEY = os.getenv('JACKETT_APIKEY')


class Jackett(BaseSearch):
    """Use jackett's all search engines feature"""

    proxy_name = None
    url_format = '{}{}&q={}&p={}'
    url = f"{HOST}/api/v2.0/indexers/all/results/torznab?apikey={APIKEY}"

    async def search_site(self, url):
        return [[item.title, item.link] for item in parse(url).entries]
