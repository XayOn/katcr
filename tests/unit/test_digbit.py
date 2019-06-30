"""Tets dibgit plugin."""


def test_digbit_search_magnets():
    """Test digbit search magnets method."""
    from katcr.engines.digbt import DigBt
    from robobrowser import RoboBrowser
    from unittest.mock import patch, MagicMock
    import logging
    logger = logging.getLogger()

    with patch('katcr.engines.base.torrentmirror.get_proxies',
               side_effect=({}, )) as mock:
        with patch('katcr.engines.base.robobrowser.RoboBrowser',
                   spec=RoboBrowser) as mock:
            DigBt(MagicMock(), logger).search_magnets('foo', 1)
            assert mock.open.called_once_with('foo')


def test_digbit_tabulate():
    """Test tabulate method given a known structure.

    Note that this structure may change in the future or even between
    different proxied sites... This needs to be handled somehow.
    """
    from katcr.engines.digbt import DigBt
    import bs4
    to_parse = """<tr><div class=head><a>Foo</a></div>
                       <div class=tail>1 2 3 4 Bar<a href='foo'>
                       </a></div></tr>"""
    fakelink = bs4.BeautifulSoup(to_parse, "html.parser")
    result = DigBt.tabulate(fakelink.find('tr'))
    assert result == ('Foo', 'Bar', 'foo')
