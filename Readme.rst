Katcr
-----

Easy-as-it-gets python3.5 library to search magnets
in kickasstorrents (kat.cr)

Uses aiohttp to do paralell searches on kickasstorrents

It also exports a nice text user interface:

::

   Usage:
       katcr --search <SEARCH_TERM> --pages <PAGES_NUM>

   Options:
       --search=<SEARCH_TERM>   Search term(s)
       --pages=<PAGES_NUM>      Number of pages to lookup

   Examples:
       katcr --search "Search terms" --pages 3
       katcr --search "Search terms" --pages 1
       katcr --pages 1


Usage
-----

As a library, you can import the main coroutine with::

    from katcr import search_magnets

    loop = asyncio.get_event_loop()
    task = asyncio.ensure_future(search_magnets("what", 1, loop))
    loop.run_until_complete(task)

    for magnet in task.result():
        yield magnet


KATbot
------

This exposes a Telegram Bot using telepot that returns links for
.torrent files on KAT.cr for the first results page of
whatever you send to the bot.
