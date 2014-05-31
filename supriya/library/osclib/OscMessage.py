# -*- encoding: utf-8 -*-
import collections
import struct
import sys


class OscMessage(object):
    r'''An OSC message.

    ::

        >>> from supriya.library import osclib
        >>> osc_message = osclib.OscMessage('/g_new', 0, 0)
        >>> osc_message
        OscMessage('/g_new', 0, 0)

    ::

        >>> datagram = osc_message.to_datagram()
        >>> osclib.OscMessage.from_datagram(datagram)
        OscMessage('/g_new', 0, 0)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_address',
        '_contents',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        address,
        *contents
        ):
        def recurse(sequence):
            sequence = list(sequence)
            for i, x in enumerate(sequence):
                if isinstance(x, list):
                    sequence[i] = tuple(recurse(sequence[i]))
            return tuple(sequence)
        assert isinstance(address, (str, int))
        self._address = address
        self._contents = recurse(contents)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(expr) != type(self):
            return False
        if expr.address != self.address:
            return False
        if expr.contents != self.contents:
            return False
        return True

    def __hash__(self):
        hash_values = (
            type(self),
            self.address,
            self.contents,
            )
        return hash(hash_values)

    def __repr__(self):
        items = (self.address,) + self.contents
        items = ', '.join(repr(x) for x in items)
        result = '{}({})'.format(
            type(self).__name__,
            items,
            )
        return result

    ### PRIVATE METHODS ###

    @staticmethod
    def _decode_array(type_tags, type_tag_offset, payload, payload_offset):
        assert type_tags[type_tag_offset] == '['
        array = []
        type_tag_offset += 1
        while type_tags[type_tag_offset] != ']':
            result, type_tag_offset, payload_offset = \
                OscMessage._decode_value(
                    type_tags,
                    type_tag_offset,
                    payload,
                    payload_offset,
                    )
            array.append(result)
        assert type_tags[type_tag_offset] == ']'
        array = tuple(array)
        type_tag_offset += 1
        return array, type_tag_offset, payload_offset

    @staticmethod
    def _decode_blob(type_tags, type_tag_offset, payload, payload_offset):
        assert type_tags[type_tag_offset] == 'b'
        length = payload[payload_offset:payload_offset + 4]
        length = struct.unpack('>i', length)
        length = length[0]
        payload_offset += 4
        total_length = length + (-length % 4)
        result = payload[payload_offset:payload_offset + length]
        type_tag_offset += 1
        payload_offset += total_length
        return result, type_tag_offset, payload_offset

    @staticmethod
    def _decode_boolean(type_tags, type_tag_offset, payload, payload_offset):
        type_tag = type_tags[type_tag_offset]
        assert type_tag in ('T', 'F')
        if type_tag == 'T':
            result = True
        elif type_tag == 'F':
            result = False
        type_tag_offset += 1
        return result, type_tag_offset, payload_offset

    @staticmethod
    def _decode_float(type_tags, type_tag_offset, payload, payload_offset):
        assert type_tags[type_tag_offset] == 'f'
        result, payload_offset = OscMessage._read_float(
            payload,
            payload_offset,
            )
        type_tag_offset += 1
        return result, type_tag_offset, payload_offset

    @staticmethod
    def _decode_int(type_tags, type_tag_offset, payload, payload_offset):
        assert type_tags[type_tag_offset] == 'i'
        result, payload_offset = OscMessage._read_int(
            payload,
            payload_offset,
            )
        type_tag_offset += 1
        return result, type_tag_offset, payload_offset

    @staticmethod
    def _decode_none(type_tags, type_tag_offset, payload, payload_offset):
        assert type_tags[type_tag_offset] == 'N'
        result = None
        type_tag_offset += 1
        return result, type_tag_offset, payload_offset

    @staticmethod
    def _decode_string(type_tags, type_tag_offset, payload, payload_offset):
        assert type_tags[type_tag_offset] == 's'
        result, payload_offset = OscMessage._read_string(
            payload,
            payload_offset,
            )
        type_tag_offset += 1
        return result, type_tag_offset, payload_offset

    @staticmethod
    def _decode_value(type_tags, type_tag_offset, payload, payload_offset):
        type_tag = type_tags[type_tag_offset]
        type_tag_mapping = {
            'N': OscMessage._decode_none,
            'T': OscMessage._decode_boolean,
            'F': OscMessage._decode_boolean,
            'i': OscMessage._decode_int,
            'f': OscMessage._decode_float,
            's': OscMessage._decode_string,
            'b': OscMessage._decode_blob,
            '[': OscMessage._decode_array,
            }
        procedure = type_tag_mapping[type_tag]
        result, type_tag_offset, payload_offset = \
            procedure(type_tags, type_tag_offset, payload, payload_offset)
        return result, type_tag_offset, payload_offset

    @staticmethod
    def _encode_array(array):
        assert isinstance(array, collections.Sequence)
        type_tags = '['
        encoded_value = b''
        for value in array:
            sub_type_tags, sub_encoded_value = OscMessage._encode_value(value)
            type_tags += sub_type_tags
            encoded_value += sub_encoded_value
        type_tags += ']'
        return type_tags, encoded_value

    @staticmethod
    def _encode_blob(value):
        assert isinstance(value, (bytearray, bytes))
        type_tags = 'b'
        encoded_value = OscMessage._write_int(len(value))
        encoded_value += value
        difference = 4 - (len(encoded_value) % 4)
        padding = b'\x00' * difference
        encoded_value += padding
        return type_tags, encoded_value

    @staticmethod
    def _encode_boolean(value):
        assert value in (True, False)
        if value:
            type_tags = 'T'
        else:
            type_tags = 'F'
        encoded_value = None
        return type_tags, encoded_value

    @staticmethod
    def _encode_float(value):
        assert isinstance(value, float)
        type_tags = 'f'
        encoded_value = OscMessage._write_float(value)
        return type_tags, encoded_value

    @staticmethod
    def _encode_int(value):
        assert isinstance(value, int)
        type_tags = 'i'
        encoded_value = OscMessage._write_int(value)
        return type_tags, encoded_value

    @staticmethod
    def _encode_none():
        type_tags = 'N'
        encoded_value = None
        return type_tags, encoded_value

    @staticmethod
    def _encode_string(value):
        assert isinstance(value, str)
        type_tags = 's'
        encoded_value = value.encode('utf-8')
        padding_length = 4 - (len(encoded_value) % 4)
        padding = b'\x00' * padding_length
        encoded_value += padding
        return type_tags, encoded_value

    @staticmethod
    def _encode_value(value):
        if isinstance(value, bytearray):
            type_tags, encoded_value = OscMessage._encode_blob(value)
        elif isinstance(value, str):
            type_tags, encoded_value = OscMessage._encode_string(value)
        elif isinstance(value, bool):
            type_tags, encoded_value = OscMessage._encode_boolean(value)
        elif isinstance(value, float):
            type_tags, encoded_value = OscMessage._encode_float(value)
        elif isinstance(value, int):
            type_tags, encoded_value = OscMessage._encode_int(value)
        elif value is None:
            type_tags, encoded_value = OscMessage._encode_none()
        elif isinstance(value, collections.Sequence):
            type_tags, encoded_value = OscMessage._encode_array(value)
        else:
            raise TypeError
        return type_tags, encoded_value

    @staticmethod
    def _read_float(payload, payload_offset):
        result = payload[payload_offset:payload_offset + 4]
        result = struct.unpack('>f', result)
        result = result[0]
        payload_offset += 4
        return result, payload_offset

    @staticmethod
    def _read_int(payload, payload_offset):
        result = payload[payload_offset:payload_offset + 4]
        result = struct.unpack('>i', result)
        result = result[0]
        payload_offset += 4
        return result, payload_offset

    @staticmethod
    def _read_string(payload, payload_offset):
        offset = 0
        while payload[payload_offset + offset] != 0:
            offset += 1
        if (offset % 4) == 0:
            offset += 4
        else:
            offset += -offset % 4
        result = payload[payload_offset:payload_offset + offset]
        result = result.replace(b'\x00', b'')
        result = result.decode('utf-8')
        if sys.version_info[0] == 2:
            if all(ord(x) < 256 for x in result):
                result = str(result)
        payload_offset += offset
        return result, payload_offset

    @staticmethod
    def _write_float(value):
        return struct.pack('>f', value)

    @staticmethod
    def _write_int(value):
        return struct.pack('>i', value)

    ### PUBLIC METHODS ###

    def to_datagram(self):
        # address can be a string or (in SuperCollider) an int
        datagram = OscMessage._encode_value(self.address)[1]
        if self.contents is None:
            return datagram
        encoded_type_tags = ','
        encoded_contents = b''
        for argument in self.contents:
            type_tags, encoded_value = OscMessage._encode_value(argument)
            encoded_type_tags += type_tags
            if encoded_value is not None:
                encoded_contents += encoded_value
        encoded_type_tags = OscMessage._encode_string(encoded_type_tags)[1]
        datagram += encoded_type_tags
        datagram += encoded_contents
        datagram = bytes(datagram)
        return datagram

    @staticmethod
    def from_datagram(datagram):
        datagram = bytearray(datagram)
        contents = []
        offset = 0
        address, offset = OscMessage._read_string(datagram, offset)
        type_tags, offset = OscMessage._read_string(datagram, offset)
        assert type_tags[0] == ','
        payload = datagram[offset:]
        payload_offset = 0
        type_tag_offset = 1
        while type_tag_offset < len(type_tags):
            result, type_tag_offset, payload_offset = \
                OscMessage._decode_value(
                    type_tags,
                    type_tag_offset,
                    payload,
                    payload_offset
                    )
            contents.append(result)
        osc_message = OscMessage(address, *contents)
        return osc_message

    ### PUBLIC PROPERTIES ###

    @property
    def address(self):
        return self._address

    @property
    def contents(self):
        return self._contents
