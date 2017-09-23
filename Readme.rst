.. image:: http://i.imgur.com/ofx75lO.png
   :align: center

Multi-site torrent search
=================================

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


.. image:: https://raw.githubusercontent.com/XayOn/katcr/master/screenshot.png

::

    Search in multiple torrent sites.

        Usage: katcr [options] [interactive options] <SEARCH_TERM>

        Currently available search engines:

        - Katcr
        - ThePirateBay

        Options:
            -e --search-engine=<SearchEngine>  Torrent search engine to use
                                               [default: Any].
            -p --pages=<PAGES_NUM>             Number of pages to lookup
                                               [default: 1]
            -d --disable-shortener             Disable url shortener
            -s --sortener=<SHORTENER_URL>      Use given magnet shortener to
                                               prettify urls.
                                               [default: http://www.shortmag.net]

        Interactive Options:
            -i --interactive                   Enable interactive mode
            -o --open                          Launch with default torrent app
                                               in interactive mode [default: True]
            -h --help                          Show this help screen
            -d --debug                         Enable debug mode


Installation
------------

This is a python package available on pypi.

On windows and mac `you can download python3.5 here <https://www.python.org/downloads/release/python-352/>`_.
On linux distros, python3.5 is already on most package managers :smile:

With python3.5 installed just execute::

    pip3.5 install katcr


If it asks about permissions and you don't know what to do, you should
probably read `Jamie Matthews's article about virtualenvs <https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/>`_


KATBot - Kickasstorrents telegram bot
--------------------------------------

Katcr also comes with a telegram bot entry point.

It's a simple bot that replies with search results for each message it gets.
It returns links to .torrent files from KAT.cr for the first page of results.

.. image:: http://i.imgur.com/7FxplBs.gif

::

    Run telegram bot.

        Usage: katcr_bot [options]

        Options:
            --token=<BOT_TOKEN>             Telegram bot token
            --shortener=<URL_SHORTENER>     Url shortener to use
                                        [default: http://shortmag.net]

Notes
------

This project is made with the best of intentions. For that times
you need to search for somethink shared as a torrent on KAT
(I.E, linux images). Logo is based on robot cat by
`Arsenty <https://thenounproject.com/arsenty/>`_

If you like this project, show its appreciation by starring it, if you're using
it and want to write to me personally, feel free to do so at
opensource@davidfrancos.net. If you've got a bug to report, please use the
github ticketing system
