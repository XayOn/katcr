.. image:: http://i.imgur.com/ofx75lO.png
   :align: center


.. image:: https://travis-ci.org/XayOn/katcr.svg?branch=master
    :target: https://travis-ci.org/XayOn/katcr

.. image:: https://coveralls.io/repos/github/XayOn/katcr/badge.svg?branch=master
    :target: https://coveralls.io/github/XayOn/katcr?branch=master

.. image:: https://badge.fury.io/py/katcr.svg
    :target: https://badge.fury.io/py/katcr


\:tv\: Multi-site torrent search
=================================

Easily **search torrents** in multiple providers.


Command Line Interface
----------------------

katcr comes with a simple but powerful command line interface


.. image:: https://raw.githubusercontent.com/XayOn/katcr/master/screenshot.png

::

    Search in multiple torrent sites.

        Usage: katcr [options] <SEARCH_TERM>

        Options:
            --search=<SEARCH_TERM>             Search term(s)
            --pages=<PAGES_NUM>                Number of pages to lookup
            -i --interactive                   Enable interactive menu
            -p --plugin=<Katcr|ThePirateBay>   Download method [default: Katcr]
            -e --enable-shortener              Enable url shortener
            -s --sortener=<SHORTENER_URL>      Use given magnet shortener
                                               [default: http://www.shortmag.net]
            -h --help                          Show this screen
            -o --open                          Launch with default torrent app
            -d                                 Debug mode.



Installation
--------------

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
