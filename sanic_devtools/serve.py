import asyncio
import contextlib
import json
import mimetypes
import sys
from pathlib import Path
from typing import Optional

from sanic.app import Sanic
from sanic.server import serve, HttpProtocol
from sanic.websocket import WebSocketProtocol

from aiohttp import WSMsgType, web
from aiohttp.hdrs import LAST_MODIFIED
from aiohttp.web import FileResponse, Response
from aiohttp.web_exceptions import HTTPNotFound, HTTPNotModified
from aiohttp.web_urldispatcher import StaticResource
from yarl import URL

from .exceptions import SanicDevException
from .log import rs_aux_logger as aux_logger
from .log import rs_dft_logger as dft_logger
from .log import setup_logging
from .config import Config


HOST = '127.0.0.1'


async def check_port_open(port, loop, delay=1):
    # the "s = socket.socket; s.bind" approach sometimes says a port is in use when it's not
    # this approach replicates aiohttp so should always give the same answer
    for i in range(5, 0, -1):
        try:
            server = await loop.create_server(asyncio.Protocol(), host=HOST, port=port)
        except OSError as e:
            if e.errno != 98:  # pragma: no cover
                raise
            dft_logger.warning('port %d is already in use, waiting %d...', port, i)
            await asyncio.sleep(delay, loop=loop)
        else:
            server.close()
            await server.wait_closed()
            return
    raise SanicDevException('The port {} is already is use'.format(port))


@contextlib.contextmanager
def set_tty(tty_path):  # pragma: no cover
    try:
        if not tty_path:
            # to match OSError from open
            raise OSError()
        with open(tty_path) as tty:
            sys.stdin = tty
            yield
    except OSError:
        # either tty_path is None (windows) or opening it fails (eg. on pycharm)
        yield


def serve_main_app(config: Config, tty_path: Optional[str]):
    with set_tty(tty_path):
        setup_logging(config.verbose)
        app_factory = config.import_app_factory()
        loop = asyncio.get_event_loop()
        runner = loop.run_until_complete(start_main_app(config, app_factory, loop))
        try:
            loop.run_forever()
        except KeyboardInterrupt:  # pragma: no cover
            pass
        finally:
            with contextlib.suppress(asyncio.TimeoutError, KeyboardInterrupt):
                loop.run_until_complete(runner.cleanup())


async def trigger_events(events, loop):
    """Trigger events (functions or async)
    :param events: one or more sync or async functions to execute
    :param loop: event loop
    """
    for event in events:
        result = event(loop)
        if isawaitable(result):
            await result


# TODO: Add Sanic Runner Wrapper
async def start_main_app(config: Config, app_factory, loop):
    app = await config.load_app(app_factory)

    await check_port_open(config.main_port, loop)
    
    # server settings
    server_settings = app._helper(
        host=config.host, port=config.main_port,
        loop=loop, protocol=config.protocol,
        backlog=config.backlog, run_async=True)

    # start app in async way


    return runner


def create_auxiliary_app():
    app = Sanic("SANIC_DEV_AUX_APP")
    return app


def _get_protocol(protocol: str):
    return WebSocketProtocol if protocol == "websocket" else HttpProtocol
