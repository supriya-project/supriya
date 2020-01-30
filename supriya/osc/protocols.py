import asyncio
import atexit
import collections
import logging
import queue
import socketserver
import threading
import time
from typing import Any, Dict, Set

from supriya.commands.Requestable import Requestable

from .callbacks import OscCallback
from .captures import Capture, CaptureEntry
from .messages import OscBundle, OscMessage

osc_in_logger = logging.getLogger("supriya.osc.in")
osc_out_logger = logging.getLogger("supriya.osc.out")
udp_in_logger = logging.getLogger("supriya.udp.in")
udp_out_logger = logging.getLogger("supriya.udp.out")


class OscProtocol:
    def __init__(self):
        self.callbacks: Dict[Any, Any] = {}
        self.captures: Set[Capture] = set()
        self.ip_address = None
        self.port = None
        self.is_running: bool = False
        self.timeout = 1.0
        atexit.register(self.disconnect)

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
    def __init__(self):
        asyncio.DatagramProtocol.__init__(self)
        OscProtocol.__init__(self)

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
        print("RECV:", data.from_datagram(data))

    async def disconnect(self):
        self.is_running = False
        self.transport.close()

    def register(
        self,
        path_pattern,
        procedure,
        *,
        args_pattern=None,
        failure_pattern=None,
        once=False,
    ):
        pass

    def send(self, message):
        print("SEND:", message)
        return self.transport.sendto(message.to_datagram())

    def unregister(self, callback):
        pass


class ThreadedOscProtocol(OscProtocol):

    ### CLASS VARIABLES ###

    class OscServer(socketserver.UDPServer):
        io_instance: "ThreadedOscProtocol"

        def process_queue(self):
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

            while self.io_instance.command_queue.qsize():
                try:
                    action, callback = self.io_instance.command_queue.get()
                except queue.Empty:
                    continue
                patterns = [callback.pattern]
                if callback.failure_pattern:
                    patterns.append(callback.failure_pattern)
                if action == "add":
                    for pattern in patterns:
                        callback_map = self.io_instance.callbacks
                        for item in pattern:
                            callbacks, callback_map = callback_map.setdefault(
                                item, ([], {})
                            )
                        callbacks.append(callback)
                elif action == "remove":
                    for pattern in patterns:
                        delete(list(pattern), self.io_instance.callbacks)

        def verify_request(self, request, client_address):
            self.process_queue()
            return True

    class OscHandler(socketserver.BaseRequestHandler):
        def handle(self):
            now = time.time()
            data = self.request[0]
            try:
                message = OscMessage.from_datagram(data)
            except Exception:
                udp_in_logger.warn("Recv: {:0.6f} {}".format(now, data))
                raise
            osc_log_function = osc_in_logger.debug
            udp_log_function = udp_in_logger.debug
            if message.address != "/status.reply":
                osc_log_function = osc_in_logger.info
                udp_log_function = udp_in_logger.info
            osc_log_function("Recv: {:0.6f} {}".format(now, message.to_list()))
            for line in str(message).splitlines():
                udp_log_function("Recv: {:0.6f} {}".format(now, line))
            # TODO: Extract "response" parsing
            for callback in self.server.io_instance._match(message):
                callback.procedure(message)
            if message.address != "/status.reply":
                for capture in self.server.io_instance.captures:
                    capture.messages.append(
                        CaptureEntry(timestamp=time.time(), label="R", message=message,)
                    )

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
        if isinstance(pattern, (str, int, float)):
            pattern = (pattern,)
        assert callable(procedure)
        callback = OscCallback(
            pattern=tuple(pattern),
            failure_pattern=failure_pattern,
            procedure=procedure,
            once=bool(once),
        )
        self.command_queue.put(("add", callback))
        return callback

    def send(self, message, with_request_name=False):
        if not self.is_running:
            raise RuntimeError
        if isinstance(message, Requestable):
            message = message.to_osc(with_request_name=with_request_name)
        prototype = (str, collections.Iterable, OscBundle, OscMessage)
        if not isinstance(message, prototype):
            raise ValueError(message)
        if isinstance(message, str):
            message = OscMessage(message)
        elif isinstance(message, collections.Iterable):
            message = OscMessage(*message)
        now = time.time()
        osc_log_function = osc_out_logger.debug
        udp_log_function = udp_out_logger.debug
        if not (isinstance(message, OscMessage) and message.address in (2, "/status")):
            osc_log_function = osc_out_logger.info
            udp_log_function = udp_out_logger.info
            for capture in self.captures:
                capture.messages.append(
                    CaptureEntry(timestamp=time.time(), label="S", message=message,)
                )
        osc_log_function("Send: {:0.6f} {}".format(now, message.to_list()))
        for line in str(message).splitlines():
            udp_log_function("Send: {:0.6f} {}".format(now, line))
        datagram = message.to_datagram()
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
