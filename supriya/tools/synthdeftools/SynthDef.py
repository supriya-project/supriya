# -*- encoding: utf-8 -*-
import collections
import hashlib
import struct
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class SynthDef(ServerObjectProxy):
    r'''A SuperCollider synth definition.

    ::

        >>> from supriya import synthdeftools
        >>> from supriya import ugentools
        >>> synthdef = synthdeftools.SynthDef(
        ...     'test',
        ...     freq_l=1200,
        ...     freq_r=1205,
        ...     )
        >>> controls = synthdef.controls
        >>> line = ugentools.Line.kr(
        ...     start=100,
        ...     stop=(
        ...         controls['freq_l'],
        ...         controls['freq_r'],
        ...         ),
        ...     )
        >>> sin_osc = ugentools.SinOsc.ar(
        ...     frequency=line,
        ...     phase=0,
        ...     )
        >>> sin_osc = sin_osc * 0.2
        >>> out = ugentools.Out.ar(
        ...     bus=0,
        ...     source=sin_osc,
        ...     )
        >>> synthdef.add_ugen(out)

    ::

        >>> from supriya import servertools
        >>> server = servertools.Server().boot()

    ::

        >>> synthdef.allocate(server=server)

    ::

        >>> synthdef in server
        True

    ::

        >>> synthdef.free()

    ::

        >>> synthdef in server
        False

    ::

        >>> server.quit()
        <Server: offline>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_available_ugens',
        '_compiled_ugen_graph',
        '_constants',
        '_controls',
        '_name',
        '_parameter_names',
        '_parameters',
        '_pending_ugens',
        '_ugens',
        '_width_first_ugens',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name=None,
        **kwargs
        ):
        from supriya.tools import synthdeftools
        ServerObjectProxy.__init__(self)
        self._available_ugens = []
        self._constants = {}
        self._name = name
        self._parameter_names = {}
        self._parameters = []
        self._pending_ugens = set()
        self._ugens = []
        self._width_first_ugens = []
        control_names = []
        for name, value in sorted(kwargs.items()):
            self._add_parameter(name, value)
            control_names.append(name)
        self._controls = synthdeftools.Control(control_names)
        if control_names:
            self._add_ugen(self._controls)
        self._compiled_ugen_graph = self._compile_ugen_graph()

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(expr) != type(self):
            return False
        if expr.name != self.name:
            return False
        if expr._compiled_ugen_graph != self._compiled_ugen_graph:
            return False
        return True

    def __hash__(self):
        hash_values = (
            type(self),
            self._name,
            self._compiled_ugen_graph,
            )
        return hash(hash_values)

    def __str__(self):
        r'''Gets string representation of synth definition.

        ::

            >>> from supriya.tools import synthdeftools
            >>> from supriya.tools import ugentools
            >>> synthdef = synthdeftools.SynthDef('test')

        ::

            >>> sin_one = ugentools.SinOsc.ar()
            >>> sin_two = ugentools.SinOsc.ar(frequency=443)
            >>> sum = sin_one + sin_two
            >>> out = ugentools.Out.ar(bus=0, source=sum)
            >>> synthdef.add_ugen(out)

        ::

            >>> print(synthdef)
            SynthDef test {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                const_2:443.0 -> 1_SinOsc[0:frequency]
                const_1:0.0 -> 1_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:ADDITION[0:left]
                1_SinOsc[0] -> 2_BinaryOpUGen:ADDITION[1:right]
                const_1:0.0 -> 3_Out[0]
                2_BinaryOpUGen:ADDITION[0] -> 3_Out[1]
            }

        Returns string.
        '''
        def get_ugen_name(ugen):
            ugen_index = self._get_ugen_index(ugen)
            ugen_class = type(ugen).__name__
            if isinstance(ugen, ugentools.BinaryOpUGen):
                ugen_op = synthdeftools.BinaryOperator.from_expr(
                    ugen.special_index)
                ugen_op_name = ugen_op.name
                ugen_name = '{}_{}:{}'.format(
                    ugen_index,
                    ugen_class,
                    ugen_op_name,
                    )
            elif isinstance(ugen, ugentools.UnaryOpUGen):
                ugen_op = synthdeftools.UnaryOperator.from_expr(
                    ugen.special_index)
                ugen_op_name = ugen_op.name
                ugen_name = '{}_{}:{}'.format(
                    ugen_index,
                    ugen_class,
                    ugen_op_name,
                    )
            else:
                ugen_name = '{}_{}'.format(ugen_index, ugen_class)
            return ugen_name
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        result = []
        result.append('SynthDef {} {{'.format(self.actual_name))
        for ugen in self._ugens:
            ugen_name = get_ugen_name(ugen)
            for i, input_ in enumerate(ugen.inputs):
                argument_name = None
                if i < len(ugen._ordered_input_names):
                    argument_name = ugen._ordered_input_names[i]
                if isinstance(input_, float):
                    input_index = self._get_constant_index(input_)
                    input_name = 'const_{}:{}'.format(input_index, input_)
                else:
                    output_index = 0
                    if isinstance(input_, synthdeftools.OutputProxy):
                        output_index = input_.output_index 
                        input_ = input_.source
                    input_name = get_ugen_name(input_)
                    input_name += '[{}]'.format(output_index)
                wire = '\t{} -> {}'.format(input_name, ugen_name)
                if argument_name:
                    wire += '[{}:{}]'.format(i, argument_name)
                else:
                    wire += '[{}]'.format(i)
                result.append(wire)
        result.append('}')
        result = '\n'.join(result)
        return result
            
    ### PRIVATE METHODS ###

    def _add_constant(self, value):
        if value not in self._constants:
            self._constants[value] = len(self.constants)

    def _add_parameter(self, name, value):
        self._parameter_names[name] = len(self._parameters)
        self._parameters.append(value)

    def _add_ugen(self, ugen):
        from supriya import synthdeftools
        def resolve(ugen, synthdef):
            for x in ugen.inputs:
                if isinstance(x, synthdeftools.OutputProxy):
                    synthdef._add_ugen(x.source)
            for x in ugen.sort_bundle.descendants:
                synthdef._add_ugen(x)
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
            if isinstance(ugen, synthdeftools.WidthFirstUGen):
                self._width_first_ugens.append(ugen)
            ugen.sort_bundle.synthdef = self
            self._pending_ugens.remove(ugen)

    def _cleanup_topological_sort(self):
        for ugen in self._ugens:
            ugen.sort_bundle.clear()

    def _collect_constants(self):
        self._constants = {}
        for ugen in self._ugens:
            ugen._collect_constants()

    def _compile(self):
        result = SynthDef._encode_string(self.name)
        result += self._compiled_ugen_graph
        return result

    def _compile_anonymously(self):
        result = SynthDef._encode_string(self.anonymous_name)
        result += self._compiled_ugen_graph
        return result

    def _compile_ugen_graph(self):
        result = []
        result.append(SynthDef._encode_unsigned_int_32bit(len(self.constants)))
        for key, value in sorted(
            self.constants.items(),
            key=lambda item: item[1],
            ):
            result.append(SynthDef._encode_float(key))
        result.append(SynthDef._encode_unsigned_int_32bit(len(self.parameters)))
        for value in self.parameters:
            result.append(SynthDef._encode_float(value))
        result.append(SynthDef._encode_unsigned_int_32bit(
            len(self.parameter_names)))
        for key, value in sorted(
            self.parameter_names.items(),
            key=lambda x: x[1],
            ):
            result.append(SynthDef._encode_string(key))
            result.append(SynthDef._encode_unsigned_int_32bit(value))
        result.append(SynthDef._encode_unsigned_int_32bit(len(self.ugens)))
        for ugen_index, ugen in enumerate(self.ugens):
            result.append(ugen.compile(self))
        result.append(SynthDef._encode_unsigned_int_16bit(0))
        result = bytes().join(result)
        return result

    @staticmethod
    def _encode_float(value):
        return bytes(struct.pack('>f', value))

    @staticmethod
    def _encode_string(value):
        result = bytes(struct.pack('>B', len(value)))
        result += bytes(bytearray(value, encoding='ascii'))
        return result

    @staticmethod
    def _encode_unsigned_int_8bit(value):
        return bytes(struct.pack('>B', value))

    @staticmethod
    def _encode_unsigned_int_16bit(value):
        return bytes(struct.pack('>H', value))

    @staticmethod
    def _encode_unsigned_int_32bit(value):
        return bytes(struct.pack('>I', value))

    def _get_constant_index(self, value):
        return self._constants[value]

    def _get_ugen_index(self, ugen):
        return self._ugens.index(ugen)

    def _initialize_topological_sort(self):
        self._available_ugens = []
        for ugen in self.ugens:
            ugen.sort_bundle.clear()
        for ugen in self.ugens:
            ugen._initialize_topological_sort()
            ugen.sort_bundle.descendants[:] = sorted(
                ugen.sort_bundle.descendants,
                key=lambda x: x.sort_bundle.synthdef.ugens.index(ugen),
                )
        for ugen in reversed(self.ugens):
            ugen.sort_bundle._make_available()

    def _sort_ugens_topologically(self):
        out_stack = []
        self._initialize_topological_sort()
        while self._available_ugens:
            available_ugen = self._available_ugens.pop()
            available_ugen._schedule(out_stack)
        self._ugens = out_stack
        self._cleanup_topological_sort()

    ### PUBLIC METHODS ###

    def allocate(self, server=None):
        from supriya.tools import servertools
        ServerObjectProxy.allocate(self, server=server)
        synthdef_name = self.actual_name
        self.server._synthdefs[synthdef_name] = self
        message = servertools.CommandManager.make_synthdef_receive_message(
            synthdef=self,
            )
        self.server.send_message(message)

    def add_ugen(self, ugen):
        self._add_ugen(ugen)
        self._sort_ugens_topologically()
        self._collect_constants()
        self._compiled_ugen_graph = self._compile_ugen_graph()

    def compile(self, synthdefs=None):
        def flatten(value):
            if isinstance(value, collections.Sequence) and \
                not isinstance(value, (bytes, bytearray)):
                return bytes().join(flatten(x) for x in value)
            return value
        synthdefs = synthdefs or [self]
        result = []
        encoded_file_type_id = b'SCgf'
        result.append(encoded_file_type_id)
        encoded_file_version = SynthDef._encode_unsigned_int_32bit(2)
        result.append(encoded_file_version)
        encoded_synthdef_count = SynthDef._encode_unsigned_int_16bit(
            len(synthdefs))
        result.append(encoded_synthdef_count)
        for synthdef in synthdefs:
            if synthdef.name:
                result.append(synthdef._compile())
            else:
                result.append(synthdef._compile_anonymously())
        result = flatten(result)
        result = bytes(result)
        return result

    def free(self):
        from supriya.tools import servertools
        synthdef_name = self.name or self.anonymous_name
        del(self.server._synthdefs[synthdef_name])
        message = servertools.CommandManager.make_synthdef_free_message(
            synthdef=self,
            )
        self.server.send_message(message)
        ServerObjectProxy.free(self)

    ### PUBLIC PROPERTIES ###

    @property
    def actual_name(self):
        return self.name or self.anonymous_name

    @property
    def anonymous_name(self):
        md5 = hashlib.md5()
        md5.update(self._compiled_ugen_graph)
        anonymous_name = md5.hexdigest()
        return anonymous_name

    @property
    def controls(self):
        return self._controls

    @property
    def constants(self):
        return self._constants

    @property
    def is_allocated(self):
        if self.server is not None:
            return self in self.server
        return False

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
