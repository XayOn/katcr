from .base import BaseSearch


class MagnetSh(BaseSearch):
    """Magnet.sh torrent search API."""

    proxy_name = ''
    url_format = '{}{}/api/?q={}&s={}'
    url = 'https://magnet.sh'

    def get_torrents(self):
        """Return a list of torrents."""
        magnet = ('magnet:?xt=urn:btih:{}&tr=udp%3A%2F%2Ftracker.leechers-'
                  'paradise.org%3A6969&tr=udp%3A%2F%2Fzer0day.ch%3A1337&tr='
                  'udp%3A%2F%2Fopen.demonii.com%3A1337&tr=udp%3A%2F%2Ftrack'
                  'er.coppersurfer.tk%3A6969&tr=udp%3A%2F%2Fexodus.desync.co'
                  'm%3A6969')
        return [(a['torrent_name'], 'Unknown',
                 magnet.format(a['torrent_info_hash']))
                for a in self.browser.response.json().values()]
