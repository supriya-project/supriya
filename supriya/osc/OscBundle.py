import datetime
import decimal
import struct

from supriya.osc import format_datagram
from supriya.system.SupriyaValueObject import SupriyaValueObject


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

    _bundle_prefix = b"#bundle\x00"
    _immediately = struct.pack(">q", 1)

    ### INITIALIZER ###

    def __init__(self, timestamp=None, contents=None):
        import supriya.osc

        prototype = (supriya.osc.OscMessage, type(self))
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

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_ntp_delta():
        import time

        system_epoch = datetime.date(*time.gmtime(0)[0:3])
        ntp_epoch = datetime.date(1900, 1, 1)
        ntp_delta = (system_epoch - ntp_epoch).days * 24 * 3600
        return ntp_delta

    @staticmethod
    def _ntp_to_system_time(date):
        return float(date) - OscBundle._get_ntp_delta()

    @staticmethod
    def _read_date(payload, offset):
        if payload[offset : offset + 8] == OscBundle._immediately:
            date = None
        else:
            seconds, fraction = struct.unpack(">II", payload[offset : offset + 8])
            date = decimal.Decimal("{!s}.{!s}".format(seconds, fraction))
            date = float(date)
            date = OscBundle._ntp_to_system_time(date)
        offset += 8
        return date, offset

    @staticmethod
    def _system_time_to_ntp(date):
        return float(date) + OscBundle._get_ntp_delta()

    @staticmethod
    def _write_date(value, realtime=True):
        if value is None:
            return OscBundle._immediately
        if realtime:
            ntp = OscBundle._system_time_to_ntp(value)
            seconds, fraction = str(ntp).split(".")
            seconds = int(seconds)
            fraction = int(fraction)
            result = struct.pack(">I", seconds)
            result += struct.pack(">I", fraction)
        else:
            kSecondsToOSC = 4_294_967_296
            result = struct.pack(">q", int(value * kSecondsToOSC))
        return result

    ### PUBLIC METHODS ###

    @staticmethod
    def datagram_is_bundle(datagram, offset=0):
        return datagram[offset : offset + 8] == OscBundle._bundle_prefix

    @staticmethod
    def from_datagram(datagram):
        import supriya.osc

        assert OscBundle.datagram_is_bundle(datagram)
        offset = 8
        timestamp, offset = OscBundle._read_date(datagram, offset)
        contents = []
        while offset < len(datagram):
            length, offset = supriya.osc.OscMessage._read_int(datagram, offset)
            data = datagram[offset : offset + length]
            if OscBundle.datagram_is_bundle(data):
                item = OscBundle.from_datagram(data)
            else:
                item = supriya.osc.OscMessage.from_datagram(data)
            contents.append(item)
            offset += length
        osc_bundle = OscBundle(timestamp=timestamp, contents=tuple(contents))
        return osc_bundle

    def to_datagram(self, realtime=True):
        import supriya.osc

        datagram = OscBundle._bundle_prefix
        datagram += OscBundle._write_date(self._timestamp, realtime=realtime)
        for content in self.contents:
            content_datagram = content.to_datagram()
            content_length = len(content_datagram)
            datagram += supriya.osc.OscMessage._write_int(content_length)
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
