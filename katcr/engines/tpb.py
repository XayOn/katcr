from .base import BaseSearch


class ThePirateBay(BaseSearch):
    """ThePirateBay search engine.

    Search on any of the pirate bay proxies or thepiratebay itself if
    available. Extract torrents, description and return it tabulated and ready
    to be printed
    """

    proxy_name = 'The Pirate Bay'
    url_format = '{}{}/search/{}/{}/99'
    url = 'https://thepiratebay.org/'

    @staticmethod
    def tabulate(link):
        """Make a given a href link parsed on bs4 printable."""
        return (link.parent.find(class_='detName').text,
                link.parent.find(class_='detDesc').text, link['href'])

    def get_torrents(self):
        """Return a list of torrents, printable."""
        # pylint: disable=not-callable
        torrents = self.browser.find_all(
            'a', title='Download this torrent using magnet')
        return [self.tabulate(torrent) for torrent in torrents]
