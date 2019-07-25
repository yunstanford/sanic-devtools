import asyncio
import contextlib
import os
from multiprocessing import set_start_method

from aiohttp.web_runner import AppRunner, TCPSite

from .log import rs_dft_logger as logger
from .config import Config
from .serve import HOST, check_port_open, create_auxiliary_app
from .watch import AppTask, LiveReloadTask


def run_app(app, port, loop):
    runner = AppRunner(app)
    loop.run_until_complete(runner.setup())

    site = TCPSite(runner, HOST, port, shutdown_timeout=0.01)
    loop.run_until_complete(site.start())

    try:
        loop.run_forever()
    except KeyboardInterrupt:  # pragma: no branch
        pass
    finally:
        logger.info('shutting down server...')
        start = loop.time()
        with contextlib.suppress(asyncio.TimeoutError, KeyboardInterrupt):
            loop.run_until_complete(runner.cleanup())
        logger.debug('shutdown took %0.2fs', loop.time() - start)


def runserver(**config_kwargs):
    """
    Prepare app ready to run development server.

    :param config_kwargs: see config.Config for more details
    :return: tuple (auxiliary app, auxiliary app port, event loop)
    """
    # force a full reload in sub processes so they load an updated version of code, this must be called only once
    set_start_method('spawn')

    config = Config(**config_kwargs)
    config.import_app_factory()
    loop = asyncio.get_event_loop()

    loop.run_until_complete(check_port_open(config.main_port, loop))

    aux_app = create_auxiliary_app(
        static_path=config.static_path_str,
        static_url=config.static_url,
        livereload=config.livereload,
    )

    main_manager = AppTask(config, loop)
    aux_app.on_startup.append(main_manager.start)
    aux_app.on_shutdown.append(main_manager.close)

    if config.static_path:
        static_manager = LiveReloadTask(config.static_path, loop)
        logger.debug('starting livereload to watch %s', config.static_path_str)
        aux_app.on_startup.append(static_manager.start)
        aux_app.on_shutdown.append(static_manager.close)

    url = 'http://{0.host}:{0.aux_port}'.format(config)
    logger.info('Starting aux server at %s ◆', url)

    if config.static_path:
        rel_path = config.static_path.relative_to(os.getcwd())
        logger.info('serving static files from ./%s/ at %s%s', rel_path, url, config.static_url)

    return aux_app, config.aux_port, loop
