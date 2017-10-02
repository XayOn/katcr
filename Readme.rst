.. image:: http://i.imgur.com/ofx75lO.png

Easily **search torrents** in multiple providers such as KickAssTorrents and
ThePirateBay.


.. image:: https://travis-ci.org/XayOn/katcr.svg?branch=master
    :target: https://travis-ci.org/XayOn/katcr

.. image:: https://coveralls.io/repos/github/XayOn/katcr/badge.svg?branch=master
    :target: https://coveralls.io/github/XayOn/katcr?branch=master

.. image:: https://badge.fury.io/py/katcr.svg
    :target: https://badge.fury.io/py/katcr


Command Line Interface
----------------------

katcr comes with a simple but powerful command line interface

.. image:: https://raw.githubusercontent.com/XayOn/katcr/master/screenshot.gif

::

    Search in multiple torrent sites.

        Usage: katcr [options] [interactive options] <SEARCH_TERM>

        Currently available search engines:

        - Katcr
        - ThePirateBay
        - Nyaa
        - Skytorrents
        - Digbt

        Options:
            -e --search-engines=<SearchEngine>  Torrent search engine to use
                                                [default: All].
            -p --pages=<PAGES_NUM>              Number of pages to lookup
                                                [default: 1]
            -d --disable-shortener              Disable url shortener
            -s --shortener=<SHORTENER_URL>      Use given magnet shortener to
                                                prettify urls.
                                                [default: http://www.shortmag.net]
            -t --token=<SHORTENER_TOKEN>        Shortener token to use, if required
            -t --token_file=<S_TOKEN_FILE>      Shortener token file

        Interactive Options:
            -i --interactive                    Enable interactive mode
            -o --open                           Launch with default torrent app
                                                in interactive mode [default: True]
            -h --help                           Show this help screen
            -v --verbose                        Enable debug mode


        katcr  Copyright (C) 2017 David Francos Cuartero
        This program comes with ABSOLUTELY NO WARRANTY; This is free software, and
        you are welcome to redistribute it under certain conditions;


Installation
------------

This is a python package available on pypi, just run::

    sudo python3 -m pip install katcr


Features
--------

- Display results in a nice utf-8 table
- Optional interactive mode, choose and open torrent with a nice text user interface
- Open torrent directly with your preferred client (via xdg-open)
- Searches on all available engines until it gets results by default.
- Search torrents in:

  + Katcr
  + ThePirateBay
  + Nyaa
  + Skytorrents
  + Digbt



KATBot - Kickasstorrents telegram bot
--------------------------------------

Katcr also comes with a telegram bot entry point.
It's a simple bot that replies with search results for each message it gets.

It returns magnet links with provided url shortener for the first page of
results, on the first available search engine.

.. image:: http://i.imgur.com/7FxplBs.gif

::

    Run telegram bot.

        Usage: katcr_bot [options]

        Options:
            --token=<BOT_TOKEN>             Telegram bot token
            --token-file=<FILE>             Telegram bot token file
            --shortener=<URL_SHORTENER>     Url shortener to use
                                            [default: http://shortmag.net]


Notes
------

This project is made with the best of intentions.

For that times you need to search for somethink shared as a torrent on KAT
(I.E, linux images). Logo is based on robot cat by
`Arsenty <https://thenounproject.com/arsenty/>`_

If you like this project, show its appreciation by starring it, if you're using
it and want to write to me personally, feel free to do so at
opensource@davidfrancos.net. If you've got a bug to report, please use the
github ticketing system
