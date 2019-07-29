sanic-devtools
==============

.. start-badges

.. list-table::
    :stub-columns: 1

    * - Build
      - | |travis| |codecov|
    * - Package
      - | |version| |wheel| |supported-versions| |supported-implementations|

.. |travis| image:: https://travis-ci.org/yunstanford/sanic-devtools.svg?branch=master
    :alt: Travis-CI Build Status
    :target: https://travis-ci.org/yunstanford/sanic-devtools

.. |codecov| image:: https://codecov.io/gh/yunstanford/sanic-devtools/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/yunstanford/sanic-devtools

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
      new        Creates a new sanic project with batteries included.
      runserver  Run a development server for an Sanic app.


Usage
-----

``sanic-devtools`` provides several commands to help you develop Sanic Application easily.


runserver
~~~~~~~~~

Provides a simple local server for running your application while you're developing, it helps you live reload your Sanic
application automatically while developing and having any code change.

.. code:: shell

    sdev runserver <app-path>


``app-path`` can be a path to either a directory containing a recognized default file (app.py or main.py) or to a specific file.
The ``--app-factory`` option can be used to define which method is called from the app path file,
if not supplied some default method names are tried (``app/app_factory/get_app/create_app``).

All runserver arguments can be set via environment variables.


For more details, try:

.. code:: shell

    sdev runserver --help

new
~~~

Creates a new sanic project with batteries included in seconds.

.. code:: shell

    sdev new --output-dir <project-output-path>


By default, ``sdev`` uses `cookiecutter-sanic <https://github.com/harshanarayana/cookiecutter-sanic>`_ as default template under the hood.
You may override it by passing ``--template-src`` option.

For more details, try:

.. code:: shell

    sdev new --help


Also feel free to add any tool/command that helps developing ``Sanic`` application smoothly, just create a PR/issue and let us know !


Contributing
------------

``sanic-devtools`` accepts contributions on GitHub, in the form of issues or pull requests.

Run unit tests.

.. code:: shell
    
    tox -e py36

or 

.. code:: shell
    
    ./uranium test

Test command locally.

.. code:: shell

    ./uranium
    ./bin/sdev runserver ./example/app.py
