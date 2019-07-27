import asyncio
from asyncio import Protocol
from ssl import SSLContext
from sanic.server import serve, HttpProtocol
from typing import Any, Optional, Type, Union


class AppRunner:

    def __init__(
        self,
        app,
        host: str,
        port: int,
        debug: bool=False,
        ssl: Union[dict, SSLContext, None]=None,
        workers: int=1,
        protocol: Type[Protocol]=None,
        backlog: int=100,
        register_sys_signals: bool=True,
        access_log: Optional[bool]=None,
        run_async: bool=True,
        loop: asyncio.AbstractEventLoop=None):

        self.app = app
        self.host = host
        self.port = port
        self.loop = loop or asyncio.get_event_loop()

        if access_log is not None:
            self.app.config.ACCESS_LOG = access_log

        self.server_settings = self.app._helper(
            host=host,
            port=port,
            debug=debug,
            ssl=ssl,
            workers=workers,
            protocol=(protocol or HttpProtocol),
            backlog=backlog,
            register_sys_signals=register_sys_signals,
            loop=self.loop,
            run_async=run_async,
        )
        # states
        self.server = None
        self.closed = None
        self.is_running = False

    @property
    def before_start_events(self):
        return self.server_settings.get("before_start", [])

    @property
    def after_start_events(self):
        return self.server_settings.get("after_start", [])

    @property
    def before_stop_events(self):
        return self.server_settings.get("before_stop", [])

    @property
    def after_stop_events(self):
        return self.server_settings.get("after_stop", [])

    async def trigger_events(self, events):
        await self.app.trigger_events(events, self.loop)

    async def start(self):
        # Trigger before_start events
        await self.trigger_events(self.before_start_events)
        self.server = await serve(**self.server_settings)
        self.is_running = True
        self.app.is_running = True

        # Trigger after_start events
        await self.trigger_events(self.after_start_events)

    async def close(self):
        """
        Close server.
        """
        if not self.is_running or self.closed:
            return

        # Trigger before_stop events
        await self.trigger_events(self.before_stop_events)

        # Stop Server
        self.server.close()
        await self.server.wait_closed()

        # Trigger after_stop events
        await self.trigger_events(self.after_stop_events)

        self.closed = True
        self.is_running = False
        self.app.is_running = False
    