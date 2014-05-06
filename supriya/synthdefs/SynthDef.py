import collections
import struct


class SynthDef(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_constants',
        '_controls',
        '_name',
        '_parameter_names',
        '_parameters',
        '_pending_ugen_specifications',
        '_ugen_specifications',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name,
        control_definitions=None,
        ugen_specifications=None,
        ):
        from supriya import synthdefs
        self._constants = {}
        self._name = name
        self._parameter_names = {}
        self._parameters = []
        self._pending_ugen_specifications = set()
        self._ugen_specifications = {}
        control_names = []
        if control_definitions is not None:
            for name, value in control_definitions:
                self._add_parameter(name, value)
                control_names.append(name)
        self._controls = synthdefs.ControlSpecification(control_names)
        if ugen_specifications is not None:
            for ugen_specification in ugen_specifications:
                self._add_ugen_specification(ugen_specification)

    ### PRIVATE METHODS ###

    def _add_constant(self, value):
        if value not in self._constants:
            self._constants[value] = len(self.constants)

    def _add_parameter(self, name, value):
        self._parameter_names[name] = len(self._parameters)
        self._parameters.append(value)

    def _add_ugen_specification(self, ugen_specification):
        if ugen_specification in self._ugen_specifications:
            return
        elif ugen_specification in self._pending_ugen_specifications:
            return
        self._pending_ugen_specifications.add(ugen_specification)
        ugen_specification._resolve(self)
        self._ugen_specifications[ugen_specification] = len(self._ugen_specifications)
        self._pending_ugen_specifications.remove(ugen_specification)

    @staticmethod
    def _encode_float(value):
        return struct.pack('>f', value)

    @staticmethod
    def _encode_string(value):
        return struct.pack('>B', len(value)) + value

    @staticmethod
    def _encode_unsigned_int_8bit(value):
        return struct.pack('>B', value)

    @staticmethod
    def _encode_unsigned_int_16bit(value):
        return struct.pack('>H', value)

    @staticmethod
    def _encode_unsigned_int_32bit(value):
        return struct.pack('>I', value)

    def _get_constant_index(self, value):
        return self._constants[value]

    def _get_ugen_specification_index(self, ugen_specification):
        return self._ugen_specifications[ugen_specification]

    ### PUBLIC METHODS ###

    def compile(self):
        result = []
        result.append(SynthDef._encode_string(self.name))
        result.append(SynthDef._encode_unsigned_int_16bit(len(self.constants)))
        for key, value in sorted(self.constants.items(), key=lambda x: x[1]):
            result.append(SynthDef._encode_float(key))
        result.append(SynthDef._encode_unsigned_int_16bit(len(self.parameters)))
        for value in self.parameters:
            result.append(SynthDef._encode_float(value))
        result.append(SynthDef._encode_unsigned_int_16bit(
            len(self.parameter_names)))
        for key, value in self.parameter_names.items():
            result.append(SynthDef._encode_string(key))
            result.append(SynthDef._encode_unsigned_int_16bit(value))
        result.append(SynthDef._encode_unsigned_int_16bit(len(self.ugens)))
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
        result.append(SynthDef._encode_unsigned_int_32bit(1))
        result.append(SynthDef._encode_unsigned_int_16bit(len(synthdefs)))
        for synthdef in synthdefs:
            result.append(synthdef.compile())
        result.append(SynthDef._encode_unsigned_int_16bit(0))
        result = flatten(result)
        return result

