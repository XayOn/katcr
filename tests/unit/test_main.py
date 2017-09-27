"""Base tests. Nothing related to plugins goes here."""


def test_main():
    """Test argument parsing and calling."""
    from katcr import main, get_from_short
    from unittest.mock import patch, call
    opts = {'<SEARCH_TERM>': "foo", '--search-engine': ['Katcr'],
            '--interactive': False, '--open': False, '-d': False,
            '--disable-shortener': True, '--pages': [1]}
    with patch('katcr.Katcr') as mock:
        with patch('katcr.docopt', side_effect=(opts,)):
            main()
            mock().search.assert_called_with(opts['<SEARCH_TERM>'], 1)

    opts = {'<SEARCH_TERM>': "foo", '--search-engine': ['Katcr'],
            '--interactive': False, '--open': False, '-d': False,
            '--shortener': ['bar'],
            '--disable-shortener': False, '--pages': [1]}
    with patch('katcr.Katcr') as mock:
        with patch('katcr.get_from_short') as short_mock:
            with patch('katcr.docopt', side_effect=(opts,)):
                main()
                mock().search.assert_called_with(opts['<SEARCH_TERM>'], 1)
                short_mock.assert_called_with('bar', None)

    class Foo:
        text = "foo"

    with patch('katcr.requests.post', return_value=Foo) as mock:
        with patch('katcr.docopt', side_effect=(opts,)):
            result = list(get_from_short(
                "foo.com", [("1", "2"), ("3", "4")]))
            assert [result == [('1', '2', 'foo.com/foo'),
                               ('3', '4', 'foo.com/foo')]]
            mock.assert_has_calls([call('foo.com', data={'magnet': '2'}),
                                   call('foo.com', data={'magnet': '4'})])

    opts = {'<SEARCH_TERM>': "foo", '--search-engine': ['Katcr'],
            '--interactive': True, '--open': True, '-d': False,
            '--disable-shortener': True, "--shortener": "http://foo.com",
            '--pages': [1]}
    torr = {'Link': 'foo'}
    args = opts['<SEARCH_TERM>'], 1

    with patch('katcr.Katcr') as mock:
        with patch('katcr.Terminal') as tmock:
            tmock().width = 50
            mock().search.side_effect = ((('foo', "3", 'bar'),),)
            with patch('katcr.subprocess') as smock:
                with patch('katcr.docopt', side_effect=(opts,)):
                    with patch('katcr.prompt', side_effect=(torr,)):
                        main()
                        mock().search.assert_called_with(*args)
                        smock.check_call.assert_called_with(
                            ['xdg-open', 'bar'])

    opts = {'<SEARCH_TERM>': "foo", '--search-engine': ['Katcr'],
            '--interactive': True, '--open': False, '-d': False,
            '--disable-shortener': True, "--shortener": "http://foo.com",
            '--pages': [1]}

    with patch('katcr.Katcr') as mock:
        with patch('katcr.Terminal') as tmock:
            tmock().width = 50
            mock().search.side_effect = ((('foo', "3", 'bar'),),)
            with patch('katcr.subprocess') as smock:
                with patch('katcr.docopt', side_effect=(opts,)):
                    with patch('katcr.prompt', side_effect=(torr,)):
                        main()
                        mock().search.assert_called_with(*args)
                        smock.check_call.assert_not_called()

    opts = {'<SEARCH_TERM>': "foo", '--search-engine': ['Katcr'],
            '--interactive': True, '--open': False,
            '--verbose': True,
            '--disable-shortener': True, '--pages': [1]}

    with patch('katcr.Katcr') as mock:
        with patch('katcr.Terminal') as tmock:
            tmock().width = 50
            mock().search.side_effect = ((('foo', "3", 'bar'),),)
            with patch('katcr.subprocess') as smock:
                with patch('katcr.docopt', side_effect=(opts,)):
                    with patch('katcr.prompt', side_effect=(torr,)):
                        with patch('katcr.Gogo') as logging_mock:
                            main()
                            logging_mock.assert_called_with(
                                'katcr', verbose=True)

    opts = {'<SEARCH_TERM>': "foo",
            '--search-engine': ['Katcr'],
            '--interactive': False,
            '--open': False,
            '--disable-shortener': True,
            "--shortener": "http://foo.com",
            '--pages': [1]}
    torr = {'Link': 'foo'}
    args = opts['<SEARCH_TERM>'], 1

    with patch('katcr.Katcr') as mock:
        tmock().width = 50
        mock().search.side_effect = ((('foo', 'bar', "baz"),),)
        with patch('katcr.docopt', side_effect=(opts,)):
            main()
            mock().search.assert_called_with(*args)


def test_basesearch():
    """Test basesearch has required methods."""
    from katcr import BaseSearch
    import unittest.mock
    import warnings
    warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

    assert hasattr(BaseSearch, "search")
    assert hasattr(BaseSearch, "search_magnets")

    with unittest.mock.patch('katcr.BaseSearch.search_magnets',
                             side_effect=(['foo'],)) as mock:
        class FakeSearch(BaseSearch):
            def get_torrents(self):
                return "foo"
            proxy_name = "The Pirate Bay"
            url = "Foo"
            url_format = None

        FakeSearch(mock.MagicMock).search('foo', 2)
        assert mock.call_count == 2

    class FakeSearch(BaseSearch):
        browser = mock.MagicMock()
        proxy_name = "The Pirate Bay"
        url = "Foo"
        url_format = "http://foo.com/"

        def get_torrents(self):
            return "foo"
    FakeSearch(mock.MagicMock).search('foo', 2)
    assert mock.call_count == 2


def test_cli_help():
    """Test help call."""
    import subprocess
    from katcr import main
    result = subprocess.check_output(['katcr', '--help'])
    assert main.__doc__.encode() in result


def test_search_in_engines():
    """Test search_in_engines function."""
    from unittest.mock import patch, MagicMock

    with patch('katcr.Katcr.search', side_effect=(tuple(),)):
        with patch('katcr.ThePirateBay.search', side_effect=(tuple(),)):
            from katcr import search_in_engines
            search_in_engines(MagicMock(), ["All"], "test", 1)
