import os
from .base import BaseSearch

HOST = os.getenv('JACKETT_HOST')
APIKEY = os.getenv('JACKETT_APIKEY')


class Jackett(BaseSearch):
    """Use jackett's all search engines feature"""

    proxy_name = None
    url_format = '{}{}&q={}&p={}'
    url = f"{HOST}/api/v2.0/indexers/all/results/torznab?apikey={APIKEY}"

    def get_torrents(self):
        for item in self.browser.find_all("item"):
            yield (item.find('title').text, item.find('size').text,
                   item.find('enclosure').get('url'))
