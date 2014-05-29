# -*- encoding: utf-8 -*-

import collections
import struct


class OscMessage(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_address',
        '_arguments',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        address=None,
        *arguments
        ):
        self._address = address
        self._arguments = arguments

    ### PRIVATE METHODS ###

    @staticmethod
    def _encode_array(array):
        assert isinstance(array, collections.Sequence)
        type_tags = b'['
        encoded_value = b''
        for value in array:
            sub_type_tags, sub_encoded_value = OscMessage._encode_value(value)
            type_tags += sub_type_tags
            encoded_value += sub_encoded_value
        type_tags += b']'
        return type_tags, encoded_value

    @staticmethod
    def _encode_blob(value):
        assert isinstance(value, (bytearray, bytes))
        type_tags = b'b'
        encoded_value = OscMessage._encode_int(len(value))
        encoded_value += value
        difference = 4 - (len(encoded_value) % 4)
        padding = b'\x00' * difference
        encoded_value += padding
        return type_tags, encoded_value

    @staticmethod
    def _encode_boolean(value):
        assert value in (True, False)
        if value:
            type_tags = b'T'
        else:
            type_tags = b'F'
        encoded_value = None
        return type_tags, encoded_value

    @staticmethod
    def _encode_float(value):
        assert isinstance(value, float)
        type_tags = b'f'
        encoded_value = struct.pack('>f', value)
        return type_tags, encoded_value

    @staticmethod
    def _encode_int(value):
        assert isinstance(value, int)
        type_tags = b'i'
        encoded_value = struct.pack('>i', value)
        return type_tags, encoded_value

    @staticmethod
    def _encode_none():
        type_tags = b'N'
        encoded_value = None
        return type_tags, encoded_value

    @staticmethod
    def _encode_string(value):
        assert isinstance(value, str)
        type_tags = b's'
        encoded_value = value.encode('utf-8')
        difference = 4 - (len(encoded_value) % 4)
        padding = b'\x00' * difference
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

    ### PUBLIC METHODS ###

    def to_datagram(
        self,
        ):
        datagram = OscMessage._encode_string(self.address)[1]
        if self.arguments is None:
            return datagram
        encoded_type_tags = b''
        encoded_arguments = b''
        for argument in self.arguments:
            type_tags, encoded_value = OscMessage._encode_value(argument)
            encoded_type_tags += type_tags
            if encoded_value is not None:
                encoded_arguments += encoded_value
        print datagram, encoded_type_tags, encoded_arguments
        datagram += encoded_type_tags
        datagram += encoded_arguments
        return datagram

    @staticmethod
    def from_datagram(
        datagram,
        ):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def address(self):
        return self._address

    @property
    def arguments(self):
        return self._arguments
