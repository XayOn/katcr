from contextlib import suppress
import urllib.parse
import re
import abc
import torrentmirror
import aiohttp

CLDS = 'cloudflare', 'cloudfront'
MAG = re.compile(
    r"(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")


class CloudFlareError(Exception):
    """Cloud flare detected"""


class BaseSearch(metaclass=abc.ABCMeta):
    """Base Search."""
    session = None
    logger = None

    @abc.abstractproperty
    def url(self):
        """Search on given url by default."""

    @abc.abstractproperty
    def proxy_name(self):
        """Proxy name to use from torrentmirror."""

    @abc.abstractproperty
    def url_format(self):
        """Url formatter to add to base_url."""

    async def search_magnets(self, query: str, page: int):
        """Return the list of magnets from a specific page.

        warning: paging may produce strange results if the first available
        proxy changes between searches.

        Arguments

            query: Query string
            page: Page to search on
        """
        proxies = []
        try:
            all_proxies = torrentmirror.get_proxies()
        except:
            all_proxies = {}
            self.logger.debug('cant_get_proxies')

        proxies = [
            a['link'] for a in all_proxies.get(self.proxy_name, {})
            if a.get('status') == 'ONLINE'
        ]
        self.logger.debug("Got proxies: %s", proxies)
        proxies.insert(0, self.url)

        for site in proxies:
            # First site to get results wins.
            http = '' if site.startswith('http') else 'http://'
            url = self.url_format.format(http, site, query, page)
            self.logger.debug("Searching in %s (%s)", site, url)
            if res := await self.search_site(url):
                return res

        return []

    async def search_site(self, url):
        with suppress(aiohttp.ClientError, CloudFlareError):
            response = await self.session.get(url)
            text = await response.text()

            if any(reserved in text for reserved in CLDS):
                raise CloudFlareError()

            return [a async for a in self.get_torrents(response)]

    @classmethod
    async def get_torrents(cls, data):
        """Get torrents from a site. data will be a response."""
        data = await data.text()
        results = (a for a in MAG.findall(data) if a.startswith('magnet'))
        for result in results:
            result = cls.parse_magnet(result)
            if result:
                yield result

    @staticmethod
    def parse_magnet(magnet):
        """Parse magnet, only returns identifiable magnets."""
        result = urllib.parse.parse_qs(magnet)
        if result and result.get('dn'):
            return next(iter(result.get('dn', [])), ''), magnet

    async def search(self, query: str, pagelen: int = 1):
        """Manage complete search for specified pages."""
        results = []
        for page in range(0, pagelen):
            self.logger.debug("Getting page %s", page)
            results.extend(await self.search_magnets(query, page + 1))
        return results
