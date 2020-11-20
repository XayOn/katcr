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
