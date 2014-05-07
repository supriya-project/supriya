import collections
import struct


class SynthDef(object):
    r'''A SuperCollider synth definition.

    ::

        >>> import supriya
        >>> synth = supriya.synthdefs.SynthDef('test')
        >>> synth.compile()
        '\x04test\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_constants',
        '_controls',
        '_name',
        '_parameter_names',
        '_parameters',
        '_pending_ugens',
        '_ugens',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name,
        control_definitions=None,
        ugens=None,
        ):
        from supriya import synthdefs
        self._constants = {}
        self._name = name
        self._parameter_names = {}
        self._parameters = []
        self._pending_ugens = set()
        self._ugens = {}
        control_names = []
        if control_definitions is not None:
            for name, value in control_definitions:
                self._add_parameter(name, value)
                control_names.append(name)
        self._controls = synthdefs.ControlSpecification(control_names)
        if ugens is not None:
            for ugen in ugens:
                self._add_ugen(ugen)

    ### PRIVATE METHODS ###

    def _add_constant(self, value):
        if value not in self._constants:
            self._constants[value] = len(self.constants)

    def _add_parameter(self, name, value):
        self._parameter_names[name] = len(self._parameters)
        self._parameters.append(value)

    def _add_ugen(self, ugen):
        def resolve(ugen, synthdef):
            for i in self.inputs:
                if type(i) == float:
                    synthdef._add_constant(i)
                else:
                    synthdef._add_ugen(i[0])
        if ugen in self._ugens:
            return
        elif ugen in self._pending_ugens:
            return
        self._pending_ugens.add(ugen)
        resolve(ugen, self)
        self._ugens[ugen] = \
            len(self._ugens)
        self._pending_ugens.remove(ugen)

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

    def _get_ugen_index(self, ugen):
        return self._ugens[ugen]

    ### PUBLIC METHODS ###

    def compile(self):
        result = []
        # the name of the synth definition
        result.append(SynthDef._encode_string(self.name))
        # number of constants (K)
        result.append(SynthDef._encode_unsigned_int_16bit(len(self.constants)))
        # constant values
        for key, value in sorted(
            self.constants.items(),
            key=lambda key, value: value,
            ):
            result.append(SynthDef._encode_float(key))
        # number of parameters (P)
        result.append(SynthDef._encode_unsigned_int_16bit(len(self.parameters)))
        # initial parameter values
        for value in self.parameters:
            result.append(SynthDef._encode_float(value))
        # number of parameter names (N)
        result.append(SynthDef._encode_unsigned_int_16bit(
            len(self.parameter_names)))
        # the name of the parameter and its index in the parameter array
        for key, value in self.parameter_names.items():
            result.append(SynthDef._encode_string(key))
            result.append(SynthDef._encode_unsigned_int_16bit(value))
        # number of unit generators (U)
        result.append(SynthDef._encode_unsigned_int_16bit(len(self.ugens)))
        # compiled ugens
        for ugen, ugen_index in sorted(
            self.ugens.items(),
            key=lambda ugen, ugen_index: ugen_index):
            result.append(ugen.compile(self))
        # number of variants (V)
        result.append(SynthDef._encode_unsigned_int_16bit(0))
        result = ''.join(result)
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
        result = flatten(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def constants(self):
        return self._constants

    @property
    def name(self):
        return self._name

    @property
    def parameter_names(self):
        return self._parameter_names

    @property
    def parameters(self):
        return self._parameters

    @property
    def ugens(self):
        return self._ugens
