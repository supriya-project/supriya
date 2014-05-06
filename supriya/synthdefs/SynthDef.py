import collections
import struct


class SynthDef(object):

    def compile(self):
        result = []
        result.append(SynthDef.encode_string(self.name))
        result.append(SynthDef.encode_unsigned_int_16bit(len(self.constants)))
        for key, value in sorted(self.constants.items(), key=lambda x: x[1]):
            result.append(SynthDef.encode_float(key))
        result.append(SynthDef.encode_unsigned_int_16bit(len(self.parameters)))
        for value in self.parameters:
            result.append(SynthDef.encode_float(value))
        result.append(SynthDef.encode_unsigned_int_16bit(
            len(self.parameter_names)))
        for key, value in self.parameter_names.items():
            result.append(SynthDef.encode_string(key))
            result.append(SynthDef.encode_unsigned_int_16bit(value))
        result.append(SynthDef.encode_unsigned_int_16bit(len(self.ugens)))
        for key, value in sorted(self.ugens.items(), key=lambda x: x[1]):
            result.append(key.compile(self))
        return result

    @staticmethod
    def compile_synthdefs(synthdefs):
        def flatten(value):
            if isinstance(value, collections.Sequence) and \
                not isinstance(value, str):
                return ''.join(flatten(x) for x in value)
            return value
        result = []
        result.append('SCgf')
        result.append(SynthDef.encode_unsigned_int_32bit(1))
        result.append(SynthDef.encode_unsigned_int_16bit(len(synthdefs)))
        for synthdef in synthdefs:
            result.append(synthdef.compile())
        result.append(SynthDef.encode_unsigned_int_16bit(0))
        result = flatten(result)
        return result

    @staticmethod
    def encode_float(value):
        return struct.pack('>f', value)

    @staticmethod
    def encode_string(value):
        return struct.pack('>B', len(value)) + value

    @staticmethod
    def encode_unsigned_int_8bit(value):
        return struct.pack('>B', value)

    @staticmethod
    def encode_unsigned_int_16bit(value):
        return struct.pack('>H', value)

    @staticmethod
    def encode_unsigned_int_32bit(value):
        return struct.pack('>I', value)
