"""Tets TPB plugin."""


def test_tpb_search_magnets():
    """Test tpb search magnets method."""
    pass


def test_tpb_make_printable():
    """Test make_printable method given a known structure.

    Note that this structure may change in the future or even between
    different proxied sites... This needs to be handled somehow.
    """
    from katcr import ThePirateBay
    import bs4
    to_parse = """<div><div class=detName>Foo</div>
                       <div class=detDesc>Bar</div>
                       <a href='foo'></a></div>"""
    fakelink = bs4.BeautifulSoup(to_parse, "html.parser")
    result = ThePirateBay.make_printable(fakelink.find('a'))
    assert result == ('Foo - Bar', 'foo')
