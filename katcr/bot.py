import asyncio
from aiogram import Bot, Dispatcher, types


async def start_handler(event: types.Message):
    await event.answer(
        (f"Hello, {event.from_user.get_mention(as_html=True)} 👋!"
         f" I'm katbot, a bot to search on multiple torrent search engines."
         f" Use the /search <your_search> command with your query and I'll"
         f" return some results"),
        parse_mode=types.ParseMode.HTML,
    )


async def search_handler(event: types.Message):
    magnets = [event.text[8:]]
    await event.answer('<br/>'.join(magnets), parse_mode=types.ParseMode.HTML)


async def bot_main(handler, token):
    bot = Bot(token=token)
    try:
        disp = Dispatcher(bot=bot)
        disp.register_message_handler(start_handler,
                                      commands={"start", "restart"})
        disp.register_message_handler(search_handler, commands={"search"})
        await disp.start_polling()
    finally:
        await bot.close()
