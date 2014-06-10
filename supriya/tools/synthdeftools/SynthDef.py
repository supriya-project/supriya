# -*- encoding: utf-8 -*-
import collections
import struct
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class SynthDefinition(ServerObjectProxy):
    r'''A SuperCollider synth definition.

    ::

        >>> from supriya import synthdeftools
        >>> synth = synthdeftools.SynthDefinition(
        ...     'test',
        ...     freq_l=1200,
        ...     freq_r=1205,
        ...     )
        >>> controls = synth.controls
        >>> line = synthdeftools.Line.kr(
        ...     start=100,
        ...     stop=(
        ...         controls['freq_l'],
        ...         controls['freq_r'],
        ...         ),
        ...     )
        >>> sin_osc = synthdeftools.SinOsc.ar(
        ...     frequency=line,
        ...     phase=0,
        ...     )
        >>> sin_osc = sin_osc * 0.2
        >>> out = synthdeftools.Out.ar(
        ...     bus=0,
        ...     source=sin_osc,
        ...     )
        >>> synth.add_ugen(out)
        >>> compiled = synth.compile()

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
        from supriya import synthdeftools
        self._available_ugens = []
        self._constants = {}
        self._name = name
        self._parameter_names = {}
        self._parameters = []
        self._pending_ugens = set()
        self._ugens = []
        control_names = []
        for name, value in sorted(kwargs.items()):
            self._add_parameter(name, value)
            control_names.append(name)
        self._controls = synthdeftools.Control(control_names)
        if control_names:
            self._add_ugen(self._controls)

    ### PRIVATE METHODS ###

    def _add_constant(self, value):
        if value not in self._constants:
            self._constants[value] = len(self.constants)

    def _add_parameter(self, name, value):
        self._parameter_names[name] = len(self._parameters)
        self._parameters.append(value)

    def _add_ugen(self, ugen):
        def resolve(ugen, synthdef):
            from supriya import synthdeftools
            for x in ugen.inputs:
                if isinstance(x, synthdeftools.OutputProxy):
                    synthdef._add_ugen(x.source)
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

    def _compile(self):
        result = []
        result.append(SynthDefinition._encode_string(self.name))
        result.append(SynthDefinition._encode_unsigned_int_32bit(len(self.constants)))
        for key, value in sorted(
            self.constants.items(),
            key=lambda item: item[1],
            ):
            result.append(SynthDefinition._encode_float(key))
        result.append(SynthDefinition._encode_unsigned_int_32bit(len(self.parameters)))
        for value in self.parameters:
            result.append(SynthDefinition._encode_float(value))
        result.append(SynthDefinition._encode_unsigned_int_32bit(
            len(self.parameter_names)))
        for key, value in sorted(
            self.parameter_names.items(),
            key=lambda x: x[1],
            ):
            result.append(SynthDefinition._encode_string(key))
            result.append(SynthDefinition._encode_unsigned_int_32bit(value))
        result.append(SynthDefinition._encode_unsigned_int_32bit(len(self.ugens)))
        for ugen_index, ugen in enumerate(self.ugens):
            result.append(ugen.compile(self))
        result.append(SynthDefinition._encode_unsigned_int_16bit(0))
        result = bytearray().join(result)
        return result

    @staticmethod
    def _encode_float(value):
        return bytearray(struct.pack('>f', value))

    @staticmethod
    def _encode_string(value):
        result = struct.pack('>B', len(value))
        result += bytearray(value, encoding='ascii')
        return result

    @staticmethod
    def _encode_unsigned_int_8bit(value):
        return bytearray(struct.pack('>B', value))

    @staticmethod
    def _encode_unsigned_int_16bit(value):
        return bytearray(struct.pack('>H', value))

    @staticmethod
    def _encode_unsigned_int_32bit(value):
        return bytearray(struct.pack('>I', value))

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

    def allocate(self, session=None):
        from supriya.tools import servertools
        ServerObjectProxy.allocate(self, session=session)
        compiled = self.compile()
        message = ('d_recv', compiled, 0)
        server = servertools.Server()
        server.send_message(message)

    def add_ugen(self, ugen):
        self._add_ugen(ugen)
        self._sort_ugens_topologically()
        self._collect_constants()

    def compile(self, synthdefs=None):
        def flatten(value):
            if isinstance(value, collections.Sequence) and \
                not isinstance(value, bytearray):
                return bytearray().join(flatten(x) for x in value)
            return value
        synthdefs = synthdefs or [self]
        result = []
        encoded_file_type_id = bytearray(b'SCgf')
        result.append(encoded_file_type_id)
        encoded_file_version = SynthDefinition._encode_unsigned_int_32bit(2)
        result.append(encoded_file_version)
        encoded_synthdef_count = SynthDefinition._encode_unsigned_int_16bit(
            len(synthdefs))
        result.append(encoded_synthdef_count)
        for synthdef in synthdefs:
            result.append(synthdef._compile())
        result = flatten(result)
        result = bytearray(result)
        return result

    def free(self):
        pass

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
