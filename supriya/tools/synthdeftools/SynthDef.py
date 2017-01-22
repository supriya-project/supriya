# -*- encoding: utf-8 -*-
from __future__ import print_function
import collections
import copy
import hashlib
import os
import shutil
import tempfile
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class SynthDef(ServerObjectProxy):
    """
    A synth definition.

    ::

        >>> from supriya.tools import synthdeftools
        >>> from supriya.tools import ugentools
        >>> with synthdeftools.SynthDefBuilder(frequency=440) as builder:
        ...     sin_osc = ugentools.SinOsc.ar(frequency=builder['frequency'])
        ...     out = ugentools.Out.ar(bus=0, source=sin_osc)
        ...
        >>> synthdef = builder.build()

    ::

        >>> graph(synthdef)  # doctest: +SKIP

    ::

        >>> from supriya import servertools
        >>> server = servertools.Server().boot()

    ::

        >>> synthdef.allocate(server=server)
        <SynthDef: 9c4eb4778dc0faf39459fa8a5cd45c19>

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

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Main Classes'

    __slots__ = (
        '_compiled_ugen_graph',
        '_constants',
        '_control_ugens',
        '_indexed_parameters',
        '_name',
        '_ugens',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ugens,
        name=None,
        optimize=True,
        parameter_names=None,
        **kwargs
        ):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        ServerObjectProxy.__init__(self)
        compiler = synthdeftools.SynthDefCompiler
        self._name = name
        ugens = copy.deepcopy(ugens)
        ugens = self._flatten_ugens(ugens)
        assert all(isinstance(_, ugentools.UGen) for _ in ugens)
        ugens = self._cleanup_pv_chains(ugens)
        ugens = self._cleanup_local_bufs(ugens)
        if optimize:
            ugens = self._optimize_ugen_graph(ugens)
        ugens = self._sort_ugens_topologically(ugens)
        self._ugens = tuple(ugens)
        self._constants = self._collect_constants(self._ugens)
        self._control_ugens = self._collect_control_ugens(self._ugens)
        self._indexed_parameters = self._collect_indexed_parameters(
            self._control_ugens,
            parameter_names=parameter_names,
            )
        self._compiled_ugen_graph = compiler.compile_ugen_graph(self)
#        if 'decompiled' not in kwargs:
#            try:
#                decompiler = synthdeftools.SynthDefDecompiler
#                assert decompiler.decompile_synthdef(self.compile()) == self
#            except:
#                print('Decompiled SynthDef does not match compiled SynthDef.')
#                raise

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(expr) != type(self):
            return False
        if expr.name != self.name:
            return False
        if expr._compiled_ugen_graph != self._compiled_ugen_graph:
            return False
        return True

    def __graph__(self):
        r"""
        Graphs SynthDef.

        ::

            >>> print(synthdef.__graph__())
            digraph synthdef_... {
                graph [bgcolor=transparent,
                    color=lightslategrey,
                    dpi=72,
                    fontname=Arial,
                    outputorder=edgesfirst,
                    overlap=prism,
                    penwidth=2,
                    rankdir=LR,
                    ranksep=1,
                    splines=spline,
                    style="dotted, rounded"];
                node [fontname=Arial,
                    fontsize=12,
                    penwidth=2,
                    shape=Mrecord,
                    style="filled, rounded"];
                edge [penwidth=2];
                ugen_0 [fillcolor=lightgoldenrod2,
                    label="<f_0> Control\n(control) | { { <f_1_0_0> frequency:\n440.0 } }"];
                ugen_1 [fillcolor=lightsteelblue2,
                    label="<f_0> SinOsc\n(audio) | { { <f_1_0_0> frequency | <f_1_0_1> phase:\n0.0 } | { <f_1_1_0> 0 } }"];
                ugen_2 [fillcolor=lightsteelblue2,
                    label="<f_0> Out\n(audio) | { { <f_1_0_0> bus:\n0.0 | <f_1_0_1> source } }"];
                ugen_0:f_1_0_0:e -> ugen_1:f_1_0_0:w [color=goldenrod];
                ugen_1:f_1_1_0:e -> ugen_2:f_1_0_1:w [color=steelblue];
            }

        Returns Graphviz graph.
        """
        from supriya.tools import synthdeftools
        return synthdeftools.SynthDefGrapher.graph(self)

    def __hash__(self):
        hash_values = (
            type(self),
            self._name,
            self._compiled_ugen_graph,
            )
        return hash(hash_values)

    def __repr__(self):
        return '<{}: {}>'.format(
            type(self).__name__,
            self.actual_name,
            )

    def __str__(self):
        """
        Gets string representation of synth definition.

        ::

            >>> from supriya.tools import synthdeftools
            >>> from supriya.tools import ugentools

        ::

            >>> with synthdeftools.SynthDefBuilder() as builder:
            ...     sin_one = ugentools.SinOsc.ar()
            ...     sin_two = ugentools.SinOsc.ar(frequency=443)
            ...     source = sin_one + sin_two
            ...     out = ugentools.Out.ar(bus=0, source=source)
            ...
            >>> synthdef = builder.build(name='test')

        ::

            >>> graph(synthdef)  # doctest: +SKIP

        ::

            >>> print(synthdef)
            SynthDef test {
                const_0:440.0 -> 0_SinOsc[0:frequency]
                const_1:0.0 -> 0_SinOsc[1:phase]
                const_2:443.0 -> 1_SinOsc[0:frequency]
                const_1:0.0 -> 1_SinOsc[1:phase]
                0_SinOsc[0] -> 2_BinaryOpUGen:ADDITION[0:left]
                1_SinOsc[0] -> 2_BinaryOpUGen:ADDITION[1:right]
                const_1:0.0 -> 3_Out[0:bus]
                2_BinaryOpUGen:ADDITION[0] -> 3_Out[1:source]
            }

        Returns string.
        """
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
                    # 11 decimal places ensures some Py2/3 standardization.
                    input_ = '{:.11f}'.format(input_).rstrip('0')
                    if input_[-1] == '.':
                        input_ += '0'
                    input_name = 'const_{}:{}'.format(input_index, input_)
                else:
                    output_index = 0
                    if isinstance(input_, synthdeftools.OutputProxy):
                        output_index = input_.output_index
                        input_ = input_.source
                    input_name = get_ugen_name(input_)
                    input_name += '[{}]'.format(output_index)
                wire = '    {} -> {}'.format(input_name, ugen_name)
                if argument_name:
                    wire += '[{}:{}]'.format(i, argument_name)
                else:
                    wire += '[{}]'.format(i)
                result.append(wire)
        result.append('}')
        result = '\n'.join(result)
        return result

    ### PRIVATE METHODS ###

    @staticmethod
    def _allocate_synthdefs(synthdefs, server):
        from supriya.tools import requesttools
        d_recv_synthdef_groups = []
        d_recv_synth_group = []
        current_total = 0
        d_load_synthdefs = []
        if synthdefs:
            for synthdef in synthdefs:
                synthdef._register_with_local_server(server=server)
                compiled = synthdef.compile()
                if 8192 < len(compiled):
                    d_load_synthdefs.append(synthdef)
                elif current_total + len(compiled) < 8192:
                    d_recv_synth_group.append(synthdef)
                    current_total += len(compiled)
                else:
                    d_recv_synthdef_groups.append(d_recv_synth_group)
                    d_recv_synth_group = [synthdef]
                    current_total = len(compiled)
        else:
            return
        if d_recv_synth_group:
            d_recv_synthdef_groups.append(d_recv_synth_group)
        for d_recv_synth_group in d_recv_synthdef_groups:
            d_recv_request = requesttools.SynthDefReceiveRequest(
                synthdefs=tuple(d_recv_synth_group),
                )
            d_recv_request.communicate(
                server=server,
                sync=True,
                )
        if d_load_synthdefs:
            temp_directory_path = tempfile.mkdtemp()
            for synthdef in d_load_synthdefs:
                file_name = '{}.scsyndef'.format(synthdef.actual_name)
                file_path = os.path.join(temp_directory_path, file_name)
                with open(file_path, 'wb') as file_pointer:
                    file_pointer.write(synthdef.compile())
            d_load_dir_request = requesttools.SynthDefLoadDirectoryRequest(
                directory_path=temp_directory_path,
                )
            d_load_dir_request.communicate(
                server=server,
                sync=True,
                )
            shutil.rmtree(temp_directory_path)

    @staticmethod
    def _build_control_mapping(parameters):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        control_mapping = collections.OrderedDict()
        scalar_parameters = []
        trigger_parameters = []
        audio_parameters = []
        control_parameters = []
        mapping = {
            synthdeftools.ParameterRate.AUDIO: audio_parameters,
            synthdeftools.ParameterRate.CONTROL: control_parameters,
            synthdeftools.ParameterRate.SCALAR: scalar_parameters,
            synthdeftools.ParameterRate.TRIGGER: trigger_parameters,
            }
        for parameter in parameters:
            mapping[parameter.parameter_rate].append(parameter)
        for filtered_parameters in mapping.values():
            filtered_parameters.sort(key=lambda x: x.name)
        control_ugens = []
        indexed_parameters = []
        starting_control_index = 0
        if scalar_parameters:
            control = ugentools.Control(
                parameters=scalar_parameters,
                calculation_rate=synthdeftools.CalculationRate.SCALAR,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            for parameter in scalar_parameters:
                indexed_parameters.append((starting_control_index, parameter))
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(
                control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        if trigger_parameters:
            control = ugentools.TrigControl(
                parameters=trigger_parameters,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            for parameter in trigger_parameters:
                indexed_parameters.append((starting_control_index, parameter))
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(
                control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        if audio_parameters:
            control = ugentools.AudioControl(
                parameters=audio_parameters,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            for parameter in audio_parameters:
                indexed_parameters.append((starting_control_index, parameter))
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(
                control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        if control_parameters:
            if any(_.lag for _ in control_parameters):
                control = ugentools.LagControl(
                    parameters=control_parameters,
                    calculation_rate=synthdeftools.CalculationRate.CONTROL,
                    starting_control_index=starting_control_index,
                    )
            else:
                control = ugentools.Control(
                    parameters=control_parameters,
                    calculation_rate=synthdeftools.CalculationRate.CONTROL,
                    starting_control_index=starting_control_index,
                    )
            control_ugens.append(control)
            for parameter in control_parameters:
                indexed_parameters.append((starting_control_index, parameter))
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(
                control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        control_ugens = tuple(control_ugens)
        indexed_parameters.sort(
            key=lambda pair: parameters.index(pair[1]),
            )
        indexed_parameters = tuple(indexed_parameters)
        return control_ugens, control_mapping, indexed_parameters

    @staticmethod
    def _build_input_mapping(ugens):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        input_mapping = {}
        for ugen in ugens:
            if not isinstance(ugen, ugentools.PV_ChainUGen):
                continue
            if isinstance(ugen, ugentools.PV_Copy):
                continue
            for i, input_ in enumerate(ugen.inputs):
                if not isinstance(input_, synthdeftools.OutputProxy):
                    continue
                source = input_.source
                if not isinstance(source, ugentools.PV_ChainUGen):
                    continue
                if source not in input_mapping:
                    input_mapping[source] = []
                input_mapping[source].append((ugen, i))
        return input_mapping

    @staticmethod
    def _cleanup_local_bufs(ugens):
        from supriya.tools import ugentools
        local_bufs = []
        processed_ugens = []
        for ugen in ugens:
            if isinstance(ugen, ugentools.MaxLocalBufs):
                continue
            if isinstance(ugen, ugentools.LocalBuf):
                local_bufs.append(ugen)
            processed_ugens.append(ugen)
        if local_bufs:
            max_local_bufs = ugentools.MaxLocalBufs(len(local_bufs))
            for local_buf in local_bufs:
                inputs = list(local_buf.inputs[:2])
                inputs.append(max_local_bufs[0])
                local_buf._inputs = tuple(inputs)
            index = processed_ugens.index(local_bufs[0])
            processed_ugens[index:index] = [max_local_bufs]
        return tuple(processed_ugens)

    @staticmethod
    def _cleanup_pv_chains(ugens):
        from supriya.tools import ugentools
        input_mapping = SynthDef._build_input_mapping(ugens)
        for antecedent, descendants in input_mapping.items():
            if len(descendants) == 1:
                continue
            for descendant, input_index in descendants[:-1]:
                fft_size = antecedent.fft_size
                new_buffer = ugentools.LocalBuf(fft_size)
                pv_copy = ugentools.PV_Copy(antecedent, new_buffer)
                inputs = list(descendant._inputs)
                inputs[input_index] = pv_copy[0]
                descendant._inputs = tuple(inputs)
                index = ugens.index(descendant)
                ugens[index:index] = [fft_size, new_buffer, pv_copy]
        return ugens

    @staticmethod
    def _collect_constants(ugens):
        constants = []
        for ugen in ugens:
            for input_ in ugen._inputs:
                if not isinstance(input_, float):
                    continue
                if input_ not in constants:
                    constants.append(input_)
        return tuple(constants)

    @staticmethod
    def _collect_control_ugens(ugens):
        from supriya.tools import ugentools
        control_ugens = tuple(
            _ for _ in ugens
            if isinstance(_, ugentools.Control)
            )
        return control_ugens

    @staticmethod
    def _collect_indexed_parameters(
        control_ugens,
        parameter_names=None,
        ):
        indexed_parameters = []
        parameters = {}
        for control_ugen in control_ugens:
            index = control_ugen.starting_control_index
            for parameter in control_ugen.parameters:
                parameters[parameter.name] = (index, parameter)
                index += len(parameter)
        parameter_names = parameter_names or sorted(parameters)
        assert sorted(parameter_names) == sorted(parameters)
        for parameter_name in parameter_names:
            indexed_parameters.append(parameters[parameter_name])
        indexed_parameters = tuple(indexed_parameters)
        return indexed_parameters

    @staticmethod
    def _collect_parameters(control_ugens):
        parameters = []
        for control_ugen in control_ugens:
            parameters.extend(control_ugen._parameters)
        return parameters

    @staticmethod
    def _extract_parameters(ugens):
        from supriya.tools import synthdeftools
        parameters = set()
        for ugen in ugens:
            if isinstance(ugen, synthdeftools.Parameter):
                parameters.add(ugen)
        ugens = tuple(ugen for ugen in ugens if ugen not in parameters)
        parameters = tuple(sorted(parameters, key=lambda x: x.name))
        return ugens, parameters

    @staticmethod
    def _flatten_ugens(ugens):
        def recurse(ugen):
            if ugen not in flattened_ugens:
                flattened_ugens.append(ugen)
            if isinstance(ugen, synthdeftools.Parameter):
                return
            elif isinstance(ugen, synthdeftools.OutputProxy):
                source = ugen.source
                if source not in flattened_ugens:
                    flattened_ugens.append(source)
                    recurse(source)
                return
            for input_ in ugen.inputs:
                if isinstance(input_, synthdeftools.Parameter):
                    if input_ not in flattened_ugens:
                        flattened_ugens.append(input_)
                elif isinstance(input_, synthdeftools.OutputProxy):
                    if input_.source not in flattened_ugens:
                        flattened_ugens.append(input_.source)
                        recurse(input_.source)
                elif isinstance(input_, ugentools.UGen):
                    if input_ not in flattened_ugens:
                        flattened_ugens.append(input_)
                        recurse(input_)
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        flattened_ugens = []
        for ugen in ugens:
            recurse(ugen)
        return flattened_ugens

    def _get_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.FormatSpecification(
            repr_is_bracketed=True,
            storage_format_is_bracketed=True,
            storage_format_is_indented=False,
            storage_format_args_values=[self.actual_name],
            storage_format_kwargs_names=[]
            )

    @staticmethod
    def _initialize_topological_sort(ugens):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        ugens = list(ugens)
        sort_bundles = collections.OrderedDict()
        width_first_antecedents = []
        for ugen in ugens:
            sort_bundles[ugen] = synthdeftools.UGenSortBundle(
                ugen, width_first_antecedents)
            if isinstance(ugen, ugentools.WidthFirstUGen):
                width_first_antecedents.append(ugen)
        for ugen in ugens:
            sort_bundle = sort_bundles[ugen]
            sort_bundle._initialize_topological_sort(sort_bundles)
            sort_bundle.descendants[:] = sorted(
                sort_bundles[ugen].descendants,
                key=lambda x: ugens.index(ugen),
                )
        return sort_bundles

    @staticmethod
    def _optimize_ugen_graph(ugens):
        sort_bundles = SynthDef._initialize_topological_sort(ugens)
        for ugen in ugens:
            ugen._optimize_graph(sort_bundles)
        return tuple(sort_bundles)

    def _register_with_local_server(
        self,
        server=None,
        ):
        ServerObjectProxy.allocate(self, server=server)
        synthdef_name = self.actual_name
        self.server._synthdefs[synthdef_name] = self

    @staticmethod
    def _remap_controls(ugens, control_mapping):
        for ugen in ugens:
            inputs = list(ugen.inputs)
            for i, input_ in enumerate(inputs):
                if input_ in control_mapping:
                    output_proxy = control_mapping[input_]
                    inputs[i] = output_proxy
            ugen._inputs = tuple(inputs)

    @staticmethod
    def _sort_ugens_topologically(ugens):
        sort_bundles = SynthDef._initialize_topological_sort(ugens)
        available_ugens = []
        for ugen in reversed(ugens):
            sort_bundles[ugen]._make_available(available_ugens)
        out_stack = []
        while available_ugens:
            available_ugen = available_ugens.pop()
            sort_bundles[available_ugen]._schedule(
                available_ugens, out_stack, sort_bundles)
        return out_stack

    ### PUBLIC METHODS ###

    def allocate(
        self,
        server=None,
        ):
        self._allocate_synthdefs((self,), server)
        return self

    def compile(self):
        from supriya.tools.synthdeftools import SynthDefCompiler
        synthdefs = [self]
        result = SynthDefCompiler.compile_synthdefs(synthdefs)
        return result

    def free(self):
        from supriya.tools import requesttools
        synthdef_name = self.actual_name
        del(self.server._synthdefs[synthdef_name])
        request = requesttools.SynthDefFreeRequest(
            synthdef=self,
            )
        if self.server.is_running:
            request.communicate(server=self.server)
        ServerObjectProxy.free(self)

    def play(self, add_action=None, target_node=None, **kwargs):
        """
        Plays the synthdef on the server.

        ::

            >>> server = Server().boot()
            >>> synthdef = synthdefs.default
            >>> synth = synthdef.play()
            >>> server = server.quit()

        """
        from supriya.tools import servertools
        if target_node is not None:
            target_node = servertools.Node.expr_as_target(target_node)
            server = target_node.server
        else:
            server = servertools.Server.get_default_server()
            target_node = servertools.Node.expr_as_target(server)
        if not server.is_running:
            server.boot()
        if not self.is_allocated:
            self.allocate(server=server)
            self.server.sync()
        synth = servertools.Synth(self, **kwargs)
        synth.allocate(
            add_action=add_action,
            sync=True,
            target_node=target_node,
            )
        return synth

    def to_dict(self):
        """
        Convert SynthDef to JSON-serializable dictionay.

        ::

            >>> import json
            >>> result = synthdefs.default.to_dict()
            >>> result = json.dumps(
            ...     result,
            ...     indent=4,
            ...     separators=(',', ': '),
            ...     sort_keys=True,
            ...     )
            >>> print(result)
            {
                "synthdef": {
                    "hash": "da0982184cc8fa54cf9d288a0fe1f6ca",
                    "name": "da0982184cc8fa54cf9d288a0fe1f6ca",
                    "parameters": {
                        "amplitude": {
                            "range": [
                                0,
                                1
                            ],
                            "rate": "control",
                            "unit": null,
                            "value": 0.1
                        },
                        "frequency": {
                            "range": [
                                0,
                                1
                            ],
                            "rate": "control",
                            "unit": null,
                            "value": 440.0
                        },
                        "gate": {
                            "range": [
                                0,
                                1
                            ],
                            "rate": "control",
                            "unit": null,
                            "value": 1.0
                        },
                        "out": {
                            "range": [
                                0,
                                1
                            ],
                            "rate": "scalar",
                            "unit": null,
                            "value": 0.0
                        },
                        "pan": {
                            "range": [
                                0,
                                1
                            ],
                            "rate": "control",
                            "unit": null,
                            "value": 0.5
                        }
                    }
                }
            }

        """
        result = {
            'name': self.actual_name,
            'hash': self.anonymous_name,
            'parameters': {},
            }
        for parameter_name, parameter in self.parameters.items():
            range_ = [0, 1]
            if parameter.range_:
                range_ = [
                    parameter.range_.minimum,
                    parameter.range_.maximum,
                    ]
            rate = parameter.parameter_rate.name.lower()
            result['parameters'][parameter_name] = {
                'rate': rate,
                'range': range_,
                'unit': parameter.unit,
                'value': parameter.value,
                }
        result = {'synthdef': result}
        return result

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
    def audio_channel_count(self):
        return max(
            self.audio_input_channel_count,
            self.audio_output_channel_count,
            )

    @property
    def audio_input_channel_count(self):
        """
        Gets audio input channel count of synthdef.

        ::

            >>> with SynthDefBuilder() as builder:
            ...     audio_in = ugentools.In.ar(channel_count=1)
            ...     control_in = ugentools.In.kr(channel_count=2)
            ...     sin = ugentools.SinOsc.ar(
            ...          frequency=audio_in,
            ...          )
            ...     source = audio_in * control_in[1]
            ...     audio_out = ugentools.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()

        ::

            >>> graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.audio_input_channel_count
            1

        Returns integer.
        """
        from supriya.tools import synthdeftools
        ugens = tuple(_ for _ in self.input_ugens
            if _.calculation_rate == synthdeftools.CalculationRate.AUDIO)
        if len(ugens) == 1:
            return ugens[0].channel_count
        elif not ugens:
            return 0
        raise ValueError

    @property
    def audio_output_channel_count(self):
        """
        Gets audio output channel count of synthdef.

        ::

            >>> with SynthDefBuilder() as builder:
            ...     audio_in = ugentools.In.ar(channel_count=1)
            ...     control_in = ugentools.In.kr(channel_count=2)
            ...     sin = ugentools.SinOsc.ar(
            ...          frequency=audio_in,
            ...          )
            ...     source = audio_in * control_in[1]
            ...     audio_out = ugentools.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()

        ::

            >>> graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.audio_output_channel_count
            4

        Returns integer.
        """
        from supriya.tools import synthdeftools
        ugens = tuple(_ for _ in self.output_ugens
            if _.calculation_rate == synthdeftools.CalculationRate.AUDIO)
        if len(ugens) == 1:
            return len(ugens[0].source)
        elif not ugens:
            return 0
        raise ValueError

    @property
    def constants(self):
        return self._constants

    @property
    def control_ugens(self):
        return self._control_ugens

    @property
    def control_channel_count(self):
        return max(
            self.control_input_channel_count,
            self.control_output_channel_count,
            )

    @property
    def control_input_channel_count(self):
        """
        Gets control input channel count of synthdef.

        ::

            >>> with SynthDefBuilder() as builder:
            ...     audio_in = ugentools.In.ar(channel_count=1)
            ...     control_in = ugentools.In.kr(channel_count=2)
            ...     sin = ugentools.SinOsc.ar(
            ...          frequency=audio_in,
            ...          )
            ...     source = audio_in * control_in[1]
            ...     audio_out = ugentools.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()

        ::

            >>> graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.control_input_channel_count
            2

        Returns integer.
        """
        from supriya.tools import synthdeftools
        ugens = tuple(_ for _ in self.input_ugens
            if _.calculation_rate == synthdeftools.CalculationRate.CONTROL)
        if len(ugens) == 1:
            return ugens[0].channel_count
        elif not ugens:
            return 0
        raise ValueError

    @property
    def control_output_channel_count(self):
        """
        Gets control output channel count of synthdef.

        ::

            >>> with SynthDefBuilder() as builder:
            ...     audio_in = ugentools.In.ar(channel_count=1)
            ...     control_in = ugentools.In.kr(channel_count=2)
            ...     sin = ugentools.SinOsc.ar(
            ...          frequency=audio_in,
            ...          )
            ...     source = audio_in * control_in[1]
            ...     audio_out = ugentools.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()

        ::

            >>> graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.control_output_channel_count
            0

        Returns integer.
        """
        from supriya.tools import synthdeftools
        ugens = tuple(_ for _ in self.output_ugens
            if _.calculation_rate == synthdeftools.CalculationRate.CONTROL)
        if len(ugens) == 1:
            return len(ugens[0].source)
        elif not ugens:
            return 0
        raise ValueError

    @property
    def done_actions(self):
        done_actions = set()
        for ugen in self.ugens:
            done_action = ugen._get_done_action()
            if done_action is not None:
                done_actions.add(done_action)
        return sorted(done_actions)

    @property
    def has_gate(self):
        return 'gate' in self.parameter_names

    @property
    def indexed_parameters(self):
        return self._indexed_parameters

    @property
    def input_ugens(self):
        return tuple(_ for _ in self.ugens if _.is_input_ugen)

    @property
    def is_allocated(self):
        if self.server is not None:
            return self in self.server
        return False

    @property
    def name(self):
        return self._name

    @property
    def output_ugens(self):
        return tuple(_ for _ in self.ugens if _.is_output_ugen)

    @property
    def parameters(self):
        return {parameter.name: parameter
            for index, parameter in self.indexed_parameters}

    @property
    def parameter_names(self):
        return [parameter.name for index, parameter in self.indexed_parameters]

    @property
    def ugens(self):
        return self._ugens
