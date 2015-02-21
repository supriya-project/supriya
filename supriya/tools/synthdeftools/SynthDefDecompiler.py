# -*- encoding: utf-8 -*-
import struct
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefDecompiler(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'SynthDef Internals'

    ### PUBLIC METHODS ###

    @staticmethod
    def decompile_synthdefs(value):
        synthdefs = []
        sdd = SynthDefDecompiler
        index = 4
        assert value[:index] == 'SCgf'
        file_version, index = sdd.decode_int_32bit(value, index)
        synthdef_count, index = sdd.decode_int_16bit(value, index)
        for _ in range(synthdef_count):
            synthdef, index = sdd.decompile_synthdef(value, index)
            synthdefs.append(synthdef)
        return synthdefs

    @staticmethod
    def decode_constants(value, index):
        sdd = SynthDefDecompiler
        constants = []
        constants_count, index = sdd.decode_int_32bit(value, index)
        for _ in range(constants_count):
            constant, index = sdd.decode_float(value, index)
            constants.append(constant)
        return constants, index

    @staticmethod
    def decode_parameters(value, index):
        sdd = SynthDefDecompiler
        parameter_names = []
        parameter_values = []
        parameter_count, index = sdd.decode_int_32bit(value, index)
        for _ in range(parameter_count):
            parameter_value, index = sdd.decode_float(value, index)
        parameter_count, index = sdd.decode_int_32bit(value, index)
        for _ in range(parameter_count):
            parameter_name, index = sdd.decode_string(value, index)
            _, index = sdd.decode_int_32bit(value, index)
            parameter_names.append(parameter_name)
        return parameter_names, parameter_values, index

    @staticmethod
    def decompile_synthdef(value, index):
        sdd = SynthDefDecompiler
        synthdef = None
        name, index = sdd.decode_string(value, index)
        constants, index = sdd.decode_constants(value, index)
        parameter_names, parameter_values, index = \
            sdd.decode_parameters(value, index)
        ugens = []
        ugen_count, index = sdd.decode_int_32bit(value, index)
        for _ in range(ugen_count):
            pass

        variants_count, index = sdd.decode_int_16bit(value, index)
        return synthdef, index

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
    def decode_int_8bit(value, index):
        result = struct.unpack('>B', value[index:index + 1])
        index += 1
        return result, index

    @staticmethod
    def decode_int_16bit(value, index):
        result = struct.unpack('>H', value[index:index + 2])
        index += 2
        return result, index

    @staticmethod
    def decode_int_32bit(value, index):
        result = struct.unpack('>I', value[index:index + 4])
        index += 4
        return result, index