import asyncio
import collections
import dataclasses
import logging
import queue
import socketserver
import threading
import time
from typing import Any, Callable, Dict, NamedTuple, Optional, Set, Tuple, Union

from .captures import Capture, CaptureEntry
from .messages import OscBundle, OscMessage


osc_in_logger = logging.getLogger("supriya.osc.in")
osc_out_logger = logging.getLogger("supriya.osc.out")
udp_in_logger = logging.getLogger("supriya.udp.in")
udp_out_logger = logging.getLogger("supriya.udp.out")


class OscProtocolOffline(Exception):
    pass


class OscProtocolAlreadyConnected(Exception):
    pass


class OscCallback(NamedTuple):
    pattern: Tuple[Union[str, int, float], ...]
    procedure: Callable
    failure_pattern: Optional[Tuple[Union[str, int, float], ...]] = None
    once: bool = False


@dataclasses.dataclass
class HealthCheck:
    request_pattern: str
    response_pattern: str
    callback: Callable
    timeout: float = 1.0
    backoff_factor: float = 1.5
    max_attempts: int = 5


class OscProtocol:

    ### INITIALIZER ###

    def __init__(self):
        self.callbacks: Dict[Any, Any] = {}
        self.captures: Set[Capture] = set()
        self.healthcheck = None
        self.healthcheck_osc_callback = None
        self.attempts = 0
        self.ip_address = None
        self.is_running: bool = False
        self.port = None

    ### PRIVATE METHODS ###

    def _add_callback(self, callback: OscCallback):
        patterns = [callback.pattern]
        if callback.failure_pattern:
            patterns.append(callback.failure_pattern)
        for pattern in patterns:
            callback_map = self.callbacks
            for item in pattern:
                callbacks, callback_map = callback_map.setdefault(item, ([], {}))
            callbacks.append(callback)

    def _match_callbacks(self, message):
        items = (message.address,) + message.contents
        matching_callbacks = []
        callback_map = self.callbacks
        for item in items:
            if item not in callback_map:
                break
            callbacks, callback_map = callback_map[item]
            matching_callbacks.extend(callbacks)
        for callback in matching_callbacks:
            if callback.once:
                self.unregister(callback)
        return matching_callbacks

    def _remove_callback(self, callback: OscCallback):
        def delete(pattern, original_callback_map):
            key = pattern.pop(0)
            if key not in original_callback_map:
                return
            callbacks, callback_map = original_callback_map[key]
            if pattern:
                delete(pattern, callback_map)
            if callback in callbacks:
                callbacks.remove(callback)
            if not callbacks and not callback_map:
                original_callback_map.pop(key)

        patterns = [callback.pattern]
        if callback.failure_pattern:
            patterns.append(callback.failure_pattern)
        for pattern in patterns:
            delete(list(pattern), self.callbacks)

    def _reset_attempts(self, message):
        self.attempts = 0

    def _setup(self, ip_address, port, healthcheck):
        self.ip_address = ip_address
        self.port = port
        self.healthcheck = healthcheck
        if self.healthcheck:
            self.healthcheck_osc_callback = self.register(
                pattern=self.healthcheck.response_pattern,
                procedure=self._reset_attempts,
            )

    def _teardown(self):
        self.is_running = False
        if self.healthcheck:
            self.unregister(self.healthcheck_osc_callback)

    def _validate_callback(
        self, pattern, procedure, *, failure_pattern=None, once=False,
    ):
        if isinstance(pattern, (str, int, float)):
            pattern = [pattern]
        if isinstance(failure_pattern, (str, int, float)):
            failure_pattern = [failure_pattern]
        assert callable(procedure)
        return OscCallback(
            pattern=tuple(pattern),
            failure_pattern=failure_pattern,
            procedure=procedure,
            once=bool(once),
        )

    def _validate_receive(self, datagram):
        udp_in_logger.debug(datagram)
        try:
            message = OscMessage.from_datagram(datagram)
        except Exception:
            raise
        osc_in_logger.debug(repr(message))
        for callback in self._match_callbacks(message):
            callback.procedure(message)
        for capture in self.captures:
            capture.messages.append(
                CaptureEntry(timestamp=time.time(), label="R", message=message,)
            )

    def _validate_send(self, message):
        if not self.is_running:
            raise OscProtocolOffline
        if not isinstance(message, (str, collections.Iterable, OscBundle, OscMessage)):
            raise ValueError(message)
        if isinstance(message, str):
            message = OscMessage(message)
        elif isinstance(message, collections.Iterable):
            message = OscMessage(*message)
        osc_out_logger.debug(repr(message))
        for capture in self.captures:
            capture.messages.append(
                CaptureEntry(timestamp=time.time(), label="S", message=message)
            )
        datagram = message.to_datagram()
        udp_out_logger.debug(datagram)
        return datagram

    ### PUBLIC METHODS ###

    def capture(self):
        return Capture(self)

    def connect(self, ip_address: str, port: int, *, healthcheck: HealthCheck = None):
        ...

    def disconnect(self):
        ...

    def register(
        self, pattern, procedure, *, failure_pattern=None, once=False
    ) -> OscCallback:
        ...

    def send(self, message):
        ...

    def unregister(self, callback: OscCallback):
        ...


class AsyncOscProtocol(asyncio.DatagramProtocol, OscProtocol):

    ### INITIALIZER ###

    def __init__(self):
        asyncio.DatagramProtocol.__init__(self)
        OscProtocol.__init__(self)
        self.loop = None

    ### PRIVATE METHODS ###

    async def _run_healthcheck(self):
        while self.is_running:
            sleep_time = self.healthcheck.timeout * pow(
                self.healthcheck.backoff_factor, self.attempts
            )
            self.attempts += 1
            if self.attempts >= self.healthcheck.max_attempts:
                self.exit_future.set_result(True)
                self._teardown()
                self.transport.close()
                obj_ = self.healthcheck.callback()
                if asyncio.iscoroutine(obj_):
                    self.loop.create_task(obj_)
                return
            self.send(OscMessage(*self.healthcheck.request_pattern))
            await asyncio.sleep(sleep_time)

    ### PUBLIC METHODS ###

    async def connect(
        self, ip_address: str, port: int, *, healthcheck: HealthCheck = None
    ):
        if self.is_running:
            raise OscProtocolAlreadyConnected
        self._setup(ip_address, port, healthcheck)
        self.loop = asyncio.get_running_loop()
        self.exit_future = self.loop.create_future()
        _, protocol = await self.loop.create_datagram_endpoint(
            lambda: self, remote_addr=(ip_address, port),
        )

    def connection_made(self, transport):
        loop = asyncio.get_running_loop()
        self.transport = transport
        self.is_running = True
        if self.healthcheck:
            self.healthcheck_task = loop.create_task(self._run_healthcheck())

    def connection_lost(self, exc):
        pass

    def datagram_received(self, data, addr):
        self._validate_receive(data)

    async def disconnect(self):
        if not self.is_running:
            return
        self.exit_future.set_result(True)
        self._teardown()
        if self.loop.is_closed():
            return
        if not self.transport.is_closing():
            self.transport.close()
        if self.healthcheck is not None:
            await self.healthcheck_task

    def error_received(self, exc):
        osc_out_logger.warning(exc)

    def register(
        self, pattern, procedure, *, failure_pattern=None, once=False,
    ) -> OscCallback:
        callback = self._validate_callback(
            pattern, procedure, failure_pattern=failure_pattern, once=once
        )
        self._add_callback(callback)
        return callback

    def send(self, message):
        datagram = self._validate_send(message)
        return self.transport.sendto(datagram)

    def unregister(self, callback: OscCallback):
        self._remove_callback(callback)


class ThreadedOscServer(socketserver.UDPServer):
    osc_protocol: "ThreadedOscProtocol"

    def verify_request(self, request, client_address):
        self.osc_protocol._process_command_queue()
        return True

    def service_actions(self):
        self.osc_protocol._run_healthcheck()


class ThreadedOscHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        self.server.osc_protocol._validate_receive(data)


class ThreadedOscProtocol(OscProtocol):

    ### INITIALIZER ###

    def __init__(self):
        OscProtocol.__init__(self)
        self.command_queue = queue.Queue()
        self.lock = threading.RLock()
        self.server = None
        self.server_thread = None

    ### SPECIAL METHODS ###

    def __del__(self):
        self.disconnect()

    ### PRIVATE METHODS ###

    def _process_command_queue(self):
        while self.command_queue.qsize():
            try:
                action, callback = self.command_queue.get()
            except queue.Empty:
                continue
            if action == "add":
                self._add_callback(callback)
            elif action == "remove":
                self._remove_callback(callback)

    def _run_healthcheck(self):
        if self.healthcheck is None or time.time() < self.healthcheck_deadline:
            return
        self.healthcheck_deadline += self.healthcheck.timeout * pow(
            self.healthcheck.backoff_factor, self.attempts
        )
        self.attempts += 1
        if self.attempts < self.healthcheck.max_attempts:
            self.send(OscMessage(*self.healthcheck.request_pattern))
            return
        self._BaseServer__shutdown_request = True
        with self.lock:
            self._teardown()
            self.server = None
            self.server_thread = None
            self.healthcheck.callback()

    def _server_factory(self, ip_address, port):
        server = ThreadedOscServer(
            (self.ip_address, self.port), ThreadedOscHandler, bind_and_activate=False
        )
        server.osc_protocol = self
        return server

    ### PUBLIC METHODS ###

    def connect(self, ip_address: str, port: int, *, healthcheck: HealthCheck = None):
        if self.is_running:
            raise OscProtocolAlreadyConnected
        self._setup(ip_address, port, healthcheck)
        self.healthcheck_deadline = time.time()
        self.server = self._server_factory(ip_address, port)
        self.server_thread = threading.Thread(target=self.server.serve_forever)
        self.server_thread.daemon = True
        self.server_thread.start()
        self.is_running = True

    def disconnect(self):
        with self.lock:
            if not self.is_running:
                return
            self._teardown()
            self.server.shutdown()
            self.server = None
            self.server_thread = None

    def register(
        self, pattern, procedure, *, failure_pattern=None, once=False,
    ) -> OscCallback:
        """
        Register a callback.
        """
        callback = self._validate_callback(
            pattern, procedure, failure_pattern=failure_pattern, once=once
        )
        # Command queue prevents lock contention.
        self.command_queue.put(("add", callback))
        return callback

    def send(self, message):
        datagram = self._validate_send(message)
        try:
            self.server.socket.sendto(datagram, (self.ip_address, self.port))
        except OSError:
            # print(message)
            raise

    def unregister(self, callback: OscCallback):
        """
        Unregister a callback.
        """
        # Command queue prevents lock contention.
        self.command_queue.put(("remove", callback))
