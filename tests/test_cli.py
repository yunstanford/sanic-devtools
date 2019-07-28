import asyncio
import pathlib

from click.testing import CliRunner

from sanic_devtools.cli import cli
from sanic_devtools.exceptions import SanicDevException


def test_cli_help():
    runner = CliRunner()
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'runserver  Run a development server for an Sanic app.' in result.output


def test_runserver(mocker):
    mock_run_app = mocker.patch('sanic_devtools.cli.run_app')
    mock_runserver = mocker.patch('sanic_devtools.cli._runserver')
    runner = CliRunner()
    result = runner.invoke(cli, ['runserver', '.'])
    assert result.exit_code == 0, result.output
    assert '' == result.output
    assert mock_run_app.call_count == 1
    assert mock_runserver.call_count == 1


def test_runserver_error(mocker):
    mock_run_app = mocker.patch('sanic_devtools.cli.run_app')
    mock_run_app.side_effect = SanicDevException('foobar')
    mock_runserver = mocker.patch('sanic_devtools.cli._runserver')
    runner = CliRunner()
    result = runner.invoke(cli, ['runserver', '.'])
    assert result.exit_code == 2
    assert 'Error: foobar\n' == result.output
    assert mock_run_app.call_count == 1
    assert mock_runserver.call_count == 1


def test_runserver_error_verbose(mocker):
    mock_run_app = mocker.patch('sanic_devtools.cli.run_app')
    mock_run_app.side_effect = SanicDevException('foobar')
    mock_runserver = mocker.patch('sanic_devtools.cli._runserver')
    runner = CliRunner()
    result = runner.invoke(cli, ['runserver', '.', '--verbose'])
    assert result.exit_code == 2
    assert 'Error: foobar\n' in result.output
    assert 'sanic_devtools.exceptions.SanicDevException: foobar' in result.output
    assert mock_run_app.call_count == 1
    assert mock_runserver.call_count == 1


def test_runserver_no_args(loop):
    asyncio.set_event_loop(loop)
    runner = CliRunner()
    result = runner.invoke(cli, ['runserver'])
    assert result.exit_code == 2
    assert result.output.startswith('Error: unable to find a recognised default file')
