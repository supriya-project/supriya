"""
Tools for sending, receiving and handling OSC messages.
"""

import collections
import datetime
import enum
import struct
import time
import logging
import queue
import socket
import socketserver
import threading
import typing
from collections import deque
from contextlib import closing

from supriya import utils
from supriya.commands.Requestable import Requestable
from supriya.commands.Response import Response
from supriya.system.SupriyaValueObject import SupriyaValueObject


osc_in_logger = logging.getLogger("supriya.osc.in")
osc_out_logger = logging.getLogger("supriya.osc.out")
udp_in_logger = logging.getLogger("supriya.udp.in")
udp_out_logger = logging.getLogger("supriya.udp.out")


BUNDLE_PREFIX = b"#bundle\x00"
IMMEDIATELY = struct.pack(">Q", 1)
NTP_TIMESTAMP_TO_SECONDS = 1.0 / 2.0 ** 32.0
SECONDS_TO_NTP_TIMESTAMP = 2.0 ** 32.0
SYSTEM_EPOCH = datetime.date(*time.gmtime(0)[0:3])
NTP_EPOCH = datetime.date(1900, 1, 1)
NTP_DELTA = (SYSTEM_EPOCH - NTP_EPOCH).days * 24 * 3600


def decode_array(type_tags, type_tag_offset, payload, payload_offset):
    assert type_tags[type_tag_offset] == "["
    array = []
    type_tag_offset += 1
    while type_tags[type_tag_offset] != "]":
        result, type_tag_offset, payload_offset = decode_value(
            type_tags, type_tag_offset, payload, payload_offset
        )
        array.append(result)
    assert type_tags[type_tag_offset] == "]"
    array = tuple(array)
    type_tag_offset += 1
    return array, type_tag_offset, payload_offset


def decode_blob(cls, type_tags, type_tag_offset, payload, payload_offset):
    assert type_tags[type_tag_offset] == "b"
    length = payload[payload_offset : payload_offset + 4]
    length = struct.unpack(">i", length)
    length = length[0]
    payload_offset += 4
    total_length = length + (-length % 4)
    result = payload[payload_offset : payload_offset + length]
    type_tag_offset += 1
    payload_offset += total_length
    for class_ in (cls, OscBundle):
        try:
            result = class_.from_datagram(result)
            break
        except IndexError:
            pass
    return result, type_tag_offset, payload_offset


def decode_boolean(type_tags, type_tag_offset, payload, payload_offset):
    type_tag = type_tags[type_tag_offset]
    if type_tag == "T":
        result = True
    elif type_tag == "F":
        result = False
    type_tag_offset += 1
    return result, type_tag_offset, payload_offset


def decode_double(type_tags, type_tag_offset, payload, payload_offset):
    result, payload_offset = read_double(payload, payload_offset)
    type_tag_offset += 1
    return result, type_tag_offset, payload_offset


def decode_float(type_tags, type_tag_offset, payload, payload_offset):
    result, payload_offset = read_float(payload, payload_offset)
    type_tag_offset += 1
    return result, type_tag_offset, payload_offset


def decode_int(type_tags, type_tag_offset, payload, payload_offset):
    result, payload_offset = read_int(payload, payload_offset)
    type_tag_offset += 1
    return result, type_tag_offset, payload_offset


def decode_none(type_tags, type_tag_offset, payload, payload_offset):
    result = None
    type_tag_offset += 1
    return result, type_tag_offset, payload_offset


def decode_string(type_tags, type_tag_offset, payload, payload_offset):
    result, payload_offset = read_string(payload, payload_offset)
    type_tag_offset += 1
    return result, type_tag_offset, payload_offset


def encode_array(array):
    type_tags = "["
    encoded_value = b""
    for value in array:
        sub_type_tags, sub_encoded_value = encode_value(value)
        type_tags += sub_type_tags
        encoded_value += sub_encoded_value
    type_tags += "]"
    return type_tags, encoded_value


def encode_blob(value):
    type_tags = "b"
    encoded_value = struct.pack(">i", len(value))
    encoded_value += value
    if len(encoded_value) % 4:
        difference = 4 - (len(encoded_value) % 4)
        padding = b"\x00" * difference
        encoded_value += padding
    return type_tags, encoded_value


def encode_boolean(value):
    if value:
        type_tags = "T"
    else:
        type_tags = "F"
    encoded_value = None
    return type_tags, encoded_value


def encode_float(value):
    type_tags = "f"
    encoded_value = struct.pack(">f", value)
    return type_tags, encoded_value


def encode_int(value):
    type_tags = "i"
    encoded_value = struct.pack(">i", value)
    return type_tags, encoded_value


def encode_none():
    type_tags = "N"
    encoded_value = None
    return type_tags, encoded_value


def encode_string(value):
    type_tags = "s"
    encoded_value = value.encode("utf-8")
    padding_length = 4 - (len(encoded_value) % 4)
    padding = b"\x00" * padding_length
    encoded_value += padding
    return type_tags, encoded_value


def encode_value(value):
    if hasattr(value, "to_datagram"):
        value = bytearray(value.to_datagram())
    elif isinstance(value, enum.Enum):
        value = value.value
    if isinstance(value, (bytearray, bytes)):
        type_tags, encoded_value = encode_blob(value)
    elif isinstance(value, str):
        type_tags, encoded_value = encode_string(value)
    elif isinstance(value, bool):
        type_tags, encoded_value = encode_boolean(value)
    elif isinstance(value, float):
        type_tags, encoded_value = encode_float(value)
    elif isinstance(value, int):
        type_tags, encoded_value = encode_int(value)
    elif value is None:
        type_tags, encoded_value = encode_none()
    elif isinstance(value, collections.Sequence):
        type_tags, encoded_value = encode_array(value)
    else:
        message = "Cannot encode {!r}".format(value)
        raise TypeError(message)
    return type_tags, encoded_value


def decode_value(type_tags, type_tag_offset, payload, payload_offset):
    type_tag = type_tags[type_tag_offset]
    type_tag_mapping = {
        "N": decode_none,
        "T": decode_boolean,
        "F": decode_boolean,
        "d": decode_double,
        "i": decode_int,
        "f": decode_float,
        "s": decode_string,
        "b": decode_blob,
        "[": decode_array,
    }
    procedure = type_tag_mapping[type_tag]
    result, type_tag_offset, payload_offset = procedure(
        type_tags, type_tag_offset, payload, payload_offset
    )
    return result, type_tag_offset, payload_offset


def read_double(payload, payload_offset):
    result = payload[payload_offset : payload_offset + 8]
    result = struct.unpack(">d", result)
    result = result[0]
    payload_offset += 8
    return result, payload_offset


def read_float(payload, payload_offset):
    result = payload[payload_offset : payload_offset + 4]
    result = struct.unpack(">f", result)
    result = result[0]
    payload_offset += 4
    return result, payload_offset


def read_int(payload, payload_offset):
    result = payload[payload_offset : payload_offset + 4]
    result = struct.unpack(">i", result)
    result = result[0]
    payload_offset += 4
    return result, payload_offset


def read_string(payload, payload_offset):
    offset = 0
    while payload[payload_offset + offset] != 0:
        offset += 1
    if (offset % 4) == 0:
        offset += 4
    else:
        offset += -offset % 4
    result = payload[payload_offset : payload_offset + offset]
    result = result.replace(b"\x00", b"")
    result = result.decode("utf-8")
    payload_offset += offset
    return result, payload_offset


def read_date(payload, offset):
    if payload[offset : offset + 8] == IMMEDIATELY:
        date = None
    else:
        date = (
            struct.unpack(">Q", payload[offset : offset + 8])[0]
            / SECONDS_TO_NTP_TIMESTAMP
        ) - NTP_DELTA
    offset += 8
    return date, offset


def write_date(seconds, realtime=True):
    if seconds is None:
        return IMMEDIATELY
    if realtime:
        seconds = seconds + NTP_DELTA
        return struct.pack(">Q", int(seconds * SECONDS_TO_NTP_TIMESTAMP))
    return struct.pack(">Q", int(seconds * SECONDS_TO_NTP_TIMESTAMP))


class OscMessage(SupriyaValueObject):
    """
    An OSC message.

    ::

        >>> import supriya.osc
        >>> osc_message = supriya.osc.OscMessage('/g_new', 0, 0)
        >>> osc_message
        OscMessage('/g_new', 0, 0)

    ::

        >>> datagram = osc_message.to_datagram()
        >>> supriya.osc.OscMessage.from_datagram(datagram)
        OscMessage('/g_new', 0, 0)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_address", "_contents")

    ### INITIALIZER ###

    def __init__(self, address, *contents):
        def recurse(sequence):
            sequence = list(sequence)
            for i, x in enumerate(sequence):
                if isinstance(x, list):
                    sequence[i] = tuple(recurse(sequence[i]))
            return tuple(sequence)

        if isinstance(address, enum.Enum):
            address = address.value
        assert isinstance(address, (str, int))
        self._address = address
        self._contents = recurse(contents)

    ### SPECIAL METHODS ###

    def __repr__(self):
        items = (self.address,) + self.contents
        items = ", ".join(repr(x) for x in items)
        result = "{}({})".format(type(self).__name__, items)
        return result

    def __str__(self):
        datagram = bytearray(self.to_datagram())
        return format_datagram(datagram)

    ### PUBLIC METHODS ###

    def to_datagram(self):
        # address can be a string or (in SuperCollider) an int
        datagram = encode_value(self.address)[1]
        if self.contents is None:
            return datagram
        encoded_type_tags = ","
        encoded_contents = b""
        for argument in self.contents:
            type_tags, encoded_value = encode_value(argument)
            encoded_type_tags += type_tags
            if encoded_value is not None:
                encoded_contents += encoded_value
        encoded_type_tags = encode_string(encoded_type_tags)[1]
        datagram += encoded_type_tags
        datagram += encoded_contents
        datagram = bytes(datagram)
        return datagram

    @staticmethod
    def from_datagram(datagram):
        datagram = bytearray(datagram)
        contents = []
        offset = 0
        address, offset = read_string(datagram, offset)
        type_tags, offset = read_string(datagram, offset)
        assert type_tags[0] == ","
        payload = datagram[offset:]
        payload_offset = 0
        type_tag_offset = 1
        while type_tag_offset < len(type_tags):
            result, type_tag_offset, payload_offset = decode_value(
                type_tags, type_tag_offset, payload, payload_offset
            )
            contents.append(result)
        osc_message = OscMessage(address, *contents)
        return osc_message

    def to_list(self):
        result = [self.address]
        for x in self.contents:
            if hasattr(x, "to_list"):
                result.append(x.to_list())
            else:
                result.append(x)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def address(self):
        return self._address

    @property
    def contents(self):
        return self._contents


class OscBundle(SupriyaValueObject):
    """
    An OSC bundle.

    ::

        >>> import supriya.osc
        >>> message_one = supriya.osc.OscMessage('/one', 1)
        >>> message_two = supriya.osc.OscMessage('/two', 2)
        >>> message_three = supriya.osc.OscMessage('/three', 3)

    ::

        >>> inner_bundle = supriya.osc.OscBundle(
        ...     timestamp=1401557034.5,
        ...     contents=(message_one, message_two),
        ...     )
        >>> inner_bundle
        OscBundle(
            contents=(
                OscMessage('/one', 1),
                OscMessage('/two', 2),
                ),
            timestamp=1401557034.5,
            )

    ::

        >>> outer_bundle = supriya.osc.OscBundle(
        ...     contents=(inner_bundle, message_three),
        ...     )
        >>> outer_bundle
        OscBundle(
            contents=(
                OscBundle(
                    contents=(
                        OscMessage('/one', 1),
                        OscMessage('/two', 2),
                        ),
                    timestamp=1401557034.5,
                    ),
                OscMessage('/three', 3),
                ),
            )

    ::

        >>> datagram = outer_bundle.to_datagram()

    ::

        >>> decoded_bundle = supriya.osc.OscBundle.from_datagram(datagram)
        >>> decoded_bundle
        OscBundle(
            contents=(
                OscBundle(
                    contents=(
                        OscMessage('/one', 1),
                        OscMessage('/two', 2),
                        ),
                    timestamp=1401557034.5,
                    ),
                OscMessage('/three', 3),
                ),
            )

    ::

        >>> decoded_bundle == outer_bundle
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_contents", "_timestamp")

    ### INITIALIZER ###

    def __init__(self, timestamp=None, contents=None):
        prototype = (OscMessage, type(self))
        self._timestamp = timestamp
        contents = contents or ()
        for x in contents:
            if not isinstance(x, prototype):
                raise ValueError(contents)
        contents = tuple(contents)
        self._contents = contents

    ### SPECIAL METHODS ###

    def __str__(self):
        datagram = bytearray(self.to_datagram())
        return format_datagram(datagram)

    ### PUBLIC METHODS ###

    @staticmethod
    def datagram_is_bundle(datagram, offset=0):
        return datagram[offset : offset + 8] == BUNDLE_PREFIX

    @staticmethod
    def from_datagram(datagram):
        assert OscBundle.datagram_is_bundle(datagram)
        offset = 8
        timestamp, offset = read_date(datagram, offset)
        contents = []
        while offset < len(datagram):
            length, offset = read_int(datagram, offset)
            data = datagram[offset : offset + length]
            if OscBundle.datagram_is_bundle(data):
                item = OscBundle.from_datagram(data)
            else:
                item = OscMessage.from_datagram(data)
            contents.append(item)
            offset += length
        osc_bundle = OscBundle(timestamp=timestamp, contents=tuple(contents))
        return osc_bundle

    @classmethod
    def partition(cls, messages, timestamp=None):
        bundles = []
        contents = []
        message = deque(messages)
        remaining = maximum = 8192 - len(BUNDLE_PREFIX) - 4
        while messages:
            message = messages.popleft()
            datagram = message.to_datagram()
            remaining -= len(datagram) + 4
            if remaining > 0:
                contents.append(message)
            else:
                bundles.append(cls(timestamp=timestamp, contents=contents))
                contents = [message]
                remaining = maximum
        if contents:
            bundles.append(cls(timestamp=timestamp, contents=contents))
        return bundles

    def to_datagram(self, realtime=True):
        datagram = BUNDLE_PREFIX
        datagram += write_date(self._timestamp, realtime=realtime)
        for content in self.contents:
            content_datagram = content.to_datagram()
            datagram += struct.pack(">i", len(content_datagram))
            datagram += content_datagram
        return datagram

    def to_list(self):
        result = [self.timestamp]
        result.append([x.to_list() for x in self.contents])
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        return self._contents

    @property
    def timestamp(self):
        return self._timestamp


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


def format_datagram(datagram):
    result = []
    result.append("size {}".format(len(datagram)))
    index = 0
    while index < len(datagram):
        chunk = datagram[index : index + 16]
        line = "{: >4}   ".format(index)
        hex_blocks = []
        ascii_block = ""
        for chunk in utils.group_iterable_by_count(chunk, 4):
            hex_block = []
            for byte in chunk:
                char = int(byte)
                if 31 < char < 127:
                    char = chr(char)
                else:
                    char = "."
                ascii_block += char
                hexed = hex(byte)[2:].zfill(2)
                hex_block.append(hexed)
            hex_block = " ".join(hex_block)
            hex_blocks.append(hex_block)
        hex_blocks = "  ".join(hex_blocks)
        ascii_block = "|{}|".format(ascii_block)
        hex_blocks = "{: <53}".format(hex_blocks)
        line += hex_blocks
        line += ascii_block
        result.append(line)
        index += 16
    result = "\n".join(result)
    return result
