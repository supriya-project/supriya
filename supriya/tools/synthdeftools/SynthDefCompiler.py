# -*- encoding: utf-8 -*-
import struct
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefCompiler(SupriyaObject):

    ### PUBLIC METHODS ###

    @staticmethod
    def encode_string(value):
        result = bytes(struct.pack('>B', len(value)))
        result += bytes(bytearray(value, encoding='ascii'))
        return result

