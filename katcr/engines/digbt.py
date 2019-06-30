from contextlib import suppress
from .base import BaseSearch


class DigBt(BaseSearch):
    """Digbt DHT search engine."""

    proxy_name = ''
    url = 'https://digbt.org/'
    url_format = '{0}{1}search/{2}-relevance-{3}/'

    @staticmethod
    def tabulate(row):
        """Extract all information from each href."""
        with suppress(IndexError, TypeError):
            tail = row.find(class_='tail')
            return (row.find('div').find('a').text.strip(),
                    list(filter(lambda x: x, tail.text.split(' ')))[4].strip(),
                    tail.find('a')['href'].strip())

    def get_torrents(self):
        """Return torrents."""
        # pylint: disable=not-callable
        return list(
            filter(None,
                   [self.tabulate(l) for l in self.browser.find_all('tr')]))
