# -*- encoding: utf-8 -*-
import struct
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefDecompiler(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    ### PUBLIC METHODS ###

    @staticmethod
    def decompile_synthdefs(synthdefs):
        pass

    @staticmethod
    def decompile_synthdef(value, index):
        pass

    @staticmethod
    def decode_string(value, index):
        length = struct.unpack('>B', value[index:index + 1])
        index += 1
        result = str(value[index:index + length])
        index += length
        return result

    @staticmethod
    def decode_float(value, index):
        result = struct.unpack('>f', value[index:index + 4])
        index += 4
        return result, index

    @staticmethod
    def decode_unsigned_int_8bit(value, index):
        result = struct.unpack('>B', value[index:index + 1])
        index += 1
        return result, index

    @staticmethod
    def decode_unsigned_int_16bit(value, index):
        result = struct.unpack('>H', value[index:index + 2])
        index += 2
        return result, index

    @staticmethod
    def decode_unsigned_int_32bit(value, index):
        result = struct.unpack('>I', value[index:index + 4])
        index += 4
        return result, index