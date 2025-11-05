import asyncio
import collections
import concurrent.futures
import contextlib
import dataclasses
import datetime
import logging
import pprint
import socket
import socketserver
import struct
import threading
import time
from collections.abc import Sequence as SequenceABC
from enum import Enum
from queue import Empty, Queue
from typing import (
    Any,
    Awaitable,
    Callable,
    Generator,
    Iterator,
    Literal,
    NamedTuple,
    Sequence,
    TypeAlias,
    Union,
    cast,
)

from .enums import BootStatus
from .typing import FutureLike, SupportsOsc
from .ugens import decompile_synthdefs
from .utils import group_by_count

osc_protocol_logger = logging.getLogger(__name__)
osc_in_logger = logging.getLogger("supriya.osc.in")
osc_out_logger = logging.getLogger("supriya.osc.out")
udp_in_logger = logging.getLogger("supriya.udp.in")
udp_out_logger = logging.getLogger("supriya.udp.out")


BUNDLE_PREFIX = b"#bundle\x00"
IMMEDIATELY = struct.pack(">Q", 1)
NTP_TIMESTAMP_TO_SECONDS = 1.0 / 2.0**32.0
SECONDS_TO_NTP_TIMESTAMP = 2.0**32.0
SYSTEM_EPOCH = datetime.date(*time.gmtime(0)[0:3])
NTP_EPOCH = datetime.date(1900, 1, 1)
NTP_DELTA = (SYSTEM_EPOCH - NTP_EPOCH).days * 24 * 3600


OscAddress: TypeAlias = Enum | int | str
OscArgument: TypeAlias = Union[
    Enum,
    "OscBundle",
    "OscMessage",
    SequenceABC["OscArgument"],
    bool,
    bytes,
    float,
    str,
    None,
]


def format_datagram(datagram: bytes) -> str:
    result: list[str] = ["size {}".format(len(datagram))]
    index = 0
    while index < len(datagram):
        hex_blocks = []
        ascii_block = ""
        for chunk in group_by_count(datagram[index : index + 16], 4):
            hex_block = []
            for byte in chunk:
                if 31 < int(byte) < 127:
                    char = chr(int(byte))
                else:
                    char = "."
                ascii_block += char
                hexed = hex(byte)[2:].zfill(2)
                hex_block.append(hexed)
            hex_blocks.append(" ".join(hex_block))
        line = "{: >4}   ".format(index)
        line += "{: <53}".format("  ".join(hex_blocks))
        line += "|{}|".format(ascii_block)
        result.append(line)
        index += 16
    return "\n".join(result)


class OscMessage:
    """
    An OSC message.

    .. container:: example

        ::

            >>> from supriya.osc import OscMessage
            >>> osc_message = OscMessage("/g_new", 0, 0)
            >>> osc_message
            OscMessage('/g_new', 0, 0)

        ::

            >>> datagram = osc_message.to_datagram()
            >>> OscMessage.from_datagram(datagram)
            OscMessage('/g_new', 0, 0)

        ::

            >>> print(osc_message)
            size 20
               0   2f 67 5f 6e  65 77 00 00  2c 69 69 00  00 00 00 00   |/g_new..,ii.....|
              16   00 00 00 00                                          |....|

    .. container:: example

        ::

            >>> osc_message = OscMessage("/foo", True, [None, [3.25]], OscMessage("/bar"))
            >>> osc_message
            OscMessage('/foo', True, [None, [3.25]], OscMessage('/bar'))

        ::

            >>> datagram = osc_message.to_datagram()
            >>> OscMessage.from_datagram(datagram)
            OscMessage('/foo', True, [None, [3.25]], OscMessage('/bar'))

        ::

            >>> print(osc_message)
            size 40
               0   2f 66 6f 6f  00 00 00 00  2c 54 5b 4e  5b 66 5d 5d   |/foo....,T[N[f]]|
              16   62 00 00 00  40 50 00 00  00 00 00 0c  2f 62 61 72   |b...@P....../bar|
              32   00 00 00 00  2c 00 00 00                             |....,...|

    .. container:: example

        ::

            >>> osc_message = supriya.osc.OscMessage(
            ...     "/foo",
            ...     1,
            ...     2.5,
            ...     supriya.osc.OscBundle(
            ...         contents=(
            ...             supriya.osc.OscMessage("/bar", "baz", 3.0),
            ...             supriya.osc.OscMessage("/ffff", False, True, None),
            ...         )
            ...     ),
            ...     ["a", "b", ["c", "d"]],
            ... )
            >>> osc_message
            OscMessage('/foo', 1, 2.5, OscBundle(contents=[OscMessage('/bar', 'baz', 3.0), OscMessage('/ffff', False, True, None)]), ['a', 'b', ['c', 'd']])

        ::

            >>> datagram = osc_message.to_datagram()
            >>> OscMessage.from_datagram(datagram)
            OscMessage('/foo', 1, 2.5, OscBundle(contents=[OscMessage('/bar', 'baz', 3.0), OscMessage('/ffff', False, True, None)]), ['a', 'b', ['c', 'd']])

        ::

            >>> print(osc_message)
            size 112
               0   2f 66 6f 6f  00 00 00 00  2c 69 66 62  5b 73 73 5b   |/foo....,ifb[ss[|
              16   73 73 5d 5d  00 00 00 00  00 00 00 01  40 20 00 00   |ss]]........@ ..|
              32   00 00 00 3c  23 62 75 6e  64 6c 65 00  00 00 00 00   |...<#bundle.....|
              48   00 00 00 01  00 00 00 14  2f 62 61 72  00 00 00 00   |......../bar....|
              64   2c 73 66 00  62 61 7a 00  40 40 00 00  00 00 00 10   |,sf.baz.@@......|
              80   2f 66 66 66  66 00 00 00  2c 46 54 4e  00 00 00 00   |/ffff...,FTN....|
              96   61 00 00 00  62 00 00 00  63 00 00 00  64 00 00 00   |a...b...c...d...|
    """

    ### INITIALIZER ###

    def __init__(self, address: OscAddress, *contents: OscArgument) -> None:
        if isinstance(address, Enum):
            address = address.value
        if not isinstance(address, (str, int)):
            raise ValueError(f"address must be int or str, got {address}")
        self.address = address
        self.contents = tuple(contents)

    ### SPECIAL METHODS ###

    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False
        if self.address != other.address:
            return False
        if self.contents != other.contents:
            return False
        return True

    def __repr__(self) -> str:
        return "{}({})".format(
            type(self).__name__,
            ", ".join(repr(_) for _ in [self.address, *self.contents]),
        )

    def __str__(self) -> str:
        return format_datagram(bytearray(self.to_datagram()))

    ### PRIVATE METHODS ###

    @staticmethod
    def _decode_blob(data: bytes) -> tuple[bytes, bytes]:
        actual_length, remainder = struct.unpack(">I", data[:4])[0], data[4:]
        padded_length = actual_length
        if actual_length % 4 != 0:
            padded_length = (actual_length // 4 + 1) * 4
        return remainder[:padded_length][:actual_length], remainder[padded_length:]

    @staticmethod
    def _decode_string(data: bytes) -> tuple[str, bytes]:
        actual_length = data.index(b"\x00")
        padded_length = (actual_length // 4 + 1) * 4
        return str(data[:actual_length], "ascii"), data[padded_length:]

    @staticmethod
    def _encode_string(value: str) -> bytes:
        result = bytes(value + "\x00", "ascii")
        if len(result) % 4 != 0:
            width = (len(result) // 4 + 1) * 4
            result = result.ljust(width, b"\x00")
        return result

    @staticmethod
    def _encode_blob(value: bytes) -> bytes:
        result = bytes(struct.pack(">I", len(value)) + value)
        if len(result) % 4 != 0:
            width = (len(result) // 4 + 1) * 4
            result = result.ljust(width, b"\x00")
        return result

    @classmethod
    def _encode_value(cls, value: OscArgument) -> tuple[str, bytes]:
        type_tags, encoded_value = "", b""
        if isinstance(value, Enum):
            if isinstance(value.value, str):
                type_tags += "s"
                encoded_value = cls._encode_string(value.value)
            else:
                type_tags += "i"
                encoded_value += struct.pack(">i", value.value)
        elif isinstance(value, (OscBundle, OscMessage)):
            type_tags += "b"
            encoded_value = cls._encode_blob(value.to_datagram())
        elif isinstance(value, (bytearray, bytes)):
            type_tags += "b"
            encoded_value = cls._encode_blob(value)
        elif isinstance(value, str):
            type_tags += "s"
            encoded_value = cls._encode_string(value)
        elif isinstance(value, bool):
            type_tags += "T" if value else "F"
        elif isinstance(value, float):
            type_tags += "f"
            encoded_value += struct.pack(">f", value)
        elif isinstance(value, int):
            type_tags += "i"
            encoded_value += struct.pack(">i", value)
        elif value is None:
            type_tags += "N"
        elif isinstance(value, SequenceABC):
            type_tags += "["
            for sub_value in value:
                sub_type_tags, sub_encoded_value = cls._encode_value(sub_value)
                type_tags += sub_type_tags
                encoded_value += sub_encoded_value
            type_tags += "]"
        else:
            message = "Cannot encode {!r}".format(value)
            raise TypeError(message)
        return type_tags, encoded_value

    ### PUBLIC METHODS ###

    def to_datagram(self) -> bytes:
        # address can be a string or (in SuperCollider) an int
        if isinstance(self.address, str):
            encoded_address = self._encode_string(self.address)
        else:
            encoded_address = struct.pack(">i", self.address)
        encoded_type_tags = ","
        encoded_contents = b""
        for value in self.contents or ():
            type_tags, encoded_value = self._encode_value(value)
            encoded_type_tags += type_tags
            encoded_contents += encoded_value
        return (
            encoded_address + self._encode_string(encoded_type_tags) + encoded_contents
        )

    @classmethod
    def from_datagram(cls, datagram: bytes) -> "OscMessage":
        remainder = datagram
        address, remainder = cls._decode_string(remainder)
        type_tags, remainder = cls._decode_string(remainder)
        contents: list[OscArgument] = []
        array_stack = [contents]
        for type_tag in type_tags[1:]:
            if type_tag == "i":
                value, remainder = struct.unpack(">i", remainder[:4])[0], remainder[4:]
                array_stack[-1].append(value)
            elif type_tag == "f":
                value, remainder = struct.unpack(">f", remainder[:4])[0], remainder[4:]
                array_stack[-1].append(value)
            elif type_tag == "d":
                value, remainder = struct.unpack(">d", remainder[:8])[0], remainder[8:]
                array_stack[-1].append(value)
            elif type_tag == "s":
                value, remainder = cls._decode_string(remainder)
                array_stack[-1].append(value)
            elif type_tag == "b":
                value, remainder = cls._decode_blob(remainder)
                for class_ in (OscBundle, OscMessage):
                    try:
                        value = class_.from_datagram(value)
                        break
                    except Exception:
                        pass
                array_stack[-1].append(value)
            elif type_tag == "T":
                array_stack[-1].append(True)
            elif type_tag == "F":
                array_stack[-1].append(False)
            elif type_tag == "N":
                array_stack[-1].append(None)
            elif type_tag == "[":
                array: list[OscArgument] = []
                array_stack[-1].append(array)
                array_stack.append(array)
            elif type_tag == "]":
                array_stack.pop()
            else:
                raise RuntimeError(f"Unable to parse type {type_tag!r}")
        return cls(address, *contents)

    def to_list(self):
        result = [self.address]
        for x in self.contents:
            if hasattr(x, "to_list"):
                result.append(x.to_list())
            else:
                result.append(x)
        return result

    def to_osc(self) -> "OscMessage":
        return self


class OscBundle:
    """
    An OSC bundle.

    ::

        >>> import supriya.osc
        >>> message_one = supriya.osc.OscMessage("/one", 1)
        >>> message_two = supriya.osc.OscMessage("/two", 2)
        >>> message_three = supriya.osc.OscMessage("/three", 3)

    ::

        >>> inner_bundle = supriya.osc.OscBundle(
        ...     timestamp=1401557034.5,
        ...     contents=(message_one, message_two),
        ... )
        >>> inner_bundle
        OscBundle(timestamp=1401557034.5, contents=[OscMessage('/one', 1), OscMessage('/two', 2)])

    ::

        >>> print(inner_bundle)
        size 56
           0   23 62 75 6e  64 6c 65 00  d7 34 8e aa  80 00 00 00   |#bundle..4......|
          16   00 00 00 10  2f 6f 6e 65  00 00 00 00  2c 69 00 00   |..../one....,i..|
          32   00 00 00 01  00 00 00 10  2f 74 77 6f  00 00 00 00   |......../two....|
          48   2c 69 00 00  00 00 00 02                             |,i......|

    ::

        >>> outer_bundle = supriya.osc.OscBundle(
        ...     contents=(inner_bundle, message_three),
        ... )
        >>> outer_bundle
        OscBundle(contents=[OscBundle(timestamp=1401557034.5, contents=[OscMessage('/one', 1), OscMessage('/two', 2)]), OscMessage('/three', 3)])

    ::

        >>> print(outer_bundle)
        size 96
           0   23 62 75 6e  64 6c 65 00  00 00 00 00  00 00 00 01   |#bundle.........|
          16   00 00 00 38  23 62 75 6e  64 6c 65 00  d7 34 8e aa   |...8#bundle..4..|
          32   80 00 00 00  00 00 00 10  2f 6f 6e 65  00 00 00 00   |......../one....|
          48   2c 69 00 00  00 00 00 01  00 00 00 10  2f 74 77 6f   |,i........../two|
          64   00 00 00 00  2c 69 00 00  00 00 00 02  00 00 00 10   |....,i..........|
          80   2f 74 68 72  65 65 00 00  2c 69 00 00  00 00 00 03   |/three..,i......|

    ::

        >>> datagram = outer_bundle.to_datagram()

    ::

        >>> decoded_bundle = supriya.osc.OscBundle.from_datagram(datagram)
        >>> decoded_bundle
        OscBundle(contents=[OscBundle(timestamp=1401557034.5, contents=[OscMessage('/one', 1), OscMessage('/two', 2)]), OscMessage('/three', 3)])

    ::

        >>> decoded_bundle == outer_bundle
        True
    """

    ### INITIALIZER ###

    def __init__(
        self,
        timestamp: float | None = None,
        *,
        contents: SequenceABC[Union["OscBundle", "OscMessage"]],
    ) -> None:
        prototype = (OscMessage, type(self))
        self.timestamp = timestamp
        contents = contents or ()
        for x in contents or ():
            if not isinstance(x, prototype):
                raise ValueError(contents)
        self.contents = tuple(contents)

    ### SPECIAL METHODS ###

    def __eq__(self, other) -> bool:
        if type(self) is not type(other):
            return False
        if self.timestamp != other.timestamp:
            return False
        if self.contents != other.contents:
            return False
        return True

    def __repr__(self) -> str:
        parts = ["{}(".format(type(self).__name__)]
        if self.timestamp is not None:
            parts.append(f"timestamp={self.timestamp}")
            if self.contents:
                parts.append(", ")
        if self.contents:
            parts.append(f"contents={list(self.contents)!r}")
        parts.append(")")
        return "".join(parts)

    def __str__(self) -> str:
        return format_datagram(bytearray(self.to_datagram()))

    ### PRIVATE METHODS ###

    @staticmethod
    def _decode_date(data: bytes) -> tuple[float | None, bytes]:
        data, remainder = data[:8], data[8:]
        if data == IMMEDIATELY:
            return None, remainder
        date = (struct.unpack(">Q", data)[0] / SECONDS_TO_NTP_TIMESTAMP) - NTP_DELTA
        return date, remainder

    @staticmethod
    def _encode_date(seconds: float | None, realtime: bool = True) -> bytes:
        if seconds is None:
            return IMMEDIATELY
        if realtime:
            seconds = seconds + NTP_DELTA
        if seconds >= 4294967296:  # 2**32
            seconds = seconds % 4294967296
        return struct.pack(">Q", int(seconds * SECONDS_TO_NTP_TIMESTAMP))

    ### PUBLIC METHODS ###

    @classmethod
    def from_datagram(cls, datagram: bytes) -> "OscBundle":
        if not datagram.startswith(BUNDLE_PREFIX):
            raise ValueError("datagram is not a bundle")
        remainder = datagram[8:]
        timestamp, remainder = cls._decode_date(remainder)
        contents = []
        while len(remainder):
            length, remainder = struct.unpack(">i", remainder[:4])[0], remainder[4:]
            item: OscBundle | OscMessage
            if remainder.startswith(BUNDLE_PREFIX):
                item = cls.from_datagram(remainder[:length])
            else:
                item = OscMessage.from_datagram(remainder[:length])
            contents.append(item)
            remainder = remainder[length:]
        osc_bundle = cls(timestamp=timestamp, contents=tuple(contents))
        return osc_bundle

    @classmethod
    def partition(
        cls, messages: list[OscMessage], timestamp: float | None = None
    ) -> list["OscBundle"]:
        bundles = []
        contents = []
        messages_ = collections.deque(messages)
        remaining = maximum = 8192 - len(BUNDLE_PREFIX) - 4
        while messages_:
            message = messages_.popleft()
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

    def to_datagram(self, realtime: bool = True) -> bytes:
        datagram: bytes = BUNDLE_PREFIX
        datagram += self._encode_date(self.timestamp, realtime=realtime)
        for content in self.contents:
            content_datagram = content.to_datagram()
            datagram += struct.pack(">i", len(content_datagram))
            datagram += content_datagram
        return datagram

    def to_list(self):
        result = [self.timestamp]
        result.append([x.to_list() for x in self.contents])
        return result

    def to_osc(self) -> "OscBundle":
        return self


def format_messages(messages: Sequence[OscBundle | OscMessage]) -> str:
    """
    Format a sequence of OSC messages as a string.

    Provides a more concise means of verifying OSC contents in the test suite
    than comparing the messages directly.
    """

    def sanitize(list_):
        for i, x in enumerate(list_):
            if isinstance(x, bytes):
                try:
                    decompiled = decompile_synthdefs(x)
                    list_[i] = decompiled[0] if len(decompiled) == 1 else decompiled
                except Exception:
                    pass
            elif isinstance(x, list):
                sanitize(x)
        return list_

    lines: list[str] = []
    for message in messages:
        sanitized = sanitize(message.to_list())
        formatted = pprint.pformat(sanitized, width=120)
        for i, line in enumerate(formatted.splitlines()):
            if i == 0:
                prefix = "-"
            else:
                prefix = " "
            lines.append(f"{prefix} {line}")
    return "\n".join(lines)


def find_free_port() -> int:
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


class OscProtocolOffline(Exception):
    pass


class OscProtocolAlreadyConnected(Exception):
    pass


class OscCallback(NamedTuple):
    protocol: "OscProtocol"
    pattern: tuple[str | int | float, ...]
    procedure: Callable
    failure_pattern: tuple[float | int | str, ...] | None = None
    once: bool = False
    args: tuple | None = None
    kwargs: dict | None = None

    def unregister(self) -> None:
        self.protocol.unregister(self)


@dataclasses.dataclass
class HealthCheck:
    request_pattern: list[str]
    response_pattern: list[str]
    active: bool = True
    timeout: float = 1.0
    backoff_factor: float = 1.5
    max_attempts: int = 5


class CaptureEntry(NamedTuple):
    timestamp: float
    label: Literal["R", "S"]
    message: OscBundle | OscMessage
    raw_message: SequenceABC | SupportsOsc | str | None = None


class Capture:
    ### INITIALIZER ###

    def __init__(self, osc_protocol: "OscProtocol") -> None:
        self.osc_protocol = osc_protocol
        self.entries: list[CaptureEntry] = []

    ### SPECIAL METHODS ###

    def __enter__(self) -> "Capture":
        self.osc_protocol.captures.add(self)
        self.entries[:] = []
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.osc_protocol.captures.remove(self)

    def __getitem__(self, i: int | slice) -> CaptureEntry | list[CaptureEntry]:
        return self.entries[i]

    def __iter__(self) -> Iterator[CaptureEntry]:
        return iter(self.entries)

    def __len__(self) -> int:
        return len(self.entries)

    ### PUBLIC METHODS ###

    def add_entry(
        self,
        timestamp: float,
        label: Literal["R", "S"],
        message: OscBundle | OscMessage,
        raw_message: SequenceABC | SupportsOsc | str | None = None,
    ) -> None:
        self.entries.append(
            CaptureEntry(
                timestamp=timestamp,
                label=label,
                message=message,
                raw_message=raw_message,
            )
        )

    def filtered(
        self, sent: bool = True, received: bool = True, status: bool = False
    ) -> list[CaptureEntry]:
        entries = []
        for entry in self.entries:
            if entry.label == "R" and not received:
                continue
            if entry.label == "S" and not sent:
                continue
            if (
                not status
                and isinstance(entry.message, OscMessage)
                and entry.message.address in ("/status", "/status.reply")
            ):
                continue
            entries.append(entry)
        return entries


class OscProtocol:
    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name: str | None = None,
        on_connect_callback: Callable | None = None,
        on_disconnect_callback: Callable | None = None,
        on_panic_callback: Callable | None = None,
    ) -> None:
        self.callbacks: dict[Any, Any] = {}
        self.captures: set[Capture] = set()
        self.healthcheck: HealthCheck | None = None
        self.healthcheck_osc_callback: OscCallback | None = None
        self.attempts = 0
        self.ip_address = "127.0.0.1"
        self.name = name
        self.port = 57551
        self.on_connect_callback = on_connect_callback
        self.on_disconnect_callback = on_disconnect_callback
        self.on_panic_callback = on_panic_callback
        self.status = BootStatus.OFFLINE

    ### PRIVATE METHODS ###

    def _activate_healthcheck(self) -> bool:
        if not self.healthcheck:
            return False
        elif self.healthcheck.active:
            return False
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            "activating healthcheck..."
        )
        return True

    def _add_callback(self, callback: OscCallback) -> None:
        patterns = [callback.pattern]
        if callback.failure_pattern:
            patterns.append(callback.failure_pattern)
        for pattern in patterns:
            callback_map = self.callbacks
            for item in pattern:
                callbacks, callback_map = callback_map.setdefault(item, ([], {}))
            callbacks.append(callback)

    def _disconnect(self, panicked: bool = False) -> Awaitable[None] | None:
        if panicked:
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
                "panicking ..."
            )
        else:
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
                "disconnecting ..."
            )
        self.status = BootStatus.QUITTING
        if self.healthcheck_osc_callback is not None:
            self.unregister(self.healthcheck_osc_callback)
        return None

    def _match_callbacks(self, message) -> list[OscCallback]:
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

    def _on_connect(self, *, boot_future: FutureLike[bool]) -> Awaitable[None] | None:
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            "... connected!"
        )
        self.status = BootStatus.ONLINE
        boot_future.set_result(True)
        return None

    def _on_disconnect(
        self,
        *,
        boot_future: FutureLike[bool],
        exit_future: FutureLike[bool],
        panicked: bool = False,
    ) -> Awaitable[None] | None:
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            "... disconnected!"
        )
        self.status = BootStatus.OFFLINE
        if not boot_future.done():
            boot_future.set_result(False)
        if not exit_future.done():
            exit_future.set_result(not panicked)
        return None

    def _on_healthcheck_passed(self, message: OscMessage) -> Awaitable[None] | None:
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            "healthcheck: passed"
        )
        self.attempts = 0
        return None

    def _remove_callback(self, callback: OscCallback) -> None:
        def delete(pattern, original_callback_map) -> None:
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

    def _register(
        self,
        pattern,
        procedure,
        *,
        failure_pattern=None,
        once: bool = False,
        args: tuple | None = None,
        kwargs: dict | None = None,
    ) -> OscCallback:
        if isinstance(pattern, (str, int, float)):
            pattern = [pattern]
        if isinstance(failure_pattern, (str, int, float)):
            failure_pattern = [failure_pattern]
        if not callable(procedure):
            raise ValueError(procedure)
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
            f"registering pattern: {pattern!r}"
        )
        return OscCallback(
            protocol=self,
            pattern=tuple(pattern),
            failure_pattern=failure_pattern,
            procedure=procedure,
            once=bool(once),
            args=args,
            kwargs=kwargs,
        )

    def _send(self, raw_message: SequenceABC | SupportsOsc | str) -> bytes:
        if self.status not in (BootStatus.BOOTING, BootStatus.ONLINE):
            raise OscProtocolOffline
        if not isinstance(raw_message, (str, SequenceABC, SupportsOsc)):
            raise ValueError(raw_message)
        message: OscBundle | OscMessage
        if isinstance(raw_message, str):
            message = OscMessage(raw_message)
        elif isinstance(raw_message, SequenceABC):
            message = OscMessage(*raw_message)
        else:
            message = raw_message.to_osc()
        osc_out_logger.debug(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] {message!r}"
        )
        for capture in self.captures:
            capture.add_entry(
                timestamp=time.time(),
                label="S",
                message=message,
                raw_message=raw_message,
            )
        datagram = message.to_datagram()
        udp_out_logger.debug(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] {datagram!r}"
        )
        return datagram

    def _setup(
        self, ip_address: str, port: int, healthcheck: HealthCheck | None
    ) -> None:
        self.status = BootStatus.BOOTING
        self.ip_address = ip_address
        self.port = port
        self.healthcheck = healthcheck
        if self.healthcheck:
            self.healthcheck_osc_callback = self.register(
                pattern=self.healthcheck.response_pattern,
                procedure=self._on_healthcheck_passed,
            )

    def _validate_receive(
        self, datagram
    ) -> Generator[tuple[OscCallback, OscMessage], None, None]:
        udp_in_logger.debug(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] {datagram}"
        )
        try:
            message = OscMessage.from_datagram(datagram)
        except Exception:
            raise
        osc_in_logger.debug(
            f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] {message!r}"
        )
        for capture in self.captures:
            capture.add_entry(timestamp=time.time(), label="R", message=message)
        for callback in self._match_callbacks(message):
            yield callback, message

    ### PUBLIC METHODS ###

    def activate_healthcheck(self) -> None:
        raise NotImplementedError

    def capture(self) -> "Capture":
        return Capture(self)

    def disconnect(self) -> Awaitable[None] | None:
        raise NotImplementedError

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
        raise NotImplementedError

    def send(self, message: SequenceABC | SupportsOsc | str) -> None:
        raise NotImplementedError

    def unregister(self, callback: OscCallback) -> None:
        raise NotImplementedError


class ThreadedOscProtocol(OscProtocol):
    class Server(socketserver.UDPServer):
        osc_protocol: "ThreadedOscProtocol"

        def verify_request(self, request, client_address) -> bool:
            self.osc_protocol._process_command_queue()
            return True

        def service_actions(self) -> None:
            if cast(HealthCheck, self.osc_protocol.healthcheck).active:
                self.osc_protocol._run_healthcheck()

    class Handler(socketserver.BaseRequestHandler):
        def handle(self) -> None:
            data = self.request[0]
            for callback, message in cast(
                ThreadedOscProtocol.Server, self.server
            ).osc_protocol._validate_receive(data):
                callback.procedure(
                    message, *(callback.args or ()), **(callback.kwargs or {})
                )

    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name: str | None = None,
        on_connect_callback: Callable | None = None,
        on_disconnect_callback: Callable | None = None,
        on_panic_callback: Callable | None = None,
    ):
        OscProtocol.__init__(
            self,
            name=name,
            on_connect_callback=on_connect_callback,
            on_disconnect_callback=on_disconnect_callback,
            on_panic_callback=on_panic_callback,
        )
        self.boot_future: concurrent.futures.Future[bool] = concurrent.futures.Future()
        self.exit_future: concurrent.futures.Future[bool] = concurrent.futures.Future()
        self.command_queue: Queue[tuple[Literal["add", "remove"], OscCallback]] = (
            Queue()
        )
        self.healthcheck_deadline = 0.0
        self.lock = threading.RLock()

    ### PRIVATE METHODS ###

    def _disconnect(self, panicked: bool = False) -> None:
        super()._disconnect(panicked=panicked)
        if not self.osc_server._BaseServer__shutdown_request:  # type: ignore
            # We set the shutdown request flag rather than call .shutdown()
            # because this is often being called from _inside_ the server
            # thread.
            # N.B. Can't figure out how to make Mypy play nice with this.
            self.osc_server._BaseServer__shutdown_request = True  # type: ignore
        self._on_disconnect(
            boot_future=self.boot_future,
            exit_future=self.exit_future,
            panicked=panicked,
        )

    def _on_connect(self, boot_future: FutureLike[bool]) -> None:
        super()._on_connect(boot_future=boot_future)
        if self.on_connect_callback:
            self.on_connect_callback()

    def _on_disconnect(
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

    def _on_healthcheck_passed(self, message: OscMessage) -> None:
        super()._on_healthcheck_passed(message)
        if self.status == BootStatus.BOOTING:
            self._on_connect(boot_future=self.boot_future)

    def _process_command_queue(self) -> None:
        while self.command_queue.qsize():
            try:
                action, callback = self.command_queue.get()
            except Empty:
                continue
            if action == "add":
                self._add_callback(callback)
            elif action == "remove":
                self._remove_callback(callback)

    def _run_healthcheck(self) -> None:
        if self.healthcheck is None:
            return
        now = time.time()
        if now < self.healthcheck_deadline:
            return
        if self.attempts > 0:
            remaining = self.healthcheck.max_attempts - self.attempts
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
                f"healthcheck failed, {remaining} attempts remaining"
            )
        new_timeout = self.healthcheck.timeout * pow(
            self.healthcheck.backoff_factor, self.attempts
        )
        self.healthcheck_deadline = now + new_timeout
        self.attempts += 1
        if self.attempts <= self.healthcheck.max_attempts:
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
                "healthcheck: checking ..."
            )
            self.send(OscMessage(*self.healthcheck.request_pattern))
            return
        self._disconnect(panicked=True)

    def _server_factory(self, ip_address, port) -> "Server":
        server = self.Server(
            (self.ip_address, self.port), self.Handler, bind_and_activate=False
        )
        server.osc_protocol = self
        return server

    ### PUBLIC METHODS ###

    def activate_healthcheck(self) -> None:
        if self._activate_healthcheck():
            cast(HealthCheck, self.healthcheck).active = True

    def connect(
        self, ip_address: str, port: int, *, healthcheck: HealthCheck | None = None
    ) -> None:
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
        self.healthcheck_deadline = time.time()
        self.boot_future = concurrent.futures.Future()
        self.exit_future = concurrent.futures.Future()
        self.osc_server = self._server_factory(ip_address, port)
        self.osc_server_thread = threading.Thread(target=self.osc_server.serve_forever)
        self.osc_server_thread.daemon = True
        self.osc_server_thread.start()
        if not self.healthcheck:
            self._on_connect(boot_future=self.boot_future)

    def disconnect(self) -> None:
        if self.status != BootStatus.ONLINE:
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}/{self.name or hex(id(self))}] "
                "already disconnected!"
            )
            return
        self._disconnect()

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
        # Command queue prevents lock contention.
        self.command_queue.put(
            (
                "add",
                callback := self._register(
                    pattern,
                    procedure,
                    failure_pattern=failure_pattern,
                    once=once,
                    args=args,
                    kwargs=kwargs,
                ),
            )
        )
        return callback

    def send(self, message: SequenceABC | SupportsOsc | str) -> None:
        try:
            self.osc_server.socket.sendto(
                self._send(message),
                (self.ip_address, self.port),
            )
        except OSError:
            # print(message)
            raise

    def unregister(self, callback: OscCallback) -> None:
        """
        Unregister a callback.
        """
        # Command queue prevents lock contention.
        self.command_queue.put(("remove", callback))


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
