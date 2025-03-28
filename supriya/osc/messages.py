import collections
import datetime
import struct
import time
from collections.abc import Sequence as SequenceABC
from enum import Enum
from typing import TypeAlias, Union

from ..utils import group_by_count

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
