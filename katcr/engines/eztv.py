from .base import BaseSearch


class Eztv(BaseSearch):
    """EZTV torrent search engine."""

    proxy_name = ''
    url = 'https://eztv.ag'
    url_format = '{}{}/search/{}'
