from unittest.mock import patch
import logging
import pytest


def test_abs():
    """Test abstract methods"""
    from katcr.engines.base import BaseSearch
    abs = BaseSearch.__abstractmethods__
    assert 'proxy_name' in abs
    assert 'url' in abs
    assert 'url_format' in abs


@pytest.mark.asyncio
@patch('torrentmirror.get_proxies', return_value={})
async def test_search_magnets_without_proxies_with_results(torrent):
    """Test search magnets method"""
    from katcr.engines.base import BaseSearch

    class FakeSearch(BaseSearch):
        url = "http://foo.com"
        url_format = ''
        proxy_name = 'fake'
        logger = logging.getLogger()

        async def search_site(self, url):
            return [{'foo': 'bar'}]

    result = await FakeSearch().search_magnets('foo', 1)
    assert result == [{'foo': 'bar'}]
    torrent.assert_called()


@pytest.mark.asyncio
@patch('torrentmirror.get_proxies', return_value={})
async def test_search_magnets_without_proxies_without_results(torrent):
    """Test search magnets method"""
    from katcr.engines.base import BaseSearch

    class FakeSearch(BaseSearch):
        url = "http://foo.com"
        url_format = ''
        proxy_name = 'fake'
        logger = logging.getLogger()

        async def search_site(self, url):
            return

    result = await FakeSearch().search_magnets('foo', 1)
    assert result == []


@pytest.mark.asyncio
@patch('torrentmirror.get_proxies', side_effect=Exception)
async def test_search_magnets_without_proxies_with_exceptions(torrent):
    """Test search magnets method"""
    from katcr.engines.base import BaseSearch

    class FakeSearch(BaseSearch):
        url = "http://foo.com"
        url_format = ''
        proxy_name = 'fake'
        logger = logging.getLogger()

        async def search_site(self, url):
            return [{'foo': 'bar'}]

    result = await FakeSearch().search_magnets('foo', 1)
    assert result == [{'foo': 'bar'}]


@pytest.mark.asyncio
async def test_get_torrents():
    from katcr.engines.base import BaseSearch

    text = ('<a href="magnet:?xt=urn:btih:22222&dn=123">asdf</a>'
            '<a href="magnet:?xt=urn:btih:1111111&dn=345">asdf</a>')

    class FakeReq:
        async def text(self):
            return text

    result = [a async for a in BaseSearch.get_torrents(FakeReq())]
    assert result == [('123', 'magnet:?xt=urn:btih:22222&dn=123'),
                      ('345', 'magnet:?xt=urn:btih:1111111&dn=345')]


@pytest.mark.asyncio
async def test_search():
    from katcr.engines.base import BaseSearch
    from unittest.mock import MagicMock, call
    mock = MagicMock()

    class FakeSearch(BaseSearch):
        url = "http://foo.com"
        url_format = ''
        proxy_name = 'fake'
        logger = logging.getLogger()

        async def search_site(self, url):
            return [{'foo': 'bar'}]

        async def search_magnets(self, query, page):
            mock(query, page)
            return [1, 2]

    assert await FakeSearch().search('a', 2) == [1, 2, 1, 2]
    mock.assert_has_calls([call('a', 1), call('a', 2)])
