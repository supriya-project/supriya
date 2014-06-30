# -*- encoding: utf-8 -*-
import collections
import struct
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthDefCompiler(SupriyaObject):

    ### PUBLIC METHODS ###

    @staticmethod
    def compile_synthdef(synthdef, name):
        result = SynthDefCompiler.encode_string(name)
        result += synthdef._compiled_ugen_graph
        return result

    @staticmethod
    def compile_synthdefs(synthdefs):
        def flatten(value):
            if isinstance(value, collections.Sequence) and \
                not isinstance(value, (bytes, bytearray)):
                return bytes().join(flatten(x) for x in value)
            return value
        result = []
        encoded_file_type_id = b'SCgf'
        result.append(encoded_file_type_id)
        encoded_file_version = SynthDefCompiler.encode_unsigned_int_32bit(2)
        result.append(encoded_file_version)
        encoded_synthdef_count = SynthDefCompiler.encode_unsigned_int_16bit(
            len(synthdefs))
        result.append(encoded_synthdef_count)
        for synthdef in synthdefs:
            name = synthdef.name
            if not name:
                name = synthdef.anonymous_name
            result.append(SynthDefCompiler.compile_synthdef(
                synthdef, name))
        result = flatten(result)
        result = bytes(result)
        return result

    @staticmethod
    def compile_ugen(ugen, synthdef):
        from supriya.tools.synthdeftools import SynthDefCompiler
        outputs = ugen._get_outputs()
        result = []
        result.append(SynthDefCompiler.encode_string(type(ugen).__name__))
        result.append(SynthDefCompiler.encode_unsigned_int_8bit(ugen.rate))
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(ugen.inputs)))
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(outputs)))
        result.append(SynthDefCompiler.encode_unsigned_int_16bit(int(ugen.special_index)))
        for input_ in ugen.inputs:
            result.append(SynthDefCompiler.compile_ugen_input_spec(input_, synthdef))
        for output in outputs:
            result.append(SynthDefCompiler.encode_unsigned_int_8bit(output))
        result = bytes().join(result)
        return result

    @staticmethod
    def compile_ugen_graph(synthdef):
        result = []
        result.append(SynthDefCompiler.encode_unsigned_int_32bit(len(synthdef.constants)))
        for constant in synthdef.constants:
            result.append(SynthDefCompiler.encode_float(constant))
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
            result.append(SynthDefCompiler.compile_ugen(ugen, synthdef))
        result.append(SynthDefCompiler.encode_unsigned_int_16bit(0))
        result = bytes().join(result)
        return result

    @staticmethod
    def compile_ugen_input_spec(input_, synthdef):
        from supriya.tools import synthdeftools
        result = []
        if isinstance(input_, float):
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(0xffffffff))
            constant_index = synthdef._constants.index(input_)
            result.append(SynthDefCompiler.encode_unsigned_int_32bit(
                constant_index))
        elif isinstance(input_, synthdeftools.OutputProxy):
            ugen = input_.source
            output_index = input_.output_index
            ugen_index = synthdef._ugens.index(ugen)
            result.append(synthdeftools.SynthDefCompiler.encode_unsigned_int_32bit(ugen_index))
            result.append(synthdeftools.SynthDefCompiler.encode_unsigned_int_32bit(output_index))
        else:
            raise Exception('Unhandled input spec: {}'.format(input_))
        return bytes().join(result)

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
