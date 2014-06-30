# -*- encoding: utf-8 -*-
import struct
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefCompiler(SupriyaObject):

    ### PUBLIC METHODS ###

    @staticmethod
    def compile_ugen_graph(synthdef):
        result = []
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(synthdef.constants)))
        for key, value in sorted(
            synthdef.constants.items(),
            key=lambda item: item[1],
            ):
            result.append(SynthDefCompiler.encode_float(key))
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(synthdef.parameters)))
        for value in synthdef.parameters:
            result.append(SynthDefCompiler.encode_float(value))
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(
            len(synthdef.parameter_names)))
        for key, value in sorted(
            synthdef.parameter_names.items(),
            key=lambda x: x[1],
            ):
            result.append(SynthDefCompiler.encode_string(key))
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(value))
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(synthdef.ugens)))
        for ugen_index, ugen in enumerate(synthdef.ugens):
            result.append(ugen.compile(synthdef))
        result.append(SynthDefCompiler.encode_unsigned_int_16bit(0))
        result = bytes().join(result)
        return result

    @staticmethod
    def encode_string(value):
        result = bytes(struct.pack('>B', len(value)))
        result += bytes(bytearray(value, encoding='ascii'))
        return result

    @staticmethod
    def encode_float(value):
        return bytes(struct.pack('>f', value))

    @staticmethod
    def encode_unsigned_int_8bit(value):
        return bytes(struct.pack('>B', value))

    @staticmethod
    def encode_unsigned_int_16bit(value):
        return bytes(struct.pack('>H', value))

    @staticmethod
    def encode_unsigned_int_32bit(value):
        return bytes(struct.pack('>I', value))

