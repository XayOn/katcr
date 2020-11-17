from .base import BaseSearch
from urllib.parse import quote

TRACKERS = ("udp://tracker.coppersurfer.tk:6969/announce",
            "udp://9.rarbg.me:2850/announce", "udp://9.rarbg.to:2920/announce",
            "udp://tracker.opentrackr.org:1337",
            "udp://tracker.leechers-paradise.org:6969/announce")

TRACKERS = list(quote(t, safe='') for t in TRACKERS)


class ThePirateBay(BaseSearch):
    """ThePirateBay search engine.

    Search on any of the pirate bay proxies or thepiratebay itself if
    available. Extract torrents, description and return it tabulated and ready
    to be printed
    """

    proxy_name = 'The Pirate Bay'
    url_format = '{}{}q.php?q={}&cat='
    url = 'https://apibay.org/'

    async def get_torrents(self, response):
        result = await response.json()
        return [[
            a['name'],
            f"magnet:?xt=urn:btih:{a['info_hash']}&dn={quote(a['name'])}&tr={'&tr='.join(TRACKERS)}"
        ] for a in result]
