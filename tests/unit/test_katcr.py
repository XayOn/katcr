"""Tests on katcr plugin."""


def test_katcr_search_magnets():
    """Test katcr search magnets method."""
    from katcr import Katcr
    from robobrowser import RoboBrowser
    from unittest.mock import patch, MagicMock
    proxies = {'Kickass Torrents': [['foo', None]]}

    with patch('katcr.torrentmirror.get_proxies',
               side_effect=(proxies,)) as mock:
        with patch('katcr.robobrowser.RoboBrowser', spec=RoboBrowser) as mock:
            Katcr(MagicMock()).search_magnets('foo', 1)
            assert mock.open.called_once_with('foo')


def test_katcr_tabulate():
    """Test tabulate method given a known structure.

    Note that this structure may change in the future or even between
    different proxied sites... This needs to be handled somehow.
    """
    from katcr import Katcr
    import bs4
    to_parse = """<div class=cellMainLink>Foo</div><td>Nope</td><td>Bar</td>
                  <a title='Torrent magnet link' href='foo'></a>"""
    fakelink = bs4.BeautifulSoup(to_parse, "html.parser")
    result = Katcr.tabulate(fakelink)
    assert result == ('Foo', 'Bar', 'foo')
