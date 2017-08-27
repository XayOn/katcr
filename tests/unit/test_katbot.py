"""Bot tests."""


def test_katbot_isinstance():
    """Test katbot is a bot instance."""
    from telepot import Bot
    from katcr.bot import KATBot
    assert issubclass(KATBot, Bot)
    assert isinstance(KATBot("foo"), Bot)


def test_katbot_main():
    """Test argument parsing and calling."""
    from katcr.bot import main
    from unittest.mock import patch

    opts = {'--token': "foo"}

    with patch('katcr.bot.docopt', side_effect=(opts,)):
        with patch('katcr.bot.KATBot') as bot:
            with patch('katcr.bot.MessageLoop'):
                main()
                bot.assert_called_with('foo')
