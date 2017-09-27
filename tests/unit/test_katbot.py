"""Bot tests."""


def test_katbot_isinstance():
    """Test katbot is a bot instance."""
    from telepot import Bot
    from katcr.bot import KATBot
    assert issubclass(KATBot, Bot)
    opts = {'--token': "foo", '--shortener': ''}
    assert isinstance(KATBot(opts), Bot)


def test_katbot_main():
    """Test argument parsing and calling."""
    from katcr.bot import main
    from unittest.mock import patch

    opts = {'--token': "foo"}

    with patch('katcr.bot.docopt', side_effect=(opts,)):
        with patch('katcr.bot.KATBot') as bot:
            with patch('katcr.bot.MessageLoop'):
                main()
                bot.assert_called_with({'--token': 'foo'})


def test_katbot_main_file():
    """Test argument parsing and calling."""
    from katcr.bot import main

    from unittest.mock import patch
    import os
    import tempfile

    with tempfile.NamedTemporaryFile(mode='w', delete=False) as tmpfile:
        tmpfile.write('foobar')

    opts = {'--token': None, '--shortener': None,
            '--token-file': tmpfile.name}
    with patch('katcr.bot.docopt', side_effect=(opts,)):
        with patch('katcr.bot.MessageLoop'):
            with patch('katcr.bot.telepot.Bot.__init__') as mock:
                main()
                mock.assert_called_with('foobar')
    os.unlink(tmpfile.name)


def test_on_chat_message_start():
    """Test on chat message handler."""
    from katcr.bot import KATBot

    class FakeKATBot(KATBot):
        """Fake kat bot to avoid initializing telepot."""

        def __init__(self, token):
            """Set token."""
            self.token = token
            self.shortener = "foo"

    fkb = FakeKATBot("foo")
    assert not fkb.on_chat_message({'text': '/start'})


def test_on_chat_message():
    """Test on chat message handler."""
    from katcr.bot import KATBot
    from unittest.mock import patch, MagicMock
    from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

    class FakeKATBot(KATBot):
        """Fake kat bot to avoid initializing telepot."""

        def __init__(self, token):
            """Set token."""
            self.token = token
            self.katcr = MagicMock()
            self.thepiratebay = MagicMock()
            self.katcr.search.return_value = (('foo', '3', 'bar'),)
            self.shortener = "http://foo"
            self.responses = {}
            self.sendMessage = MagicMock()

    with patch('katcr.bot.telepot.glance', return_value=((0, 0, 1))):
        fkb = FakeKATBot("foo")
        assert not fkb.on_chat_message({'text': 'debian'})
        fkb.sendMessage.assert_called_with(
            1, 'Results for: debian',
            parse_mode='html',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(
                        text='foo',
                        url=None, callback_data='0',
                        switch_inline_query=None,
                        switch_inline_query_current_chat=None,
                        callback_game=None, pay=None)]]))
        assert fkb.responses


def test_on_chat_message_empty():
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
            self.thepiratebay = MagicMock()
            self.shortener = "http://foo"
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
            self.shortener = "http://foo"
            self.sendMessage = MagicMock()

    with patch('katcr.bot.telepot.glance', return_value=((0, 1, 1))):
        with patch('katcr.bot.get_short', return_value=(('foo'))):
            fkb = FakeKATBot("foo")
            assert not fkb.on_callback_query({'text': 'debian'})
            assert fkb.sendMessage.called
            assert fkb.sendMessage.call_args[0][0] == 1
            assert 'href' in fkb.sendMessage.call_args[0][1]
            assert fkb.sendMessage.call_args[1]['parse_mode'] == 'html'


def test_katbot_tokenfile():
    """Test katbot tokenfile."""
