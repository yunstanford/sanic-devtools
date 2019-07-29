import sys
import traceback
from pathlib import Path
from cookiecutter.main import cookiecutter

import click

from .exceptions import SanicDevException
from .log import main_logger, setup_logging
from .config import INFER_HOST, DEFAULT_PORT
from .main import runserver as _runserver
from .main import run_app
from .version import VERSION


DEFAULT_COOKIECUTTER_SRC = "https://github.com/harshanarayana/cookiecutter-sanic.git"


_dir_existing = click.Path(exists=True, dir_okay=True, file_okay=False)
_file_dir_existing = click.Path(exists=True, dir_okay=True, file_okay=True)
_dir_may_exist = click.Path(dir_okay=True, file_okay=False, writable=True, resolve_path=True)


@click.group()
@click.version_option(VERSION, '-V', '--version', prog_name='sanic-devtools')
def cli():
    pass


verbose_help = 'Enable verbose output.'
root_help = 'Root directory project used to qualify other paths. env variable: AIO_ROOT'
host_help = ('host used when referencing livereload and static files, if blank host is taken from the request header '
             'with default of localhost. env variable AIO_HOST')
app_factory_help = ('name of the app factory to create an sanic.app.Sanic with, if missing default app-factory '
                    'names are tried. This can be either a function with signature '
                    '"def create_app(loop): -> Application" or "def create_app(): -> Application" '
                    'or just an instance of sanic.app.Sanic. env variable AIO_APP_FACTORY')
port_help = 'Port to serve app from, default 8000. env variable: AIO_PORT'
aux_port_help = 'Port to serve auxiliary app (reload, etc.) on, default port + 1. env variable: AIO_AUX_PORT'
protocol_help = 'app web protocol, HttpProtocol or WebSocketProtocol'
backlog_help = 'a number of unaccepted connections that the system will allow before refusing new connections'
workers_help = 'sanic workers that will be spawned'
access_log_help = 'Enables writing access logs'
template_src_help = 'provide your own cookiecutter template src, otherwise the default one will be used'
output_dir_help = 'where to output the generated sanic project dir into'


# defaults are all None here so default settings are defined in one place: DEV_DICT validation
@cli.command()
@click.argument('app-path', envvar='AIO_APP_PATH', type=_file_dir_existing, required=False)
@click.option('--root', 'root_path', envvar='AIO_ROOT', type=_dir_existing, help=root_help)
@click.option('--host', default=INFER_HOST, help=host_help)
@click.option('--app-factory', 'app_factory_name', envvar='AIO_APP_FACTORY', help=app_factory_help)
@click.option('-p', '--port', 'main_port', default=DEFAULT_PORT, envvar='AIO_PORT', type=click.INT, help=port_help)
@click.option('--aux-port', 'aux_port', envvar='AIO_AUX_PORT', type=click.INT, help=aux_port_help)
@click.option('--protocol', 'protocol', envvar='PROTOCOL', default='http', help=protocol_help)
@click.option('--backlog', 'backlog', envvar='BACKLOG', default=100, type=click.INT, help=backlog_help)
@click.option('--workers', 'workers', envvar='WORKERS', default=1, type=click.INT, help=workers_help)
@click.option('--access-log', is_flag=True, help=access_log_help)
@click.option('-v', '--verbose', is_flag=True, help=verbose_help)
def runserver(**config):
    """
    Run a development server for an Sanic app.

    Takes one argument "app-path" which should be a path to either a directory containing a recognized default file
    ("app.py" or "main.py") or to a specific file. Defaults to the environment variable "AIO_APP_PATH" or ".".

    The app path is run directly, see the "--app-factory" option for details on how an app is loaded from a python
    module.
    """
    active_config = {k: v for k, v in config.items() if v is not None}
    setup_logging(config['verbose'])
    try:
        run_app(*_runserver(**active_config))
    except SanicDevException as e:
        if config['verbose']:
            tb = click.style(traceback.format_exc().strip('\n'), fg='white', dim=True)
            main_logger.warning('SanicDevException traceback:\n%s', tb)
        main_logger.error('Error: %s', e)
        sys.exit(2)


@cli.command()
@click.option('--template-src', 'template_src', default=DEFAULT_COOKIECUTTER_SRC, envvar='SANIC_TEMPLATE_SRC', help=template_src_help)
@click.option('--output-dir', 'output_dir', default='.', envvar='SANIC_APP_OUTPUT_DIR', help=output_dir_help)
@click.option('-v', '--verbose', is_flag=True, help=verbose_help)
def new(**config):
    """
    Creates a new sanic project with batteries included.


    """
    active_config = {k: v for k, v in config.items() if v is not None}
    setup_logging(config['verbose'])
    try:
        cookiecutter(active_config["template_src"], output_dir=active_config["output_dir"])
    except SanicDevException as e:
        if config['verbose']:
            tb = click.style(traceback.format_exc().strip('\n'), fg='white', dim=True)
            main_logger.warning('SanicDevException traceback:\n%s', tb)
        main_logger.error('Error: %s', e)
        sys.exit(2)
