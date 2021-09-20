import asyncio
from asyncio import AbstractEventLoop
from typing import Callable, List, Union

import aiomatrix


class Executor:
    def __init__(self, client: 'aiomatrix.Aiomatrix', loop: AbstractEventLoop = None):
        if loop is not None:
            self._loop = loop
        self.client = client
        self._on_startup = []
        self._on_shutdown = []

    @property
    def loop(self) -> asyncio.AbstractEventLoop:
        return getattr(self, '_loop', asyncio.get_event_loop())

    def on_startup(self, callback: Union[Callable, List[Callable]]):
        if not isinstance(callback, Callable):
            return
        if isinstance(callback, list):
            for cb in callback:
                self.on_startup(cb)
            return
        self._on_startup.append(callback)

    def on_shutdown(self, callback: Union[Callable, List[Callable]]):
        if not isinstance(callback, Callable):
            return
        if isinstance(callback, list):
            for cb in callback:
                self.on_shutdown(cb)
            return
        self._on_shutdown.append(callback)

    def start_polling(self, ignore_errors: bool = True, timeout: int = 10, sleep: float = 0.1):
        loop: AbstractEventLoop = self.loop

        try:
            loop.run_until_complete(self._start_polling())
            loop.create_task(self.client.run(ignore_errors, timeout, sleep))
            loop.run_forever()
        except (KeyboardInterrupt, SystemExit):
            # loop.stop()
            pass
        finally:
            loop.run_until_complete(self._shutdown_polling())

    async def _start_polling(self):
        for cb in self._on_startup:
            await cb(self.client)

    async def _shutdown_polling(self):
        for cb in self._on_shutdown:
            await cb(self.client)
