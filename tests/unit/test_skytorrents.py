"""Test skytorrents plugin."""


def test_skytorrents_search_magnets():
    """Test skytorrents search magnets method."""
    from katcr import Skytorrents
    from robobrowser import RoboBrowser
    from unittest.mock import patch, MagicMock

    with patch('katcr.torrentmirror.get_proxies',
               side_effect=({},)) as mock:
        with patch('katcr.robobrowser.RoboBrowser', spec=RoboBrowser) as mock:
            Skytorrents(MagicMock()).search_magnets('foo', 1)
            assert mock.open.called_once_with('foo')


def test_skytorrents_tabulate():
    """Test tabulate method given a known structure.

    Note that this structure may change in the future or even between
    different proxied sites... This needs to be handled somehow.
    """
    from katcr import Skytorrents
    import bs4
    to_parse = """<tr><td><a href="">Foo</a>
                  <a href="foo"></a></td><td>Bar</td></tr>"""
    fakelink = bs4.BeautifulSoup(to_parse, "html.parser")
    result = Skytorrents.tabulate(fakelink.find('tr'))
    assert result == ('Foo', 'Bar', 'foo')
