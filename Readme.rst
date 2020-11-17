.. image:: http://i.imgur.com/ofx75lO.png

CLI client to torrent searches and streaming. Easily **search torrents** in
multiple providers such as KickAssTorrents and ThePirateBay.

|pypi| |release| |downloads| |python_versions| |pypi_versions| |coverage| |actions|

.. |pypi| image:: https://img.shields.io/pypi/l/katcr
.. |release| image:: https://img.shields.io/librariesio/release/pypi/katcr
.. |downloads| image:: https://img.shields.io/pypi/dm/katcr
.. |python_versions| image:: https://img.shields.io/pypi/pyversions/katcr
.. |pypi_versions| image:: https://img.shields.io/pypi/v/katcr
.. |actions| image:: https://travis-ci.org/XayOn/katcr.svg?branch=master
    :target: https://travis-ci.org/XayOn/katcr


Command Line Interface
----------------------

katcr comes with a simple but powerful command line interface

.. image:: /docs/screenshot.gif?raw=True

::

   > poetry run katcr search ...

   USAGE
     katcr search [--pages <...>] [--token [<...>]] [--shortener [<...>]] [--engines <...>] [--interactive [<...>]] [--open [<...>]] <search>

   ARGUMENTS
     <search>               Search term

   OPTIONS
     --pages                Pages to search on search engines (default: "1")
     --token                Token to use on URL shortener as AUTH
     --shortener            URL Shortener
     --engines              Engines (default: "Katcr,ThePirateBay,NyaaSi,Skytorrents")
     --interactive          Allow the user to choose a specific magnet
     --open                 Open selected magnet with xdg-open

   GLOBAL OPTIONS
     -h (--help)            Display this help message
     -q (--quiet)           Do not output any message
     -v (--verbose)         Increase the verbosity of messages: "-v" for normal output, "-vv" for more verbose output and "-vvv" for debug
     -V (--version)         Display this application version
     --ansi                 Force ANSI output
     --no-ansi              Disable ANSI output
     -n (--no-interaction)  Do not ask any interactive question


Installation
------------

This is a python package available on pypi, just run::

    sudo python3 -m pip install katcr


Features
--------

- Display results in a nice utf-8 table
- Optional interactive mode, choose and open torrent with a nice text user interface
- Open torrent directly with your preferred client (via xdg-open)
- Stream torrent with `torrentstream <https://github.com/XayOn/torrentstream>`_
- Searches on all available engines until it gets results by default.
- Search torrents in:

  + Eztv
  + `Jackett <https://github.com/Jackett/Jackett>`_
  + Katcr
  + NyaaSi
  + Skytorrents
  + ThePirateBay


Jackett Support
---------------

You can easily use a `Jackett <https://github.com/Jackett/Jackett>`_ instance
to search on all your configured provider.

This allows you to search on any jackett-supported site (that's about supported
300 trackers).

Jackett is probably the best way to use katcr and katbot, as it has a more
active mantainance of the tracker sites that us.

To enable Jackett use, simply export your jackett URL and TOKEN as variables::

   JACKETT_HOST=http://127.0.0.1:9117 JACKETT_APIKEY=<redacted> poetry run katcr --engines=


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
