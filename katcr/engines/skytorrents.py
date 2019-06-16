from .base import BaseSearch


class Skytorrents(BaseSearch):
    """Skytorrents.in torrent search engine."""

    proxy_name = ''
    url = 'https://skytorrents.in/'
    url_format = '{0}{1}search/all/ed/{3}/?l=en-us&q={2}'

    @staticmethod
    def tabulate(row):
        """Extract all information from each href."""
        with suppress(IndexError):
            cols = row.find_all('td')
            links = cols[0].find_all('a')
            return (links[0].text, cols[1].text, links[1]['href'])

    def get_torrents(self):
        """Return torrents."""
        # pylint: disable=not-callable
        return list(
            filter(None,
                   [self.tabulate(l) for l in self.browser.find_all('tr')]))
