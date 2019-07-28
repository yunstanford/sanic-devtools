import asyncio
import json
import os
import signal
import time
from multiprocessing import Process
from unittest import mock

import aiohttp
import pytest
from sanic import Sanic
from pytest_toolbox import mktree

from sanic_devtools.main import run_app, runserver
from sanic_devtools.config import Config
from sanic_devtools.serve import create_auxiliary_app, start_main_app

from .conftest import SIMPLE_APP


@pytest.mark.boxed
def test_start_runserver_app_instance(tmpworkdir):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    mktree(tmpworkdir, SIMPLE_APP)
    aux_app, aux_port, _ = runserver(app_path='app.py', host='foobar.com')
    assert isinstance(aux_app, Sanic)
    assert aux_port == 8001
    assert len(aux_app.listeners["after_server_start"]) == 1
    assert len(aux_app.listeners["before_server_stop"]) == 1


def kill_parent_soon(pid):
    time.sleep(0.2)
    os.kill(pid, signal.SIGINT)


@pytest.mark.boxed
def test_run_app(loop, unused_port):
    app = Sanic()
    Process(target=kill_parent_soon, args=(os.getpid(),)).start()
    run_app(app, unused_port, loop)


@pytest.mark.boxed
async def test_run_app_sanic_client(tmpworkdir, sanic_client):
    mktree(tmpworkdir, SIMPLE_APP)
    config = Config(app_path='app.py')
    app_factory = config.import_app_factory()
    app = app_factory()
    assert isinstance(app, Sanic)
    cli = await sanic_client(app)
    r = await cli.get('/')
    assert r.status == 200
    text = await r.text()
    assert text == 'hello world'


async def test_aux_app(tmpworkdir, sanic_client):
    mktree(tmpworkdir, {
        'test.txt': 'test value',
    })
    app = create_auxiliary_app()
    cli = await sanic_client(app)
    r = await cli.get('/')
    assert r.status == 200


@pytest.mark.boxed
async def test_serve_main_app(tmpworkdir, loop):
    mktree(tmpworkdir, SIMPLE_APP)
    config = Config(app_path='app.py')
    runner = await start_main_app(config, config.import_app_factory(), loop)
    assert runner.is_running == True
    await runner.close()
