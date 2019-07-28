import asyncio
import pytest
from platform import system as get_os_family
from unittest.mock import MagicMock, call

from sanic_devtools.watch import AppTask, WatchTask


non_windows_test = pytest.mark.skipif(
    get_os_family() == 'Windows',
    reason='This only works under UNIX-based OS and gets stuck under Windows',
)


def create_awatch_mock(*results):
    results = results or [{('x', '/path/to/file')}]

    class awatch_mock:
        def __init__(self, path, **kwargs):
            self._result = iter(results)

        def __aiter__(self):
            return self

        async def __anext__(self):
            try:
                return next(self._result)
            except StopIteration:
                raise StopAsyncIteration
    return awatch_mock


async def test_watch_task(loop):
    class TestWatchTask(WatchTask):
        async def _run(self):
            await asyncio.sleep(0.001)
    task = TestWatchTask(MagicMock(), loop)
    await task.start(MagicMock())
    await task.close()


async def test_single_file_change(loop, mocker):
    mocked_awatch = mocker.patch('sanic_devtools.watch.awatch')
    mocked_awatch.side_effect = create_awatch_mock()

    app_task = AppTask(MagicMock(), loop)
    app_task._start_dev_server = MagicMock()
    app_task._stop_dev_server = MagicMock()
    app_task._app = MagicMock()
    await app_task._run()
    assert app_task._start_dev_server.call_count == 1
    assert app_task._stop_dev_server.called is False
    await app_task._session.close()


async def test_multiple_file_change(loop, mocker):
    mocked_awatch = mocker.patch('sanic_devtools.watch.awatch')
    mocked_awatch.side_effect = create_awatch_mock({('x', '/path/to/file'), ('x', '/path/to/file2')})
    app_task = AppTask(MagicMock(), loop)
    app_task._start_dev_server = MagicMock()
    app_task._stop_dev_server = MagicMock()

    app_task._app = MagicMock()
    await app_task._run()
    assert app_task._start_dev_server.call_count == 1
    await app_task._session.close()


class FakeProcess:
    def __init__(self, is_alive=True, exitcode=1, pid=123):
        self._is_alive = is_alive
        self.exitcode = exitcode
        self.pid = pid

    def is_alive(self):
        return self._is_alive

    def join(self, wait):
        pass


def test_stop_process_dead(smart_caplog, mocker):
    mock_kill = mocker.patch('sanic_devtools.watch.os.kill')
    mocker.patch('sanic_devtools.watch.awatch')
    app_task = AppTask(MagicMock(), MagicMock())
    app_task._process = MagicMock()
    app_task._process.is_alive = MagicMock(return_value=False)
    app_task._process.exitcode = 123
    app_task._stop_dev_server()
    assert 'server process already dead, exit code: 123' in smart_caplog
    assert mock_kill.called is False


def test_stop_process_clean(mocker):
    mock_kill = mocker.patch('sanic_devtools.watch.os.kill')
    mocker.patch('sanic_devtools.watch.awatch')
    app_task = AppTask(MagicMock(), MagicMock())
    app_task._process = MagicMock()
    app_task._process.is_alive = MagicMock(return_value=True)
    app_task._process.pid = 321
    app_task._process.exitcode = 123
    app_task._stop_dev_server()
    assert mock_kill.called_once_with(321, 2)


@non_windows_test  # There's no signals in Windows
def test_stop_process_dirty(mocker):
    mock_kill = mocker.patch('sanic_devtools.watch.os.kill')
    mocker.patch('sanic_devtools.watch.awatch')
    app_task = AppTask(MagicMock(), MagicMock())
    app_task._process = MagicMock()
    app_task._process.is_alive = MagicMock(return_value=True)
    app_task._process.pid = 321
    app_task._process.exitcode = None
    app_task._stop_dev_server()
    assert mock_kill.call_args_list == [
        call(321, 2),
        call(321, 9),
    ]
