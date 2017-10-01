"""Base tests. Nothing related to plugins goes here."""


def test_main():
    """Test argument parsing and calling."""
    from katcr import main
    from unittest.mock import patch
    opts = {'<SEARCH_TERM>': "foo", '--search-engines': ['Katcr'],
            '--interactive': False, '--open': False, '-d': False,
            '--disable-shortener': True, '--pages': [1]}
    with patch('katcr.Katcr') as mock:
        with patch('katcr.docopt', side_effect=(opts,)):
            main()
            mock().search.assert_called_with(opts['<SEARCH_TERM>'], 1)


def test_main_with_shortener():
    """Test usage with url shortener."""
    from katcr import main, get_from_short
    from unittest.mock import patch, call
    opts = {'<SEARCH_TERM>': "foo", '--search-engines': ['Katcr'],
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
        # pylint: disable=too-few-public-methods, missing-docstring
        text = "foo"

    with patch('katcr.requests.post', return_value=Foo) as mock:
        with patch('katcr.docopt', side_effect=(opts,)):
            result = list(get_from_short(
                "foo.com", [("1", "2"), ("3", "4")]))
            assert [result == [('1', '2', 'foo.com/foo'),
                               ('3', '4', 'foo.com/foo')]]
            mock.assert_has_calls([call('foo.com', data={'magnet': '2'}),
                                   call('foo.com', data={'magnet': '4'})])


def test_main_open_link():
    """Test open link option."""
    from katcr import main
    from unittest.mock import patch
    opts = {'<SEARCH_TERM>': "foo", '--search-engines': ['Katcr'],
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


def test_interactive_mode():
    """Test interactive mode."""
    from katcr import main
    from unittest.mock import patch
    opts = {'<SEARCH_TERM>': "foo", '--search-engines': ['Katcr'],
            '--interactive': True, '--open': False, '-d': False,
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
                        smock.check_call.assert_not_called()


def test_logging():
    """Test logging."""
    from katcr import main
    from unittest.mock import patch
    opts = {'<SEARCH_TERM>': "foo", '--search-engines': ['Katcr'],
            '--interactive': True, '--open': False,
            '--verbose': True,
            '--disable-shortener': True, '--pages': [1]}
    torr = {'Link': 'foo'}

    with patch('katcr.Katcr') as mock:
        with patch('katcr.Terminal') as tmock:
            tmock().width = 50
            mock().search.side_effect = ((('foo', "3", 'bar'),),)
            with patch('katcr.docopt', side_effect=(opts,)):
                with patch('katcr.prompt', side_effect=(torr,)):
                    with patch('katcr.Gogo') as logging_mock:
                        main()
                        logging_mock.assert_called_with(
                            'katcr', verbose=True)


def test_search_call():
    """Test main search call."""
    from katcr import main
    from unittest.mock import patch
    opts = {'<SEARCH_TERM>': "foo",
            '--search-engines': ['Katcr'],
            '--interactive': False,
            '--open': False,
            '--disable-shortener': True,
            "--shortener": "http://foo.com",
            '--pages': [1]}
    args = opts['<SEARCH_TERM>'], 1

    with patch('katcr.Terminal') as tmock:
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
        with unittest.mock.patch('katcr.torrentmirror.get_proxies',
                                 side_effect=({},)):
            class FakeSearch(BaseSearch):
                """Fake search."""

                def get_torrents(self):
                    """Get torrents."""
                    return "foo"
                browser = unittest.mock.MagicMock()
                proxy_name = "The Pirate Bay"
                url = "Foo"
                url_format = None

            FakeSearch(mock.MagicMock).search('foo', 2)
            assert mock.call_count == 2

    with unittest.mock.patch('katcr.torrentmirror.get_proxies',
                             side_effect=({},)):
        class FakeSearchB(BaseSearch):
            """Fake search."""

            proxy_name = "The Pirate Bay"
            url = "Foo"
            url_format = "http://foo.com/"

            def __init__(self, logger):
                super().__init__(logger)
                self.browser = unittest.mock.MagicMock()

            def get_torrents(self):
                return "foo"

        FakeSearchB(unittest.mock.MagicMock()).search('foo', 2)
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
