import pytest
from sanic import Sanic
from pytest_toolbox import mktree

from sanic_devtools.exceptions import SanicDevConfigError
from sanic_devtools.config import Config

from .conftest import SIMPLE_APP


async def test_load_simple_app(tmpworkdir):
    mktree(tmpworkdir, SIMPLE_APP)
    Config(app_path='app.py')


async def test_create_app_wrong_name(tmpworkdir, loop):
    mktree(tmpworkdir, SIMPLE_APP)
    config = Config(app_path='app.py', app_factory_name='missing')
    with pytest.raises(SanicDevConfigError) as excinfo:
        config.import_app_factory()
    assert excinfo.value.args[0] == 'Module "app.py" does not define a "missing" attribute/class'


async def test_no_loop_coroutine(tmpworkdir):
    mktree(tmpworkdir, SIMPLE_APP)
    config = Config(app_path='app.py')
    app = await config.load_app(config.import_app_factory())
    assert isinstance(app, Sanic)


async def test_not_app(tmpworkdir):
    mktree(tmpworkdir, {
        'app_not_sanic.py': """\
def app_factory():
    return 123
"""
    })
    config = Config(app_path='app_not_sanic.py')
    with pytest.raises(SanicDevConfigError):
        await config.load_app(config.import_app_factory())
