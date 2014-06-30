# -*- encoding: utf-8 -*-
import collections
import hashlib
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
        from supriya.tools import ugentools
        ServerObjectProxy.__init__(self)
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
        self._controls = ugentools.Control(
            control_names,
            rate=synthdeftools.Rate.CONTROL,
            )
        if control_names:
            self._add_ugen(self._controls)
        self._compiled_ugen_graph = \
            synthdeftools.SynthDefCompiler.compile_ugen_graph(self)

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
            ugen_index = self._ugens.index(ugen)
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
                    input_index = self._constants.index(input_)
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

    def _add_parameter(self, name, value):
        self._parameter_names[name] = len(self._parameters)
        self._parameters.append(value)

    def _add_ugen(self, ugen):
        from supriya import synthdeftools
        from supriya import ugentools
        def resolve(ugen, synthdef):
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
            if isinstance(ugen, ugentools.WidthFirstUGen):
                self._width_first_ugens.append(ugen)
            self._pending_ugens.remove(ugen)

    def _collect_constants(self):
        constants = []
        for ugen in self._ugens:
            for input_ in ugen._inputs:
                if not isinstance(input_, float):
                    continue
                if input_ not in constants:
                    constants.append(input_)
        self._constants = tuple(constants)

    def _sort_ugens_topologically(self):
        from supriya.tools import synthdeftools
        available_ugens = []
        sort_bundles = {}
        ugens = list(self.ugens)
        for ugen in ugens:
            sort_bundles[ugen] = synthdeftools.UGenSortBundle(ugen)
        for ugen in ugens:
            sort_bundle = sort_bundles[ugen]
            sort_bundle._initialize_topological_sort(sort_bundles)
            sort_bundle.descendants[:] = sorted(
                sort_bundles[ugen].descendants,
                key=lambda x: ugens.index(ugen),
                )
        for ugen in reversed(ugens):
            sort_bundles[ugen]._make_available(available_ugens)
        out_stack = []
        while available_ugens:
            available_ugen = available_ugens.pop()
            sort_bundles[available_ugen]._schedule(
                available_ugens, out_stack, sort_bundles)
        self._ugens = out_stack

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
        from supriya.tools import synthdeftools
        self._add_ugen(ugen)
        self._sort_ugens_topologically()
        self._collect_constants()
        self._compiled_ugen_graph = \
            synthdeftools.SynthDefCompiler.compile_ugen_graph(self)

    def compile(self, synthdefs=None):
        from supriya.tools.synthdeftools import SynthDefCompiler
        synthdefs = synthdefs or [self]
        result = SynthDefCompiler.compile_synthdefs(synthdefs)
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
