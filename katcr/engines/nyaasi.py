from .base import BaseSearch


class NyaaSi(BaseSearch):
    """Nyaa.Si torrent search engine."""

    proxy_name = ''
    url = 'https://nyaa.si'
    url_format = '{}{}/?f=0&c=0_0&q={}&p={}'

    @staticmethod
    def tabulate(link):
        """Extract all information from each href."""
        row = link.parent.parent.parent
        cols = row.find_all('td')

        def _nocomments(where):
            return where != 'comments'

        name = ''.join((cols[1].find('a', class_=_nocomments).text.strip(),
                        ' ', cols[0].find('img')['alt'].strip()))
        return (name, cols[3].text.strip(), link.parent['href'])

    def get_torrents(self):
        """Return torrents."""
        # pylint: disable=not-callable
        links = self.browser.find_all(class_='fa-magnet')
        return [self.tabulate(link) for link in links]
