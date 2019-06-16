from contextlib import suppress
import abc
import itertools

import requests

import robobrowser
import torrentmirror


class BaseSearch(metaclass=abc.ABCMeta):
    """Base Search."""

    def __init__(self, session, logger):
        """Initialize browser instance."""
        self.session = session
        self.logger = logger
        self.browser = robobrowser.RoboBrowser(session=session,
                                               parser='html.parser',
                                               timeout=50)

    @abc.abstractproperty
    def url(self):
        """Search on given url by default."""

    @abc.abstractproperty
    def proxy_name(self):
        """Proxy name to use from torrentmirror."""

    @abc.abstractproperty
    def url_format(self):
        """Url formatter to add to base_url."""

    @abc.abstractmethod
    def get_torrents(self):
        """Return a list of torrents."""

    def search_magnets(self, query: str, page: int):
        """Return the list of magnets from a specific page."""
        proxies = torrentmirror.get_proxies().get(self.proxy_name, [])
        self.logger.debug("Got proxies: %s", proxies)
        proxies.insert(0, [self.url, None])
        for site, _ in proxies:
            self.logger.debug("Searching in %s", site)
            with suppress(requests.exceptions.ReadTimeout,
                          requests.ConnectionError,
                          requests.exceptions.SSLError, AssertionError):
                http = '' if site.startswith('http') else 'http://'
                self.browser.open(
                    self.url_format.format(http, site, query, page))
                torrents = self.get_torrents()
                assert torrents
                self.logger.debug("Got torrents %s", torrents)
                return torrents
        return []

    def search(self, query: str, pagelen: int = 1):
        """Manage complete search for specified pages."""
        return itertools.chain(*(self.search_magnets(query, page + 1)
                                 for page in range(0, pagelen)))
