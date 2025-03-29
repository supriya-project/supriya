import asyncio
from collections.abc import Sequence as SequenceABC
from typing import Awaitable, Callable, Sequence

from ..enums import BootStatus
from ..typing import FutureLike, SupportsOsc
from .messages import OscMessage
from .protocols import (
    HealthCheck,
    OscCallback,
    OscProtocol,
    OscProtocolAlreadyConnected,
    osc_out_logger,
    osc_protocol_logger,
)


class AsyncOscProtocol(asyncio.DatagramProtocol, OscProtocol):
    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name: str | None = None,
        on_connect_callback: Callable | None = None,
        on_disconnect_callback: Callable | None = None,
        on_panic_callback: Callable | None = None,
    ) -> None:
        asyncio.DatagramProtocol.__init__(self)
        OscProtocol.__init__(
            self,
            name=name,
            on_connect_callback=on_connect_callback,
            on_disconnect_callback=on_disconnect_callback,
            on_panic_callback=on_panic_callback,
        )
        self.boot_future: asyncio.Future[bool] = asyncio.Future()
        self.exit_future: asyncio.Future[bool] = asyncio.Future()
        self.background_tasks: set[asyncio.Task] = set()
        self.healthcheck_task: asyncio.Task | None = None

    ### PRIVATE METHODS ###

    async def _disconnect(self, panicked: bool = False) -> None:
        super()._disconnect(panicked=panicked)
        self.transport.close()
        if self.healthcheck_task:
            self.healthcheck_task.cancel()
        await self._on_disconnect(
            boot_future=self.boot_future,
            exit_future=self.exit_future,
            panicked=panicked,
        )

    async def _on_connect(self, *, boot_future: FutureLike[bool]) -> None:
        super()._on_connect(boot_future=self.boot_future)
        if self.on_connect_callback:
            self.on_connect_callback()

    async def _on_disconnect(
        self,
        *,
        boot_future: FutureLike[bool],
        exit_future: FutureLike[bool],
        panicked: bool = False,
    ) -> None:
        super()._on_disconnect(
            boot_future=boot_future,
            exit_future=exit_future,
            panicked=panicked,
        )
        if panicked and self.on_panic_callback:
            self.on_panic_callback()
        elif not panicked and self.on_disconnect_callback:
            self.on_disconnect_callback()

    async def _on_healthcheck_passed(self, message: OscMessage) -> None:
        super()._on_healthcheck_passed(message)
        if self.status == BootStatus.BOOTING:
            await self._on_connect(boot_future=self.boot_future)

    async def _run_healthcheck(self) -> None:
        if self.healthcheck is None:
            return
        while self.status in (BootStatus.BOOTING, BootStatus.ONLINE):
            if self.attempts >= self.healthcheck.max_attempts:
                await self._disconnect(panicked=True)
                return
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
                "healthcheck: checking ..."
            )
            self.send(OscMessage(*self.healthcheck.request_pattern))
            sleep_time = self.healthcheck.timeout * pow(
                self.healthcheck.backoff_factor, self.attempts
            )
            self.attempts += 1
            await asyncio.sleep(sleep_time)

    ### OVERRIDES ###

    def connection_made(self, transport) -> None:
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            "connection made!"
        )
        self.transport = transport

    def connection_lost(self, exc) -> None:
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            "connection lost!"
        )

    def datagram_received(self, data, addr) -> None:
        loop = asyncio.get_running_loop()
        for callback, message in self._validate_receive(data):
            if asyncio.iscoroutine(
                result := callback.procedure(
                    message, *(callback.args or ()), **(callback.kwargs or {})
                )
            ):
                self.background_tasks.add(task := loop.create_task(result))
                task.add_done_callback(self.background_tasks.discard)

    def error_received(self, exc) -> None:
        osc_out_logger.warning(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            f"errored: {exc}"
        )

    ### PUBLIC METHODS ###

    def activate_healthcheck(self) -> None:
        if self._activate_healthcheck():
            self.healthcheck_task = asyncio.get_running_loop().create_task(
                self._run_healthcheck()
            )

    async def connect(
        self, ip_address: str, port: int, *, healthcheck: HealthCheck | None = None
    ):
        if self.status != BootStatus.OFFLINE:
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
                "already connected!"
            )
            raise OscProtocolAlreadyConnected
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            "connecting ..."
        )
        self._setup(ip_address, port, healthcheck)
        loop = asyncio.get_running_loop()
        self.boot_future = loop.create_future()
        self.exit_future = loop.create_future()
        _, protocol = await loop.create_datagram_endpoint(
            lambda: self, remote_addr=(ip_address, port)
        )
        if self.healthcheck and self.healthcheck.active:
            self.healthcheck_task = loop.create_task(self._run_healthcheck())
        elif not self.healthcheck:
            await self._on_connect(boot_future=self.boot_future)

    async def disconnect(self) -> None:
        if self.status != BootStatus.ONLINE:
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
                "already disconnected!"
            )
            return
        await self._disconnect()

    def register(
        self,
        pattern: Sequence[float | str],
        procedure: Callable[[OscMessage], Awaitable[None] | None],
        *,
        failure_pattern: Sequence[float | str] | None = None,
        once: bool = False,
        args: tuple | None = None,
        kwargs: dict | None = None,
    ) -> OscCallback:
        """
        Register a callback.
        """
        self._add_callback(
            callback := self._register(
                pattern,
                procedure,
                failure_pattern=failure_pattern,
                once=once,
                args=args,
                kwargs=kwargs,
            )
        )
        return callback

    def send(self, message: SequenceABC | SupportsOsc | str) -> None:
        self.transport.sendto(self._send(message))

    def unregister(self, callback: OscCallback) -> None:
        self._remove_callback(callback)
