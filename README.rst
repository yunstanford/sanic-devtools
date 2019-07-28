sanic-devtools
==============

.. start-badges

.. list-table::
    :stub-columns: 1

    * - Build
      - | |travis| |coverage|
    * - Package
      - | |version| |wheel| |supported-versions| |supported-implementations|

.. |travis| image:: https://travis-ci.org/yunstanford/sanic-devtools.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/yunstanford/sanic-devtools

.. |coverage| image:: https://coveralls.io/repos/github/yunstanford/sanic-devtools/badge.svg?branch=master
    :alt: coverage status
    :target: https://coveralls.io/github/yunstanford/sanic-devtools?branch=master

.. |version| image:: https://img.shields.io/pypi/v/sanic-devtools.svg
    :alt: PyPI Package latest release
    :target: https://pypi.python.org/pypi/sanic-devtools

.. |wheel| image:: https://img.shields.io/pypi/wheel/sanic-devtools.svg
    :alt: PyPI Wheel
    :target: https://pypi.python.org/pypi/sanic-devtools

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/sanic-devtools.svg
    :alt: Supported versions
    :target: https://pypi.python.org/pypi/sanic-devtools

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/sanic-devtools.svg
    :alt: Supported implementations
    :target: https://pypi.python.org/pypi/sanic-devtools

.. end-badges


Dev tools for Sanic.

This tool is highly inspired by `aiohttp-devtools <https://github.com/aio-libs/aiohttp-devtools>`_, `aio-libs <https://github.com/aio-libs>`_.


Installation
------------

.. code:: shell

    pip install sanic-devtools


Quick Start
-----------

.. code:: shell
    
    ⋊> ~ sdev --help

    Usage: sdev [OPTIONS] COMMAND [ARGS]...

    Options:
      -V, --version  Show the version and exit.
      --help         Show this message and exit.

    Commands:
      runserver  Run a development server for an Sanic app.


Usage
-----

The `sanic-devtools` provides several commands to help you develop Sanic Application easily.


runserver
~~~~~~~~~

Provides a simple local server for running your application while you're developing, it helps you live reload your Sanic
application automatically while developing and having any code change.

.. code:: shell

    adev runserver <app-path>

new
~~~

[TODO]


Also feel free to add any tool/command that could help developing `Sanic` application smoothly, just create a PR/ßissue and let us know !


Contributing
------------

`sanic-devtools` accepts contributions on GitHub, in the form of issues or pull requests.

Run unit tests.

.. code:: shell
    
    tox -e py36

or 

.. code:: shell
    
    ./uranium test
