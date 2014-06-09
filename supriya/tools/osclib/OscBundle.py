# -*- encoding: utf-8 -*-
import datetime
import decimal
import struct


class OscBundle(object):
    r'''An OSC bundle.

    ::

        >>> from supriya.tools import osclib
        >>> message_one = osclib.OscMessage('/one', 1)
        >>> message_two = osclib.OscMessage('/two', 2)
        >>> message_three = osclib.OscMessage('/three', 3)

    ::

        >>> inner_bundle = osclib.OscBundle(
        ...     timestamp=1401557034.5,
        ...     contents=(message_one, message_two),
        ...     )
        >>> inner_bundle
        <OscBundle 1401557034.5 {2}>

    ::

        >>> outer_bundle = osclib.OscBundle(
        ...     contents=(inner_bundle, message_three),
        ...     )
        >>> outer_bundle
        <OscBundle None {2}>

    ::

        >>> datagram = outer_bundle.to_datagram()

    ::

        >>> decoded_bundle = osclib.OscBundle.from_datagram(datagram)
        >>> decoded_bundle
        <OscBundle None {2}>

    ::

        >>> decoded_bundle == outer_bundle
        True

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contents',
        '_timestamp',
        )

    _bundle_prefix = b'#bundle\x00'
    _immediately = struct.pack('>q', 1)

    ### INITIALIZER ###

    def __init__(
        self,
        timestamp=None,
        contents=None,
        ):
        from supriya.tools import osclib
        self._timestamp = timestamp
        if contents is not None:
            prototype = (osclib.OscMessage, osclib.OscBundle)
            assert all(isinstance(x, prototype) for x in contents)
            contents = tuple(contents)
        else:
            contents = ()
        self._contents = contents

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(expr) != type(self):
            return False
        if expr.timestamp != self.timestamp:
            return False
        if expr.contents != self.contents:
            return False
        return True

    def __hash__(self):
        hash_values = (
            type(self),
            self.timestamp,
            self.contents,
            )
        return hash(hash_values)

    def __repr__(self):
        return '<{} {} {{{}}}>'.format(
            type(self).__name__,
            self.timestamp,
            len(self.contents),
            )

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
        if payload[offset:offset + 8] == OscBundle._immediately:
            date = None
        else:
            seconds, fraction = struct.unpack(
                '>II',
                payload[offset:offset + 8],
                )
            date = decimal.Decimal('{!s}.{!s}'.format(seconds, fraction))
            date = float(date)
            date = OscBundle._ntp_to_system_time(date)
        offset += 8
        return date, offset

    @staticmethod
    def _system_time_to_ntp(date):
        return float(date) + OscBundle._get_ntp_delta()

    @staticmethod
    def _write_date(value):
        if value is None:
            return OscBundle._immediately
        ntp = OscBundle._system_time_to_ntp(value)
        seconds, fraction = str(ntp).split('.')
        seconds = int(seconds)
        fraction = int(fraction)
        result = struct.pack('>I', seconds)
        result += struct.pack('>I', fraction)
        return result

    ### PUBLIC METHODS ###

    @staticmethod
    def datagram_is_bundle(datagram, offset=0):
        return datagram[offset:offset + 8] == OscBundle._bundle_prefix

    @staticmethod
    def from_datagram(datagram):
        from supriya.tools import osclib
        assert OscBundle.datagram_is_bundle(datagram)
        offset = 8
        timestamp, offset = OscBundle._read_date(datagram, offset)
        contents = []
        while offset < len(datagram):
            length, offset = osclib.OscMessage._read_int(datagram, offset)
            data = datagram[offset:offset + length]
            if OscBundle.datagram_is_bundle(data):
                item = OscBundle.from_datagram(data)
            else:
                item = osclib.OscMessage.from_datagram(data)
            contents.append(item)
            offset += length
        osc_bundle = OscBundle(
            timestamp=timestamp,
            contents=tuple(contents),
            )
        return osc_bundle

    def to_datagram(self):
        from supriya.tools import osclib
        datagram = OscBundle._bundle_prefix
        datagram += OscBundle._write_date(self._timestamp)
        for content in self.contents:
            content_datagram = content.to_datagram()
            content_length = len(content_datagram)
            datagram += osclib.OscMessage._write_int(content_length)
            datagram += content_datagram
        return datagram

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        return self._contents

    @property
    def timestamp(self):
        return self._timestamp
