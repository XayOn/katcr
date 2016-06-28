.. image:: http://i.imgur.com/ofx75lO.png
   :align: center

\:tv\: Python3 + KickAssTorrents | CLI | Telegram
=================================================

Python3.5 library to search in kickasstorrents (`kat.cr <http://kat.cr>`_)

It's also a **telegram bot** and a **command line interface** :wink:

.. contents:: :local:


\:notebook\: Library Usage
---------------------------

KATcr uses **python3.5**'s new **async def**
`(pep-492) <https://www.python.org/dev/peps/pep-0492/>`_ syntax.

For search, it just has a simple coroutine, **search_magnets**,
that accepts a search term, the page number to return, and a type (
type is either **"torrent"** or **"magnet"**)

::

    from katcr import search_magnets

    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(
        search_magnets("ubuntu", 1, loop, "torrent"))

    for url, name in result:
        print("{}: {}".format(name, url))


**This library also comes with a command line interface and a telegram bot!**



\:tv\: katcr - kickasstorrents command line interface
------------------------------------------------------

katcr comes with a simple but powerful command line interface, able to
return either magnets or torrents.


.. image:: http://i.imgur.com/vdAIPb3.png


Usage
+++++

::

    Easy-as-it-gets python3.5 library to search magnets
    in kickasstorrents (kat.cr)

    Usage:
    	katcr --search=<SEARCH_TERM> --pages=<PAGES_NUM> --type="magnet"

    Options:
    	--search=<SEARCH_TERM>   Search term(s)
    	--pages=<PAGES_NUM>      Number of pages to lookup
    	--type=<magnet|torrent>  Type

    Examples:
    	katcr --search "Search terms" --pages 3
    	katcr --search "Search terms" --pages 1
    	katcr --search "Search terms" --pages 1 --type=magnet
    	katcr --search "Search terms" --pages 1 --type=torrent
    	katcr --pages 1


\:space_invader\: KATBot - Kickasstorrents telegram bot
--------------------------------------------------------

Katcr also comes with a telegram bot entry point.

It's a simple bot that replies with search results for each message it gets.
It returns links to .torrent files from KAT.cr for the first page of results.

.. image:: http://i.imgur.com/qywHKHT.gif

Usage
+++++

::

    Telegram bot to query kat.cr

    Usage:
        katcr --token <BOT_TOKEN>

    Options:
        --token=<BOT_TOKEN> Telegram bot token

    Examples:
        katcr --token 123123:123123

I would recommend to read
`official documentation on setting up your own telegram bot <https://core.telegram.org/bots#6-botfather>`_
to **get the token**



\:star2\: Notes
----------------

This project is made with the best of intentions. For that times
you need to search for somethink shared as a torrent on KAT
(I.E, linux images).

Logo is based on robot cat by `Arsenty <https://thenounproject.com/arsenty/>`_

If you like this project, show its appreciation by starring it
