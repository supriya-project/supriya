import collections
import struct


class SynthDef(object):
    r'''A SuperCollider synth definition.

    ::

        >>> from supriya import synthdefs
        >>> synth = synthdefs.SynthDef('test')
        >>> synth.compile()
        '\x04test\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

    ::

        >>> synth = synthdefs.SynthDef(
        ...     'test',
        ...     freq_l=1200,
        ...     freq_r=1205,
        ...     )
        >>> controls = synth.controls
        >>> line = synthdefs.Line.kr(
        ...     start=100,
        ...     end=[controls['freq_l'], controls['freq_r']],
        ...     )
        >>> sin_osc = synthdefs.SinOsc.ar(freq=line, phase=0) * 0.2
        >>> out = synthdefs.Out.ar(bus=0, source=sin_osc)
        >>> synth.add_ugen(out)
        >>> synth.compile()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_available_ugens',
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
        **kwargs
        ):
        from supriya import synthdefs
        self._available_ugens = []
        self._constants = {}
        self._name = name
        self._parameter_names = {}
        self._parameters = []
        self._pending_ugens = set()
        self._ugens = []
        control_names = []
        for name, value in kwargs.items():
            self._add_parameter(name, value)
            control_names.append(name)
        self._controls = synthdefs.ControlSpecification(control_names)

    ### PRIVATE METHODS ###

    def _add_constant(self, value):
        if value not in self._constants:
            self._constants[value] = len(self.constants)

    def _add_parameter(self, name, value):
        self._parameter_names[name] = len(self._parameters)
        self._parameters.append(value)

    def _add_ugen(self, ugen):
        def resolve(ugen, synthdef):
            from supriya import synthdefs
            for x in ugen.inputs:
                #if isinstance(x, float):
                #    synthdef._add_constant(x)
                if isinstance(x, synthdefs.OutputProxy):
                    synthdef._add_ugen(x.source)
                #else:
                #    raise Exception('Unhandled input spec: {}'.format(x))
        if isinstance(ugen, collections.Sequence):
            for x in ugen:
                self._add_ugen(x)
        else:
            if ugen in self._ugens:
                return
            elif ugen in self._pending_ugens:
                return
            self._pending_ugens.add(ugen)
            resolve(ugen, self)
            self._ugens.append(ugen)
            ugen.synthdef = self
            self._pending_ugens.remove(ugen)

    def _cleanup_topological_sort(self):
        for ugen in self._ugens:
            ugen._antecedents = None
            ugen._descendants = None
            ugen._width_first_antecedents = None

    def _collect_constants(self):
        self._constants = {}
        for ugen in self._ugens:
            ugen._collect_constants()

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
        return self._ugens.index(ugen)

    def _initialize_topological_sort(self):
        self._available_ugens = []
        for ugen in self.ugens:
            ugen._antecedents = []
            ugen._descendants = []
            ugen._width_first_antecedents = []
        for ugen in self.ugens:
            ugen._initialize_topological_sort()
            ugen._descendants = sorted(
                ugen._descendants,
                key=lambda x: x.synthdef.ugens.index(ugen),
                )
        for ugen in reversed(self.ugens):
            ugen._make_available()

    def _sort_ugens_topologically(self):
        out_stack = []
        self._initialize_topological_sort()
        while self._available_ugens:
            available_ugen = self._available_ugens.pop()
            available_ugen._schedule(out_stack)
        self._ugens = out_stack
        self._cleanup_topological_sort()

    ### PUBLIC METHODS ###

    def add_ugen(self, ugen):
        self._add_ugen(ugen)
        self._sort_ugens_topologically()
        self._collect_constants()

    def compile(self):
        result = []
        # the name of the synth definition
        result.append(SynthDef._encode_string(self.name))

        # number of constants (K)
        result.append(SynthDef._encode_unsigned_int_32bit(len(self.constants)))

        # constant values
        for key, value in sorted(
            self.constants.items(),
            key=lambda item: item[1],
            ):
            result.append(SynthDef._encode_float(key))

        # number of parameters (P)
        result.append(SynthDef._encode_unsigned_int_32bit(len(self.parameters)))

        # initial parameter values
        for value in self.parameters:
            result.append(SynthDef._encode_float(value))

        # number of parameter names (N)
        result.append(SynthDef._encode_unsigned_int_32bit(
            len(self.parameter_names)))

        # the name of the parameter and its index in the parameter array
        for key, value in self.parameter_names.items():
            result.append(SynthDef._encode_string(key))
            result.append(SynthDef._encode_unsigned_int_32bit(value))

        # number of unit generators (U)
        result.append(SynthDef._encode_unsigned_int_32bit(len(self.ugens)))

        # compiled ugens
        for ugen_index, ugen in enumerate(self.ugens):
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
        encoded_file_type_id = 'SCgf'
        result.append(encoded_file_type_id)
        encoded_file_version = SynthDef._encode_unsigned_int_32bit(2)
        result.append(encoded_file_version)
        encoded_synthdef_count = SynthDef._encode_unsigned_int_16bit(len(synthdefs))
        result.append(encoded_synthdef_count)
        for synthdef in synthdefs:
            result.append(synthdef.compile())
        result = flatten(result)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def controls(self):
        return self._controls

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
