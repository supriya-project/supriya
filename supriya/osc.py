"""
Tools for sending, receiving and handling OSC messages.
"""

import abc
import asyncio
import collections
import contextlib
import dataclasses
import datetime
import enum
import inspect
import logging
import queue
import socket
import socketserver
import struct
import threading
import time
from collections.abc import Sequence as SequenceABC
from typing import (
    Any,
    Callable,
    Dict,
    List,
    NamedTuple,
    Optional,
    Sequence,
    Set,
    Tuple,
    Union,
)

from uqbar.objects import get_repr

from .utils import group_iterable_by_count

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
            OscMessage('/foo', 1, 2.5, OscBundle(
                contents=(
                    OscMessage('/bar', 'baz', 3.0),
                    OscMessage('/ffff', False, True, None),
                ),
            ), ['a', 'b', ['c', 'd']])

        ::

            >>> datagram = osc_message.to_datagram()
            >>> OscMessage.from_datagram(datagram)
            OscMessage('/foo', 1, 2.5, OscBundle(
                contents=(
                    OscMessage('/bar', 'baz', 3.0),
                    OscMessage('/ffff', False, True, None),
                ),
            ), ['a', 'b', ['c', 'd']])

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

    def __init__(self, address, *contents) -> None:
        if isinstance(address, enum.Enum):
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
    def _decode_blob(data):
        actual_length, remainder = struct.unpack(">I", data[:4])[0], data[4:]
        padded_length = actual_length
        if actual_length % 4 != 0:
            padded_length = (actual_length // 4 + 1) * 4
        return remainder[:padded_length][:actual_length], remainder[padded_length:]

    @staticmethod
    def _decode_string(data):
        actual_length = data.index(b"\x00")
        padded_length = (actual_length // 4 + 1) * 4
        return str(data[:actual_length], "ascii"), data[padded_length:]

    @staticmethod
    def _encode_string(value):
        result = bytes(value + "\x00", "ascii")
        if len(result) % 4 != 0:
            width = (len(result) // 4 + 1) * 4
            result = result.ljust(width, b"\x00")
        return result

    @staticmethod
    def _encode_blob(value):
        result = bytes(struct.pack(">I", len(value)) + value)
        if len(result) % 4 != 0:
            width = (len(result) // 4 + 1) * 4
            result = result.ljust(width, b"\x00")
        return result

    @classmethod
    def _encode_value(cls, value):
        if hasattr(value, "to_datagram"):
            value = bytearray(value.to_datagram())
        elif isinstance(value, enum.Enum):
            value = value.value
        type_tags, encoded_value = "", b""
        if isinstance(value, (bytearray, bytes)):
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
    def from_datagram(cls, datagram):
        remainder = datagram
        address, remainder = cls._decode_string(remainder)
        type_tags, remainder = cls._decode_string(remainder)
        contents = []
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
                array = []
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
        OscBundle(
            contents=(
                OscMessage('/one', 1),
                OscMessage('/two', 2),
            ),
            timestamp=1401557034.5,
        )

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

    ### INITIALIZER ###

    def __init__(self, timestamp=None, contents=None) -> None:
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
        return get_repr(self)

    def __str__(self) -> str:
        return format_datagram(bytearray(self.to_datagram()))

    ### PRIVATE METHODS ###

    @staticmethod
    def _decode_date(data):
        data, remainder = data[:8], data[8:]
        if data == IMMEDIATELY:
            return None, remainder
        date = (struct.unpack(">Q", data)[0] / SECONDS_TO_NTP_TIMESTAMP) - NTP_DELTA
        return date, remainder

    @staticmethod
    def _encode_date(seconds, realtime=True):
        if seconds is None:
            return IMMEDIATELY
        if realtime:
            seconds = seconds + NTP_DELTA
        if seconds >= 4294967296:  # 2**32
            seconds = seconds % 4294967296
        return struct.pack(">Q", int(seconds * SECONDS_TO_NTP_TIMESTAMP))

    ### PUBLIC METHODS ###

    @classmethod
    def from_datagram(cls, datagram):
        if not datagram.startswith(BUNDLE_PREFIX):
            raise ValueError("datagram is not a bundle")
        remainder = datagram[8:]
        timestamp, remainder = cls._decode_date(remainder)
        contents = []
        while len(remainder):
            length, remainder = struct.unpack(">i", remainder[:4])[0], remainder[4:]
            if remainder.startswith(BUNDLE_PREFIX):
                item = cls.from_datagram(remainder[:length])
            else:
                item = OscMessage.from_datagram(remainder[:length])
            contents.append(item)
            remainder = remainder[length:]
        osc_bundle = cls(timestamp=timestamp, contents=tuple(contents))
        return osc_bundle

    @classmethod
    def partition(cls, messages, timestamp=None):
        bundles = []
        contents = []
        message = collections.deque(messages)
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

    def to_datagram(self, realtime=True) -> bytes:
        datagram = BUNDLE_PREFIX
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
    request_pattern: List[str]
    response_pattern: List[str]
    callback: Callable
    active: bool = True
    timeout: float = 1.0
    backoff_factor: float = 1.5
    max_attempts: int = 5


class OscProtocol(metaclass=abc.ABCMeta):
    ### INITIALIZER ###

    def __init__(self) -> None:
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

    def _disconnect(self) -> None:
        raise NotImplementedError

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

    def _pass_healthcheck(self, message):
        osc_protocol_logger.info(f"[{self.ip_address}:{self.port}] healthcheck: passed")
        self.attempts = 0

    def _setup(self, ip_address, port, healthcheck):
        self.ip_address = ip_address
        self.port = port
        self.healthcheck = healthcheck
        if self.healthcheck:
            self.healthcheck_osc_callback = self.register(
                pattern=self.healthcheck.response_pattern,
                procedure=self._pass_healthcheck,
            )

    def _teardown(self):
        osc_protocol_logger.info(f"[{self.ip_address}:{self.port}] Tearing down...")
        self.is_running = False
        if self.healthcheck is not None:
            self.unregister(self.healthcheck_osc_callback)

    def _validate_callback(
        self, pattern, procedure, *, failure_pattern=None, once=False
    ):
        if isinstance(pattern, (str, int, float)):
            pattern = [pattern]
        if isinstance(failure_pattern, (str, int, float)):
            failure_pattern = [failure_pattern]
        if not callable(procedure):
            raise ValueError(procedure)
        return OscCallback(
            pattern=tuple(pattern),
            failure_pattern=failure_pattern,
            procedure=procedure,
            once=bool(once),
        )

    def _validate_receive(self, datagram):
        udp_in_logger.debug(f"[{self.ip_address}:{self.port}] {datagram}")
        try:
            message = OscMessage.from_datagram(datagram)
        except Exception:
            raise
        osc_in_logger.debug(f"[{self.ip_address}:{self.port}] {message!r}")
        for capture in self.captures:
            capture.messages.append(
                CaptureEntry(timestamp=time.time(), label="R", message=message)
            )
        for callback in self._match_callbacks(message):
            yield callback.procedure, message

    def _validate_send(self, message):
        if not self.is_running:
            raise OscProtocolOffline
        if not isinstance(message, (str, SequenceABC, OscBundle, OscMessage)):
            raise ValueError(message)
        if isinstance(message, str):
            message = OscMessage(message)
        elif isinstance(message, SequenceABC):
            message = OscMessage(*message)
        osc_out_logger.debug(f"[{self.ip_address}:{self.port}] {message!r}")
        for capture in self.captures:
            capture.messages.append(
                CaptureEntry(timestamp=time.time(), label="S", message=message)
            )
        datagram = message.to_datagram()
        udp_out_logger.debug(f"[{self.ip_address}:{self.port}] {datagram}")
        return datagram

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def activate_healthcheck(self) -> None:
        raise NotImplementedError

    def capture(self) -> "Capture":
        return Capture(self)

    def disconnect(self) -> None:
        osc_protocol_logger.info(f"[{self.ip_address}:{self.port}] disconnecting")
        self._disconnect()
        osc_protocol_logger.info(f"[{self.ip_address}:{self.port}] ...disconnected")

    @abc.abstractmethod
    def register(
        self,
        pattern: Sequence[Union[str, float]],
        procedure: Callable[[OscMessage], None],
        *,
        failure_pattern: Optional[Sequence[Union[str, float]]] = None,
        once: bool = False,
    ) -> OscCallback:
        raise NotImplementedError

    @abc.abstractmethod
    def send(self, message) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def unregister(self, callback: OscCallback):
        raise NotImplementedError


class AsyncOscProtocol(asyncio.DatagramProtocol, OscProtocol):
    ### INITIALIZER ###

    def __init__(self) -> None:
        asyncio.DatagramProtocol.__init__(self)
        OscProtocol.__init__(self)
        self.background_tasks: Set[asyncio.Task] = set()
        self.healthcheck_task: Optional[asyncio.Task] = None

    ### PRIVATE METHODS ###

    def _disconnect(self) -> None:
        if not self.is_running:
            osc_protocol_logger.info(
                f"{self.ip_address}:{self.port} already disconnected!"
            )
            return
        self._teardown()
        self.transport.close()
        if self.healthcheck_task:
            self.healthcheck_task.cancel()

    async def _run_healthcheck(self):
        while self.is_running:
            if self.attempts >= self.healthcheck.max_attempts:
                osc_protocol_logger.info(
                    f"[{self.ip_address}:{self.port}] health check: failure limit exceeded"
                )
                self.exit_future.set_result(True)
                self._teardown()
                self.transport.close()
                obj_ = self.healthcheck.callback()
                if asyncio.iscoroutine(obj_):
                    asyncio.get_running_loop().create_task(obj_)
                return
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}] healthcheck: checking..."
            )
            self.send(OscMessage(*self.healthcheck.request_pattern))
            sleep_time = self.healthcheck.timeout * pow(
                self.healthcheck.backoff_factor, self.attempts
            )
            self.attempts += 1
            await asyncio.sleep(sleep_time)

    ### PUBLIC METHODS ###

    def activate_healthcheck(self) -> None:
        if not self.healthcheck:
            return
        elif self.healthcheck.active:
            return
        self.healthcheck_task = asyncio.get_running_loop().create_task(
            self._run_healthcheck()
        )

    async def connect(
        self, ip_address: str, port: int, *, healthcheck: Optional[HealthCheck] = None
    ):
        osc_protocol_logger.info(f"[{self.ip_address}:{self.port}] connecting...")
        if self.is_running:
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}] already connected!"
            )
            raise OscProtocolAlreadyConnected
        self._setup(ip_address, port, healthcheck)
        loop = asyncio.get_running_loop()
        self.exit_future = loop.create_future()
        _, protocol = await loop.create_datagram_endpoint(
            lambda: self, remote_addr=(ip_address, port)
        )
        if self.healthcheck and self.healthcheck.active:
            self.healthcheck_task = asyncio.get_running_loop().create_task(
                self._run_healthcheck()
            )
        osc_protocol_logger.info(f"[{self.ip_address}:{self.port}] ...connected")

    def connection_made(self, transport):
        osc_protocol_logger.info(f"[{self.ip_address}:{self.port}] connection made")
        self.transport = transport
        self.is_running = True

    def connection_lost(self, exc):
        osc_protocol_logger.info(f"[{self.ip_address}:{self.port}] connection lost")
        self.exit_future.set_result(True)

    def datagram_received(self, data, addr):
        loop = asyncio.get_running_loop()
        for callback, message in self._validate_receive(data):
            if inspect.iscoroutinefunction(callback):
                task = loop.create_task(callback(message))
                self.background_tasks.add(task)
                task.add_done_callback(self.background_tasks.discard)
            else:
                callback(message)

    def error_received(self, exc):
        osc_out_logger.warning(f"[{self.ip_address}:{self.port}] errored: {exc}")

    def register(
        self,
        pattern: Sequence[Union[str, float]],
        procedure: Callable[[OscMessage], None],
        *,
        failure_pattern: Optional[Sequence[Union[str, float]]] = None,
        once: bool = False,
    ) -> OscCallback:
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}] registering pattern: {pattern!r}"
        )
        callback = self._validate_callback(
            pattern, procedure, failure_pattern=failure_pattern, once=once
        )
        self._add_callback(callback)
        return callback

    def send(self, message):
        osc_protocol_logger.debug(
            f"[{self.ip_address}:{self.port}] sending: {message!r}"
        )
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
        if self.osc_protocol.healthcheck.active:
            self.osc_protocol._run_healthcheck()


class ThreadedOscHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0]
        for procedure, message in self.server.osc_protocol._validate_receive(data):
            procedure(message)


class ThreadedOscProtocol(OscProtocol):
    ### INITIALIZER ###

    def __init__(self):
        OscProtocol.__init__(self)
        self.command_queue = queue.Queue()
        self.lock = threading.RLock()
        self.osc_server = None
        self.osc_server_thread = None

    ### PRIVATE METHODS ###

    def _disconnect(self) -> None:
        with self.lock:
            if not self.is_running:
                osc_protocol_logger.info(
                    f"{self.ip_address}:{self.port} already disconnected!"
                )
                return
            self._teardown()
            if not self.osc_server._BaseServer__shutdown_request:
                self.osc_server.shutdown()
            self.osc_server = None
            self.osc_server_thread = None

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
        if self.healthcheck is None:
            return
        now = time.time()
        if now < self.healthcheck_deadline:
            return
        if self.attempts > 0:
            remaining = self.healthcheck.max_attempts - self.attempts
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}] healthcheck failed, {remaining} attempts remaining"
            )
        new_timeout = self.healthcheck.timeout * pow(
            self.healthcheck.backoff_factor, self.attempts
        )
        self.healthcheck_deadline = now + new_timeout
        self.attempts += 1
        if self.attempts <= self.healthcheck.max_attempts:
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}] healthcheck: checking..."
            )
            self.send(OscMessage(*self.healthcheck.request_pattern))
            return
        osc_protocol_logger.info(
            f"[{self.ip_address}:{self.port}] healthcheck: failure limit exceeded"
        )
        self.osc_server._BaseServer__shutdown_request = True
        self.disconnect()
        self.healthcheck.callback()

    def _server_factory(self, ip_address, port):
        server = ThreadedOscServer(
            (self.ip_address, self.port), ThreadedOscHandler, bind_and_activate=False
        )
        server.osc_protocol = self
        return server

    ### PUBLIC METHODS ###

    def activate_healthcheck(self) -> None:
        if not self.healthcheck:
            return
        elif self.healthcheck.active:
            return
        self.healthcheck.active = True

    def connect(
        self, ip_address: str, port: int, *, healthcheck: Optional[HealthCheck] = None
    ):
        osc_protocol_logger.info(f"[{self.ip_address}:{self.port}] connecting...")
        if self.is_running:
            osc_protocol_logger.info(
                f"[{self.ip_address}:{self.port}] already connected!"
            )
            raise OscProtocolAlreadyConnected
        self._setup(ip_address, port, healthcheck)
        self.healthcheck_deadline = time.time()
        self.osc_server = self._server_factory(ip_address, port)
        self.osc_server_thread = threading.Thread(target=self.osc_server.serve_forever)
        self.osc_server_thread.daemon = True
        self.osc_server_thread.start()
        self.is_running = True
        osc_protocol_logger.info(f"[{self.ip_address}:{self.port}] ...connected")

    def register(
        self,
        pattern: Sequence[Union[str, float]],
        procedure: Callable[[OscMessage], None],
        *,
        failure_pattern: Optional[Sequence[Union[str, float]]] = None,
        once: bool = False,
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

    def send(self, message) -> None:
        datagram = self._validate_send(message)
        try:
            self.osc_server.socket.sendto(datagram, (self.ip_address, self.port))
        except OSError:
            # print(message)
            raise

    def unregister(self, callback: OscCallback) -> None:
        """
        Unregister a callback.
        """
        # Command queue prevents lock contention.
        self.command_queue.put(("remove", callback))


class CaptureEntry(NamedTuple):
    timestamp: float
    label: str
    message: Union[OscMessage, OscBundle]


class Capture:
    ### INITIALIZER ###

    def __init__(self, osc_protocol):
        self.osc_protocol = osc_protocol
        self.messages = []

    ### SPECIAL METHODS ###

    def __enter__(self):
        self.osc_protocol.captures.add(self)
        self.messages[:] = []
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.osc_protocol.captures.remove(self)

    def __iter__(self):
        return iter(self.messages)

    def __len__(self):
        return len(self.messages)

    ### PUBLIC METHODS ###

    def filtered(
        self, sent=True, received=True, status=True
    ) -> List[Union[OscBundle, OscMessage]]:
        messages = []
        for _, label, message in self.messages:
            if label == "R" and not received:
                continue
            if label == "S" and not sent:
                continue
            if (
                isinstance(message, OscMessage)
                and message.address in ("/status", "/status.reply")
                and not status
            ):
                continue
            messages.append(message)
        return messages

    ### PUBLIC PROPERTIES ###

    @property
    def received_messages(self):
        return [
            (timestamp, osc_message)
            for timestamp, label, osc_message in self.messages
            if label == "R"
        ]

    @property
    def sent_messages(self):
        return [
            (timestamp, osc_message)
            for timestamp, label, osc_message in self.messages
            if label == "S"
        ]


def find_free_port():
    with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_DGRAM)) as s:
        s.bind(("", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def format_datagram(datagram):
    result = []
    result.append("size {}".format(len(datagram)))
    index = 0
    while index < len(datagram):
        chunk = datagram[index : index + 16]
        line = "{: >4}   ".format(index)
        hex_blocks = []
        ascii_block = ""
        for chunk in group_iterable_by_count(chunk, 4):
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


__all__ = [
    "AsyncOscProtocol",
    "Capture",
    "CaptureEntry",
    "HealthCheck",
    "OscBundle",
    "OscCallback",
    "OscMessage",
    "OscProtocol",
    "ThreadedOscProtocol",
    "find_free_port",
]
