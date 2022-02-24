import collections
import datetime
import enum
import struct
import time
from collections.abc import Sequence

from supriya.system import SupriyaValueObject

from .utils import format_datagram

BUNDLE_PREFIX = b"#bundle\x00"
IMMEDIATELY = struct.pack(">Q", 1)
NTP_TIMESTAMP_TO_SECONDS = 1.0 / 2.0**32.0
SECONDS_TO_NTP_TIMESTAMP = 2.0**32.0
SYSTEM_EPOCH = datetime.date(*time.gmtime(0)[0:3])
NTP_EPOCH = datetime.date(1900, 1, 1)
NTP_DELTA = (SYSTEM_EPOCH - NTP_EPOCH).days * 24 * 3600


class OscMessage(SupriyaValueObject):
    """
    An OSC message.

    ..  container:: example

        ::

            >>> from supriya.osc import OscMessage
            >>> osc_message = OscMessage("/g_new", 0, 0)
            >>> osc_message
            OscMessage('/g_new', 0, 0)

        ::

            >>> datagram = osc_message.to_datagram()
            >>> OscMessage.from_datagram(datagram)
            OscMessage('/g_new', 0, 0)

    ..  container:: example

        ::

            >>> osc_message = OscMessage("/foo", True, [None, [3.25]], OscMessage("/bar"))
            >>> osc_message
            OscMessage('/foo', True, [None, [3.25]], OscMessage('/bar'))

        ::

            >>> datagram = osc_message.to_datagram()
            >>> OscMessage.from_datagram(datagram)
            OscMessage('/foo', True, [None, [3.25]], OscMessage('/bar'))

    ..  container:: example

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

    """

    ### CLASS VARIABLES ###

    __slots__ = ("address", "contents")

    ### INITIALIZER ###

    def __init__(self, address, *contents):
        if isinstance(address, enum.Enum):
            address = address.value
        if not isinstance(address, (str, int)):
            raise ValueError(f"address must be int or str, got {address}")
        self.address = address
        self.contents = tuple(contents)

    ### SPECIAL METHODS ###

    def __repr__(self):
        return "{}({})".format(
            type(self).__name__,
            ", ".join(repr(x) for x in (self.address,) + self.contents),
        )

    def __str__(self):
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
        elif isinstance(value, Sequence):
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

    def to_datagram(self):
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


class OscBundle(SupriyaValueObject):
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

    __slots__ = ("contents", "timestamp")

    ### INITIALIZER ###

    def __init__(self, timestamp=None, contents=None):
        prototype = (OscMessage, type(self))
        self.timestamp = timestamp
        contents = contents or ()
        for x in contents or ():
            if not isinstance(x, prototype):
                raise ValueError(contents)
        self.contents = tuple(contents)

    ### SPECIAL METHODS ###

    def __str__(self):
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
            return struct.pack(">Q", int(seconds * SECONDS_TO_NTP_TIMESTAMP))
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

    def to_datagram(self, realtime=True):
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
