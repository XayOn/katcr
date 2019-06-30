"""Tets TPB plugin."""


def test_tpb_search_magnets():
    """Test tpb search magnets method."""
    from katcr.engines import ThePirateBay
    from robobrowser import RoboBrowser
    from unittest.mock import patch, MagicMock
    proxies = {'The Pirate Bay': [['foo', None]]}

    import logging
    logger = logging.getLogger()

    with patch('katcr.engines.base.torrentmirror.get_proxies',
               side_effect=(proxies, )) as mock:
        with patch('katcr.engines.base.robobrowser.RoboBrowser',
                   spec=RoboBrowser) as mock:
            ThePirateBay(MagicMock(), logger).search_magnets('foo', 1)
            assert mock.open.called_once_with('foo')


def test_tpb_tabulate():
    """Test tabulate method given a known structure.

    Note that this structure may change in the future or even between
    different proxied sites... This needs to be handled somehow.
    """
    from katcr.engines import ThePirateBay
    import bs4
    to_parse = """<div><div class=detName>Foo</div>
                       <div class=detDesc>Bar</div>
                       <a href='foo'></a></div>"""
    fakelink = bs4.BeautifulSoup(to_parse, "html.parser")
    result = ThePirateBay.tabulate(fakelink.find('a'))
    assert result == ('Foo', 'Bar', 'foo')
