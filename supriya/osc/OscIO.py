import collections
import socketserver
import threading
import time
import typing

from supriya.commands.Requestable import Requestable
from supriya.commands.Response import Response
from supriya.osc.OscBundle import OscBundle
from supriya.osc.OscMessage import OscMessage


class OscIO:
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

    class OscServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
        pass

    class OscHandler(socketserver.BaseRequestHandler):
        def handle(self):
            data = self.request[0]
            message = OscMessage.from_datagram(data)
            debug_osc = self.server.io_instance.debug_osc
            debug_udp = self.server.io_instance.debug_udp
            # TODO: Is it worth the additional thread creation?
            response = None
            for callback in self.server.io_instance.match(message):
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
                if debug_osc:
                    print("RECV", "{:0.6f}".format(time.time()), message.to_list())
                    if debug_udp:
                        for line in str(message).splitlines():
                            print("    " + line)

    class OscCallback(typing.NamedTuple):
        pattern: typing.Tuple[typing.Union[str, int, float], ...]
        procedure: typing.Callable
        once: bool
        parse_response: bool

    def __init__(
        self,
        debug_osc=False,
        debug_udp=False,
        ip_address="127.0.0.1",
        port=57751,
        timeout=2,
    ):
        import supriya.commands

        self.callbacks = {}
        self.captures = set()
        self.debug_osc = bool(debug_osc)
        self.debug_udp = bool(debug_udp)
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

    def match(self, message):
        """
        Match callbacks against pattern.

        ::

            >>> io = supriya.osc.OscIO()
            >>> callback = io.register(
            ...     pattern=['/synced', 1],
            ...     procedure=lambda: print('ok'),
            ...     )
            >>> other_callback = io.register(
            ...     pattern=['/synced'],
            ...     procedure=lambda: print('sure'),
            ...     )

        ::

            >>> for callback in io.match(supriya.osc.OscMessage('/synced', 1)):
            ...     callback
            ...
            OscCallback(pattern=('/synced',), procedure=<function <lambda> at 0x...>, once=False, parse_response=False)
            OscCallback(pattern=('/synced', 1), procedure=<function <lambda> at 0x...>, once=False, parse_response=False)

        ::

            >>> for callback in io.match(supriya.osc.OscMessage('/synced', 2)):
            ...     callback
            ...
            OscCallback(pattern=('/synced',), procedure=<function <lambda> at 0x...>, once=False, parse_response=False)

        ::

            >>> for callback in io.match(supriya.osc.OscMessage('/n_go', 1000, 1001)):
            ...     callback
            ...

        """
        items = (message.address,) + message.contents
        matching_callbacks = []
        with self.lock:
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

    def quit(self):
        with self.lock:
            if not self.is_running:
                return
            self.server.shutdown()
            self.server = None
            self.server_thread = None
            self.is_running = False

    def register(self, pattern, procedure, once=False, parse_response=False):
        """
        Register a callback.

        ::

            >>> io = supriya.osc.OscIO()
            >>> callback = io.register(
            ...     pattern=['/synced', 1],
            ...     procedure=lambda: print('ok'),
            ...     )

        ::

            >>> import pprint
            >>> pprint.pprint(io.callbacks)
            {'/synced': ([],
                         {1: ([OscCallback(pattern=('/synced', 1), procedure=<function <lambda> at 0x...>, once=False, parse_response=False)],
                              {})})}

        """
        if isinstance(pattern, (str, int, float)):
            pattern = (pattern,)
        assert callable(procedure)
        callback = self.OscCallback(
            pattern=tuple(pattern),
            procedure=procedure,
            once=bool(once),
            parse_response=bool(parse_response),
        )
        with self.lock:
            callback_map = self.callbacks
            for item in pattern:
                callbacks, callback_map = callback_map.setdefault(item, ([], {}))
            callbacks.append(callback)
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
        if not (isinstance(message, OscMessage) and message.address in (2, "/status")):
            for capture in self.captures:
                capture.messages.append(
                    OscIO.CaptureEntry(
                        timestamp=time.time(),
                        label="S",
                        message=message,
                        command=request,
                    )
                )
            if self.debug_osc:
                print("SEND", "{:0.6f}".format(time.time()), message.to_list())
                if self.debug_udp:
                    for line in str(message).splitlines():
                        print("    " + line)
        datagram = message.to_datagram()
        self.server.socket.sendto(datagram, (self.ip_address, self.port))

    def unregister(self, callback):
        """
        Unregister a callback.

        ::

            >>> io = supriya.osc.OscIO()
            >>> callback = io.register(
            ...     pattern=['/synced', 1],
            ...     procedure=lambda: print('ok'),
            ...     )
            >>> other_callback = io.register(
            ...     pattern=['/synced'],
            ...     procedure=lambda: print('sure'),
            ...     )

        ::

            >>> import pprint
            >>> pprint.pprint(io.callbacks)
            {'/synced': ([OscCallback(pattern=('/synced',), procedure=<function <lambda> at 0x...>, once=False, parse_response=False)],
                         {1: ([OscCallback(pattern=('/synced', 1), procedure=<function <lambda> at 0x...>, once=False, parse_response=False)],
                              {})})}

        ::

            >>> io.unregister(other_callback)
            >>> pprint.pprint(io.callbacks)
            {'/synced': ([],
                         {1: ([OscCallback(pattern=('/synced', 1), procedure=<function <lambda> at 0x...>, once=False, parse_response=False)],
                              {})})}

        ::

            >>> io.unregister(callback)
            >>> pprint.pprint(io.callbacks)
            {}

        """

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

        with self.lock:
            delete(list(callback.pattern), self.callbacks)
