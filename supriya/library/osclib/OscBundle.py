# -*- encoding: utf-8 -*-
import datetime
import decimal
import struct
import time


class OscBundle(object):
    r'''An OSC bundle.

    ::

        >>> from supriya.library import osclib
        >>> message_one = osclib.OscMessage('/one', 1)
        >>> message_two = osclib.OscMessage('/two', 2)
        >>> message_three = osclib.OscMessage('/three', 3)

    ::

        >>> inner_bundle = osclib.OscBundle(
        ...     timestamp=100.,
        ...     contents=(message_one, message_two),
        ...     )
        >>> inner_bundle
        <OscBundle 100.0 {2}>

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
        '_timestamp',
        '_contents',
        )

    _bundle_prefix = b'#bundle\x00'
    _immediately = struct.pack('>q', 1)

    ### INITIALIZER ###

    def __init__(
        self,
        timestamp=None,
        contents=None,
        ):
        from supriya.library import osclib
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
        system_epoch = datetime.date(*time.gmtime(0)[0:3])
        ntp_epoch = datetime.date(1900, 1, 1)
        ntp_delta = (system_epoch - ntp_epoch).days * 24 * 3600
        return ntp_delta

    @staticmethod
    def _ntp_to_system_time(date):
        return date - OscBundle._get_ntp_delta()

    @staticmethod
    def _read_date(payload, offset):
        from supriya.library import osclib
        if payload[offset:offset + 8] == OscBundle._immediately:
            date = None
            offset += 8
        else:
            seconds, offset = osclib.OscMessage._read_int(payload, offset)
            fraction, offset = osclib.OscMessage._read_int(payload, offset)
            date = decimal.Decimal('{!s}.{!s}'.format(seconds, fraction))
            date = float(date)
            date = OscBundle._ntp_to_system_time(date)
        return date, offset

    @staticmethod
    def _system_time_to_ntp(date):
        ntp = date + OscBundle._get_ntp_delta()
        seconds, fraction = str(ntp).split('.')
        result = struct.pack('>I', int(seconds))
        result += struct.pack('>I', int(fraction))
        return result

    @staticmethod
    def _write_date(value):
        if value is None:
            return OscBundle._immediately
        return OscBundle._system_time_to_ntp(value)

    ### PUBLIC METHODS ###

    @staticmethod
    def datagram_is_bundle(datagram, offset=0):
        return datagram[offset:offset + 8] == OscBundle._bundle_prefix

    @staticmethod
    def from_datagram(datagram):
        from supriya.library import osclib
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
        from supriya.library import osclib
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
