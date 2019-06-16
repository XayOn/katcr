import re
from .base import BaseSearch


class Katcr(BaseSearch):
    """KickAssTorrents search engine.

    Search on any of the pirate bay proxies or thepiratebay itself if
    available. Extract torrents, description and return it tabulated and ready
    to be printed
    """

    proxy_name = 'kickass-torrents'
    url_format = '{}{}/search.php?q={}&p={}'
    url = 'https://kat.cd'

    @staticmethod
    def tabulate(link):
        """Make a given a href link parsed on bs4 printable."""
        magnet = link.find('a', title='Torrent magnet link')
        return (link.find(class_='cellMainLink').text,
                link.find_all('td')[1].text, magnet['href'])

    def get_torrents(self):
        """Return a list of torrents, printable."""
        # pylint: disable=not-callable
        torrents = self.browser.find_all(
            id=re.compile('torrent_latest_torrents(.*)'))
        return [self.tabulate(torrent) for torrent in torrents]
