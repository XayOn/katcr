.. image:: http://i.imgur.com/ofx75lO.png
   :align: center


.. image:: https://travis-ci.org/XayOn/katcr.svg?branch=master
    :target: https://travis-ci.org/XayOn/katcr

.. image:: https://coveralls.io/repos/github/XayOn/katcr/badge.svg?branch=master
    :target: https://coveralls.io/XayOn/katcr?branch=master

.. image:: https://badge.fury.io/py/katcr
    :target: https://badge.fury.io/py/katcr


\:tv\: Multi-site torrent search library | CommandLine | Telegram Bot
======================================================================

This is a simple **python library to search in kickasstorrents and thepiratebay**.
It's also a **telegram bot** and a **command line interface** :wink:

.. contents:: :local:


\:tv\: katcr - kickasstorrents command line interface
------------------------------------------------------

katcr comes with a simple but powerful command line interface, able to
return either magnets or torrents.

Usage
+++++

::

    Search in multiple torrent sites.

        Usage: katcr --plugin=<PLUGIN> [options] <SEARCH_TERM>

        Options:
    	--search=<SEARCH_TERM>   Search term(s)
    	--pages=<PAGES_NUM>      Number of pages to lookup
    	-i --interactive         Enable interactive menu
    	-p --plugin=<PLUGIN>     Plugin to use for search <Katcr|ThePirateBay>
    	-h --help                Show this screen
    	-o --open                Use xdg-open to launch the default torrent app


.. image:: http://i.imgur.com/gOo3mqf.gif


\:notebook\: Library Usage
---------------------------

You can directly import any ``plugin`` from the katcr library:

- ThePirateBay
- Katcr

Sample code for getting the first page of results from kickasstorrents::

    from katcr import Katcr
    print(Katcr().search("ubuntu", 1))


\:space_invader\: KATBot - Kickasstorrents telegram bot
--------------------------------------------------------

Katcr also comes with a telegram bot entry point.

It's a simple bot that replies with search results for each message it gets.
It returns links to .torrent files from KAT.cr for the first page of results.

.. image:: http://i.imgur.com/7FxplBs.gif

Usage
+++++

::

    Telegram bot to query kickasstorrents

    Usage:
        katcr_bot [options]

    Options:
        --token=<BOT_TOKEN> Telegram bot token

    Examples:
        katcr_bot --token 123123:123123


\:star\: Installation
---------------------

This is a python package available on pypi.

On windows and mac `you can download python3.5 here <https://www.python.org/downloads/release/python-352/>`_.
On linux distros, python3.5 is already on most package managers :smile:

With python3.5 installed just execute::

    pip3.5 install katcr


If it asks about permissions and you don't know what to do, you should
probably read `Jamie Matthews's article about virtualenvs <https://www.dabapps.com/blog/introduction-to-pip-and-virtualenv-python/>`_


\:star2\: Notes
----------------

This project is made with the best of intentions. For that times
you need to search for somethink shared as a torrent on KAT
(I.E, linux images). Logo is based on robot cat by
`Arsenty <https://thenounproject.com/arsenty/>`_

If you like this project, show its appreciation by starring it, if you're using
it and want to write to me personally, feel free to do so at
opensource@davidfrancos.net. If you've got a bug to report, please use the
github ticketing system
