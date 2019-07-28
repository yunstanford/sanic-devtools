import asyncio
import contextlib
import os
from multiprocessing import set_start_method

from .log import rs_dft_logger as logger
from .config import Config
from .runner import AppRunner
from .serve import HOST, check_port_open, create_auxiliary_app
from .watch import AppTask


def run_app(app, port, loop):
    runner = AppRunner(app, HOST, port, loop=loop)
    loop.run_until_complete(runner.start())

    try:
        loop.run_forever()
    except KeyboardInterrupt:  # pragma: no branch
        pass
    finally:
        logger.info('shutting down server...')
        start = loop.time()
        with contextlib.suppress(asyncio.TimeoutError, KeyboardInterrupt):
            loop.run_until_complete(runner.close())
        logger.debug('shutdown took %0.2fs', loop.time() - start)


def runserver(**config_kwargs):
    """
    Prepare app ready to run development server.

    :param config_kwargs: see config.Config for more details
    :return: tuple (auxiliary app, auxiliary app port, event loop)
    """
    # force a full reload in sub processes so they load an updated version of code, this must be called only once
    try:
        set_start_method('spawn')
    except RuntimeError as e:
        logger.warning(str(e))

    config = Config(**config_kwargs)
    config.import_app_factory()
    loop = asyncio.get_event_loop()

    loop.run_until_complete(check_port_open(config.main_port, loop))

    aux_app = create_auxiliary_app()

    main_manager = AppTask(config, loop)

    async def start(app, loop):
        await main_manager.start(app)

    async def close(app, loop):
        await main_manager.close(app)

    aux_app.register_listener(start, 'after_server_start')
    aux_app.register_listener(close, 'before_server_stop')

    url = 'http://{0.host}:{0.aux_port}'.format(config)
    logger.info('Starting aux server at %s ◆', url)

    return aux_app, config.aux_port, loop
