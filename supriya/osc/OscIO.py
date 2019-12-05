import collections
import logging
import queue
import socket
import socketserver
import threading
import time
import typing
from contextlib import closing

from supriya.commands.Requestable import Requestable
from supriya.commands.Response import Response
from supriya.osc.OscBundle import OscBundle
from supriya.osc.OscMessage import OscMessage

osc_in_logger = logging.getLogger("supriya.osc.in")
osc_out_logger = logging.getLogger("supriya.osc.out")
udp_in_logger = logging.getLogger("supriya.udp.in")
udp_out_logger = logging.getLogger("supriya.udp.out")


class OscIO:

    ### CLASS VARIABLES ###

    class CaptureEntry(typing.NamedTuple):
        timestamp: float
        label: str
        message: typing.Union[OscMessage, OscBundle]
        command: typing.Optional[typing.Union[Requestable, Response]]

    class Capture:
        def __init__(self, osc_io):
            self.osc_io = osc_io
            self.messages = []

        def __enter__(self):
            self.osc_io.captures.add(self)
            self.messages[:] = []
            return self

        def __exit__(self, exc_type, exc_value, traceback):
            self.osc_io.captures.remove(self)

        def __iter__(self):
            return iter(self.messages)

        def __len__(self):
            return len(self.messages)

        @property
        def received_messages(self):
            return [
                (timestamp, osc_message)
                for timestamp, label, osc_message, _ in self.messages
                if label == "R"
            ]

        @property
        def requests(self):
            return [
                (timestamp, command)
                for timestamp, label, _, command in self.messages
                if label == "S" and command is not None
            ]

        @property
        def responses(self):
            return [
                (timestamp, command)
                for timestamp, label, _, command in self.messages
                if label == "R" and command is not None
            ]

        @property
        def sent_messages(self):
            return [
                (timestamp, osc_message)
                for timestamp, label, osc_message, _ in self.messages
                if label == "S"
            ]

    # class OscServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    class OscServer(socketserver.UDPServer):
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
            # TODO: Is it worth the additional thread creation?
            response = None
            for callback in self.server.io_instance._match(message):
                if callback.parse_response:
                    if response is None:
                        handler = self.server.io_instance.response_handlers.get(
                            message.address
                        )
                        if handler:
                            response = handler.from_osc_message(message)
                    args = response
                else:
                    args = message
                callback.procedure(args)
            if message.address != "/status.reply":
                for capture in self.server.io_instance.captures:
                    capture.messages.append(
                        OscIO.CaptureEntry(
                            timestamp=time.time(),
                            label="R",
                            message=message,
                            command=response,
                        )
                    )

    class OscCallback(typing.NamedTuple):
        pattern: typing.Tuple[typing.Union[str, int, float], ...]
        procedure: typing.Callable
        failure_pattern: typing.Optional[
            typing.Tuple[typing.Union[str, int, float], ...]
        ] = None
        once: bool = False
        parse_response: bool = False

    ### INITIALIZER ###

    def __init__(self, ip_address="127.0.0.1", port=57751, timeout=2):
        import supriya.commands

        self.callbacks = {}
        self.captures = set()
        self.command_queue = queue.Queue()
        self.ip_address = ip_address
        self.lock = threading.RLock()
        self.server = None
        self.server_thread = None
        self.port = port
        self.is_running = False
        self.timeout = timeout
        self.response_handlers = {
            "/b_info": supriya.commands.BufferInfoResponse,
            "/b_set": supriya.commands.BufferSetResponse,
            "/b_setn": supriya.commands.BufferSetContiguousResponse,
            "/c_set": supriya.commands.ControlBusSetResponse,
            "/c_setn": supriya.commands.ControlBusSetContiguousResponse,
            "/d_removed": supriya.commands.SynthDefRemovedResponse,
            "/done": supriya.commands.DoneResponse,
            "/fail": supriya.commands.FailResponse,
            "/g_queryTree.reply": supriya.commands.QueryTreeResponse,
            "/n_end": supriya.commands.NodeInfoResponse,
            "/n_go": supriya.commands.NodeInfoResponse,
            "/n_info": supriya.commands.NodeInfoResponse,
            "/n_move": supriya.commands.NodeInfoResponse,
            "/n_off": supriya.commands.NodeInfoResponse,
            "/n_on": supriya.commands.NodeInfoResponse,
            "/n_set": supriya.commands.NodeSetResponse,
            "/n_setn": supriya.commands.NodeSetContiguousResponse,
            "/status.reply": supriya.commands.StatusResponse,
            "/synced": supriya.commands.SyncedResponse,
            "/tr": supriya.commands.TriggerResponse,
        }

    ### SPECIAL METHODS ###

    def __del__(self):
        self.quit()

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

    def boot(self, ip_address=None, port=None):
        with self.lock:
            if self.is_running:
                return
            if ip_address:
                self.ip_address = ip_address
            if port:
                self.port = port
            self.server = self.OscServer(
                (self.ip_address, self.port), self.OscHandler, bind_and_activate=False
            )
            self.server.io_instance = self
            self.server_thread = threading.Thread(target=self.server.serve_forever)
            self.server_thread.daemon = True
            self.server_thread.start()
            self.is_running = True

    def capture(self):
        return self.Capture(self)

    @staticmethod
    def find_free_port():
        with closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
            s.bind(("", 0))
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            return s.getsockname()[1]

    def quit(self):
        with self.lock:
            if not self.is_running:
                return
            self.server.shutdown()
            self.server = None
            self.server_thread = None
            self.is_running = False

    def register(
        self, pattern, procedure, failure_pattern=None, once=False, parse_response=False
    ):
        """
        Register a callback.
        """
        if isinstance(pattern, (str, int, float)):
            pattern = (pattern,)
        assert callable(procedure)
        callback = self.OscCallback(
            pattern=tuple(pattern),
            failure_pattern=failure_pattern,
            procedure=procedure,
            once=bool(once),
            parse_response=bool(parse_response),
        )
        self.command_queue.put(("add", callback))
        return callback

    def send(self, message, with_request_name=False):
        if not self.is_running:
            raise RuntimeError
        request = None
        if isinstance(message, Requestable):
            request = message
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
                    OscIO.CaptureEntry(
                        timestamp=time.time(),
                        label="S",
                        message=message,
                        command=request,
                    )
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
