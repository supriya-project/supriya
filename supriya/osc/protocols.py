import asyncio
import atexit
import collections
import queue
import socketserver
import threading
import time
from typing import Any, Dict, Set

from .callbacks import OscCallback
from .captures import Capture, CaptureEntry
from .messages import OscBundle, OscMessage


class OscProtocol:

    ### INITIALIZER ###

    def __init__(self):
        self.callbacks: Dict[Any, Any] = {}
        self.captures: Set[Capture] = set()
        self.ip_address = None
        self.port = None
        self.is_running: bool = False
        self.timeout = 1.0
        atexit.register(self.disconnect)

    ### PRIVATE METHODS ###

    def _add_callback(self, callback):
        patterns = [callback.pattern]
        if callback.failure_pattern:
            patterns.append(callback.failure_pattern)
        for pattern in patterns:
            callback_map = self.callbacks
            for item in pattern:
                callbacks, callback_map = callback_map.setdefault(
                    item, ([], {})
                )
            callbacks.append(callback)

    def _remove_callback(self, callback):
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

    def _match(self, message):
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

    def _validate_callback(
        self, pattern, procedure, *, failure_pattern=None, once=False,
    ):
        if isinstance(pattern, (str, int, float)):
            pattern = (pattern,)
        assert callable(procedure)
        return OscCallback(
            pattern=tuple(pattern),
            failure_pattern=failure_pattern,
            procedure=procedure,
            once=bool(once),
        )

    def _validate_receive(self, data):
        try:
            message = OscMessage.from_datagram(data)
        except Exception:
            raise
        for callback in self._match(message):
            callback.procedure(message)
        for capture in self.server.io_instance.captures:
            capture.messages.append(
                CaptureEntry(timestamp=time.time(), label="R", message=message,)
            )

    def _validate_send(self, message):
        if not self.is_running:
            raise RuntimeError
        if not isinstance(message, (str, collections.Iterable, OscBundle, OscMessage)):
            raise ValueError(message)
        if isinstance(message, str):
            message = OscMessage(message)
        elif isinstance(message, collections.Iterable):
            message = OscMessage(*message)
        for capture in self.captures:
            capture.messages.append(
                CaptureEntry(timestamp=time.time(), label="S", message=message)
            )
        return message.to_datagram()

    ### PUBLIC METHODS ###

    def capture(self):
        return Capture(self)

    def connect(self, ip_address: str, port: int, *, timeout: float = 2.0):
        ...

    def disconnect(self):
        ...

    def register(self, pattern, procedure, *, failure_pattern=None, once=False):
        ...

    def send(self, message):
        ...

    def unregister(self, callback):
        ...


class AsyncOscProtocol(asyncio.DatagramProtocol, OscProtocol):

    ### INITIALIZER ###

    def __init__(self):
        asyncio.DatagramProtocol.__init__(self)
        OscProtocol.__init__(self)

    ### PUBLIC METHODS ###

    async def connect(self, ip_address: str, port: int, *, timeout: float = 2.0):
        if self.is_running:
            raise RuntimeError
        self.ip_address = ip_address
        self.port = port
        self.timeout = timeout
        loop = asyncio.get_running_loop()
        _, protocol = await loop.create_datagram_endpoint(
            lambda: self, remote_addr=(ip_address, port),
        )
        return protocol

    def connection_made(self, transport):
        self.transport = transport
        self.is_running = True

    def connection_lost(self, exc):
        self.disconnect()

    def datagram_received(self, data, addr):
        self._validate_receive(data)

    async def disconnect(self):
        self.is_running = False
        self.transport.close()

    def register(
        self,
        pattern,
        procedure,
        *,
        failure_pattern=None,
        once=False,
    ):
        callback = self._validate_callback(
            pattern, procedure, failure_pattern=failure_pattern, once=once
        )
        self._add_callback(callback)

    def send(self, message):
        datagram = self._validate_send(message)
        return self.transport.sendto(datagram)

    def unregister(self, callback):
        self._remove_callback(callback)


class ThreadedOscProtocol(OscProtocol):

    ### CLASS VARIABLES ###

    class OscServer(socketserver.UDPServer):
        io_instance: "ThreadedOscProtocol"

        def verify_request(self, request, client_address):
            while self.io_instance.command_queue.qsize():
                try:
                    action, callback = self.io_instance.command_queue.get()
                except queue.Empty:
                    continue
                if action == "add":
                    self.io_instance._add_callback(callback)
                elif action == "remove":
                    self.io_instance._remove_callback(callback)
            return True

    class OscHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data = self.request[0]
            self.server.io_instance._validate_receive(data)

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

    ### PUBLIC METHODS ###

    def connect(self, ip_address: str, port: int, *, timeout: float = 2.0):
        with self.lock:
            if self.is_running:
                raise RuntimeError
            self.ip_address = ip_address
            self.port = port
            self.timeout = timeout
            self.server = self.OscServer(
                (self.ip_address, self.port), self.OscHandler, bind_and_activate=False
            )
            self.server.io_instance = self
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            self.is_running = True

    def disconnect(self):
        with self.lock:
            if not self.is_running:
                return
            self.server.shutdown()
            self.server = None
            self.server_thread = None
            self.is_running = False

    def register(
        self, pattern, procedure, *, failure_pattern=None, once=False,
    ):
        """
        Register a callback.
        """
        callback = self._validate_callback(
            pattern, procedure, failure_pattern=failure_pattern, once=once
        )
        self.command_queue.put(("add", callback))
        return callback

    def send(self, message):
        datagram = self._validate_send(message)
        try:
            self.server.socket.sendto(datagram, (self.ip_address, self.port))
        except OSError:
            print(message)
            raise

    def unregister(self, callback):
        """
        Unregister a callback.
        """
        self.command_queue.put(("remove", callback))
