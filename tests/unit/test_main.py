"""Base tests. Nothing related to plugins goes here."""


def test_main():
    """Test argument parsing and calling."""
    from katcr import main, get_from_short
    from unittest.mock import patch, call
    opts = {'<SEARCH_TERM>': "foo", '--plugin': 'Katcr',
            '--interactive': False, '--open': False, '-d': False,
            '--enable-shortener': False, '--pages': 1}
    with patch('katcr.Katcr') as mock:
        with patch('katcr.docopt', side_effect=(opts,)):
            main()
            mock().search.assert_called_with(opts['<SEARCH_TERM>'], 1)

    opts = {'<SEARCH_TERM>': "foo", '--plugin': 'Katcr',
            '--interactive': False, '--open': False, '-d': False,
            '--shortener': 'bar',
            '--enable-shortener': True, '--pages': 1}
    with patch('katcr.Katcr') as mock:
        with patch('katcr.get_from_short') as short_mock:
            with patch('katcr.docopt', side_effect=(opts,)):
                main()
                mock().search.assert_called_with(opts['<SEARCH_TERM>'], 1)
                short_mock.assert_called_with('bar', [])

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

    opts = {'<SEARCH_TERM>': "foo", '--plugin': 'Katcr',
            '--interactive': True, '--open': True, '-d': False,
            '--enable-shortener': False, '--pages': 1}
    torr = {'Link': 'foo'}
    args = opts['<SEARCH_TERM>'], 1

    with patch('katcr.Katcr') as mock:
        with patch('katcr.Terminal') as tmock:
            tmock().width = 50
            mock().search.side_effect = ((('foo', 'bar'),),)
            with patch('katcr.subprocess') as smock:
                with patch('katcr.docopt', side_effect=(opts,)):
                    with patch('katcr.prompt', side_effect=(torr,)):
                        main()
                        mock().search.assert_called_with(*args)
                        smock.check_call.assert_called_with(
                            ['xdg-open', 'bar'])

    opts = {'<SEARCH_TERM>': "foo", '--plugin': 'Katcr',
            '--interactive': True, '--open': False, '-d': False,
            '--enable-shortener': False, '--pages': 1}

    with patch('katcr.Katcr') as mock:
        with patch('katcr.Terminal') as tmock:
            tmock().width = 50
            mock().search.side_effect = ((('foo', 'bar'),),)
            with patch('katcr.subprocess') as smock:
                with patch('katcr.docopt', side_effect=(opts,)):
                    with patch('katcr.prompt', side_effect=(torr,)):
                        main()
                        mock().search.assert_called_with(*args)
                        smock.check_call.assert_not_called()

    opts = {'<SEARCH_TERM>': "foo", '--plugin': 'Katcr',
            '--interactive': True, '--open': False, '-d': True,
            '--enable-shortener': False, '--pages': 1}

    with patch('katcr.Katcr') as mock:
        with patch('katcr.Terminal') as tmock:
            tmock().width = 50
            mock().search.side_effect = ((('foo', 'bar'),),)
            with patch('katcr.subprocess') as smock:
                with patch('katcr.docopt', side_effect=(opts,)):
                    with patch('katcr.prompt', side_effect=(torr,)):
                        import logging
                        main()
                        level = logging.getLogger().getEffectiveLevel()
                        assert level == logging.DEBUG


def test_basesearch():
    """Test basesearch has required methods."""
    import unittest.mock
    from katcr import BaseSearch

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

        FakeSearch().search('foo', 2)
        assert mock.call_count == 2


def test_cli_help():
    """Test help call."""
    import subprocess
    from katcr import main
    result = subprocess.check_output(['katcr', '--help'])
    assert main.__doc__.encode() in result
