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


def test_on_chat_message_start():
    """Test on chat message handler."""
    from katcr.bot import KATBot

    class FakeKATBot(KATBot):
        """Fake kat bot to avoid initializing telepot."""

        def __init__(self, token):
            """Set token."""
            self.token = token

    fkb = FakeKATBot("foo")
    assert not fkb.on_chat_message({'text': '/start'})


def test_on_chat_message():
    """Test on chat message handler."""
    from katcr.bot import KATBot
    from unittest.mock import patch, MagicMock
    from telepot.namedtuple import InlineKeyboardMarkup

    class FakeKATBot(KATBot):
        """Fake kat bot to avoid initializing telepot."""

        def __init__(self, token):
            """Set token."""
            self.token = token
            self.katcr = MagicMock()
            self.responses = {}
            self.sendMessage = MagicMock()

    with patch('katcr.bot.telepot.glance', return_value=((0, 0, 1))):
        fkb = FakeKATBot("foo")
        assert not fkb.on_chat_message({'text': 'debian'})
        fkb.sendMessage.assert_called_with(
            1, 'Results for: debian',
            parse_mode='html',
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[]))


def test_on_callback_query():
    """Test on chat message handler."""
    from katcr.bot import KATBot
    from unittest.mock import patch, MagicMock

    class FakeKATBot(KATBot):
        """Fake kat bot to avoid initializing telepot."""

        def __init__(self, token):
            """Set token."""
            self.token = token
            self.katcr = MagicMock()
            self.responses = {1: {1: ['foo', 'foo']}}
            self.sendMessage = MagicMock()

    with patch('katcr.bot.telepot.glance', return_value=((0, 1, 1))):
        with patch('katcr.bot.requests'):
            fkb = FakeKATBot("foo")
            assert not fkb.on_callback_query({'text': 'debian'})
            assert fkb.sendMessage.called
            assert fkb.sendMessage.call_args[0][0] == 1
            assert 'href' in fkb.sendMessage.call_args[0][1]
            assert fkb.sendMessage.call_args[1]['parse_mode'] == 'html'
