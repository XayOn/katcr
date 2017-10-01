"""Test nyaasi plugin."""


def test_nyaasi_search_magnets():
    """Test nyaasi search magnets method."""
    from katcr import NyaaSi
    from robobrowser import RoboBrowser
    from unittest.mock import patch, MagicMock

    with patch('katcr.torrentmirror.get_proxies',
               side_effect=({},)) as mock:
        with patch('katcr.robobrowser.RoboBrowser', spec=RoboBrowser) as mock:
            NyaaSi(MagicMock()).search_magnets('foo', 1)
            assert mock.open.called_once_with('foo')


def test_nyaasi_tabulate():
    """Test tabulate method given a known structure.

    Note that this structure may change in the future or even between
    different proxied sites... This needs to be handled somehow.
    """
    from katcr import NyaaSi
    import bs4

    to_parse = """<tr><td><a href=""><img src="" alt="Cat"></a></td>
        <td><a href="">Foo</a></td>
        <td><a href=""></a> <a href="foo"><i class=fa-magnet></i></a></td>
        <td class="text-center">Bar</td></tr>"""
    fakelink = bs4.BeautifulSoup(to_parse, "html.parser")
    result = NyaaSi.tabulate(fakelink.find(class_='fa-magnet'))
    assert result == ('Foo Cat', 'Bar', 'foo')
