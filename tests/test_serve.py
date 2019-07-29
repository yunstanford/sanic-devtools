import pytest
from pytest_toolbox import mktree
from sanic_devtools.config import Config
from sanic_devtools.serve import check_port_open, start_main_app
from sanic_devtools.exceptions import SanicDevException
from .conftest import SIMPLE_APP


async def test_check_port_open(unused_port, tmpworkdir, loop):
    try:
        mktree(tmpworkdir, SIMPLE_APP)
        config = Config(app_path='app.py')
        runner = await start_main_app(config, config.import_app_factory(), loop)
        assert runner.is_running == True
        with pytest.raises(Exception):
            await check_port_open(runner.port, loop, 0.01)
    finally:
        await runner.close()
