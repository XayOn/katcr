from .base import BaseSearch


class NyaaSi(BaseSearch):
    """Nyaa.Si torrent search engine."""

    proxy_name = ''
    url = 'https://nyaa.si'
    url_format = '{}{}/?f=0&c=0_0&q={}&p={}'
