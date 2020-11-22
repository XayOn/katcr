from aiogram import Bot, Dispatcher, types


class BotHandler:
    """Main bothandler class"""
    def __init__(self, handler):
        """Set parent handler to delegate search function."""
        self.handler = handler

    async def start_handler(self, event: types.Message):
        """Start command"""
        await event.answer(
            (f"Hello, {event.from_user.get_mention(as_html=True)} 👋!"
             f" I'm katbot, use me to search on many torrent search engines."
             f" Use the /search <your_search> command with your query and I'll"
             f" return some results"),
            parse_mode=types.ParseMode.HTML,
        )

    async def search_handler(self, event: types.Message):
        """Search in providers."""
        provs = ['ThePirateBay', 'Eztv', 'NyaaSi', 'Skytorrents']
        response = await self.handler.search(provs, event.text[8:], 1, 0, 0)
        for res in response:
            await event.answer(f'{res.result[0]} &gt; {res.result[1]}',
                               parse_mode=types.ParseMode.HTML)

    async def start(self, token):
        """Start bot."""
        bot = Bot(token=token)
        try:
            disp = Dispatcher(bot=bot)
            register = disp.register_message_handler
            register(self.start_handler, commands={"start"})
            register(self.search_handler, commands={"search"})
            await disp.start_polling()
        finally:
            await bot.close()
