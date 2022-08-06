import collections
import copy
import hashlib
import os
import pathlib
import shutil
import subprocess
import tempfile

import yaml

from supriya import (
    BinaryOperator,
    CalculationRate,
    ParameterRate,
    UnaryOperator,
    sclang,
)
from supriya.system import SupriyaObject

from .bases import BinaryOpUGen, UGen, UnaryOpUGen, WidthFirstUGen
from .compilers import SynthDefCompiler
from .controls import AudioControl, Control, LagControl, Parameter, TrigControl
from .grapher import SynthDefGrapher
from .mixins import OutputProxy, UGenMethodMixin


class SynthDef:
    """
    A synth definition.

    ::

        >>> import supriya.synthdefs
        >>> import supriya.ugens
        >>> with supriya.synthdefs.SynthDefBuilder(frequency=440) as builder:
        ...     sin_osc = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
        ...     out = supriya.ugens.Out.ar(bus=0, source=sin_osc)
        ...
        >>> synthdef = builder.build()

    ::

        >>> supriya.graph(synthdef)  # doctest: +SKIP

    ::

        >>> import supriya.realtime
        >>> server = supriya.Server().boot()

    ::

        >>> synthdef.allocate(server=server)
        <SynthDef: 9c4eb4778dc0faf39459fa8a5cd45c19>

    ::

        >>> synthdef in server
        True

    ::

        >>> synthdef.free(server)

    ::

        >>> synthdef in server
        False

    ::

        >>> server.quit()
        <Server: offline>

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_compiled_ugen_graph",
        "_constants",
        "_control_ugens",
        "_indexed_parameters",
        "_name",
        "_ugens",
    )

    ### INITIALIZER ###

    def __init__(self, ugens, name=None, optimize=True, parameter_names=None, **kwargs):
        self._name = name
        ugens = list(copy.deepcopy(ugens))
        assert all(isinstance(_, UGen) for _ in ugens)
        ugens = self._cleanup_pv_chains(ugens)
        ugens = self._cleanup_local_bufs(ugens)
        if optimize:
            ugens = self._optimize_ugen_graph(ugens)
        ugens = self._sort_ugens_topologically(ugens)
        self._ugens = tuple(ugens)
        self._constants = self._collect_constants(self._ugens)
        self._control_ugens = self._collect_control_ugens(self._ugens)
        self._indexed_parameters = self._collect_indexed_parameters(
            self._control_ugens, parameter_names=parameter_names
        )
        self._compiled_ugen_graph = SynthDefCompiler.compile_ugen_graph(self)

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

            >>> with supriya.synthdefs.SynthDefBuilder(frequency=440) as builder:
            ...     sin_osc = supriya.ugens.SinOsc.ar(frequency=builder["frequency"])
            ...     out = supriya.ugens.Out.ar(bus=0, source=sin_osc)
            ...
            >>> synthdef = builder.build()
            >>> print(format(synthdef.__graph__(), "graphviz"))
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
        return SynthDefGrapher.graph(self)

    def __hash__(self):
        hash_values = (type(self), self._name, self._compiled_ugen_graph)
        return hash(hash_values)

    def __repr__(self):
        return "<{}: {}>".format(type(self).__name__, self.actual_name)

    def __str__(self):
        """
        Gets string representation of synth definition.

        ::

            >>> import supriya.synthdefs
            >>> import supriya.ugens

        ::

            >>> with supriya.synthdefs.SynthDefBuilder() as builder:
            ...     sin_one = supriya.ugens.SinOsc.ar()
            ...     sin_two = supriya.ugens.SinOsc.ar(frequency=443)
            ...     source = sin_one + sin_two
            ...     out = supriya.ugens.Out.ar(bus=0, source=source)
            ...
            >>> synthdef = builder.build(name="test")

        ::

            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> print(synthdef)
            synthdef:
                name: test
                ugens:
                -   SinOsc.ar/0:
                        frequency: 440.0
                        phase: 0.0
                -   SinOsc.ar/1:
                        frequency: 443.0
                        phase: 0.0
                -   BinaryOpUGen(ADDITION).ar:
                        left: SinOsc.ar/0[0]
                        right: SinOsc.ar/1[0]
                -   Out.ar:
                        bus: 0.0
                        source[0]: BinaryOpUGen(ADDITION).ar[0]

        Returns string.
        """

        def get_ugen_names():
            grouped_ugens = {}
            named_ugens = {}
            for ugen in self._ugens:
                key = (type(ugen), ugen.calculation_rate, ugen.special_index)
                grouped_ugens.setdefault(key, []).append(ugen)
            for ugen in self._ugens:
                parts = [type(ugen).__name__]
                if isinstance(ugen, BinaryOpUGen):
                    ugen_op = BinaryOperator.from_expr(ugen.special_index)
                    parts.append("(" + ugen_op.name + ")")
                elif isinstance(ugen, UnaryOpUGen):
                    ugen_op = UnaryOperator.from_expr(ugen.special_index)
                    parts.append("(" + ugen_op.name + ")")
                parts.append("." + ugen.calculation_rate.token)
                key = (type(ugen), ugen.calculation_rate, ugen.special_index)
                related_ugens = grouped_ugens[key]
                if len(related_ugens) > 1:
                    parts.append("/{}".format(related_ugens.index(ugen)))
                named_ugens[ugen] = "".join(parts)
            return named_ugens

        def get_parameter_name(input_, output_index=0):
            if isinstance(input_, Parameter):
                return ":{}".format(input_.name)
            elif isinstance(input_, Control):
                # Handle array-like parameters
                value_index = 0
                for parameter in input_.parameters:
                    values = parameter.value
                    if isinstance(values, float):
                        values = [values]
                    for i in range(len(values)):
                        if value_index != output_index:
                            value_index += 1
                            continue
                        elif len(values) == 1:
                            return ":{}".format(parameter.name)
                        else:
                            return ":{}[{}]".format(parameter.name, i)
            return ""

        ugens = []
        named_ugens = get_ugen_names()
        for ugen in self._ugens:
            ugen_dict = {}
            ugen_name = named_ugens[ugen]
            for input_name, input_ in zip(ugen._input_names, ugen._inputs):

                if isinstance(input_name, str):
                    argument_name = input_name
                else:
                    argument_name = f"{input_name[0]}[{input_name[1]}]"
                if isinstance(input_, float):
                    value = input_
                else:
                    output_index = 0
                    if isinstance(input_, OutputProxy):
                        output_index = input_.output_index
                        input_ = input_.source
                    input_name = named_ugens[input_]
                    value = "{}[{}{}]".format(
                        input_name,
                        output_index,
                        get_parameter_name(input_, output_index),
                    )
                ugen_dict[argument_name] = value
            if not ugen_dict:
                ugen_dict = None
            ugens.append({ugen_name: ugen_dict})

        result = {
            "synthdef": {
                "name": self.actual_name,
                # 'hash': self.anonymous_name,
                "ugens": ugens,
            }
        }
        return yaml.dump(
            result, default_flow_style=False, indent=4, sort_keys=False
        ).rstrip()

    ### PRIVATE METHODS ###

    @staticmethod
    def _allocate_synthdefs(synthdefs, server):
        # TODO: Should sync be configurable here?
        import supriya.commands

        d_recv_synthdef_groups = []
        d_recv_synth_group = []
        current_total = 0
        d_load_synthdefs = []
        if not synthdefs:
            return
        for synthdef in synthdefs:
            # synthdef._register_with_local_server(server=server)
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
        if d_recv_synth_group:
            d_recv_synthdef_groups.append(d_recv_synth_group)
        for d_recv_synth_group in d_recv_synthdef_groups:
            d_recv_request = supriya.commands.SynthDefReceiveRequest(
                synthdefs=tuple(d_recv_synth_group)
            )

            d_recv_request.communicate(server=server, sync=True)
        if d_load_synthdefs:
            temp_directory_path = tempfile.mkdtemp()
            for synthdef in d_load_synthdefs:
                file_name = "{}.scsyndef".format(synthdef.actual_name)
                file_path = os.path.join(temp_directory_path, file_name)
                with open(file_path, "wb") as file_pointer:
                    file_pointer.write(synthdef.compile())
            d_load_dir_request = supriya.commands.SynthDefLoadDirectoryRequest(
                directory_path=temp_directory_path
            )
            d_load_dir_request.communicate(server=server, sync=True)
            shutil.rmtree(temp_directory_path)

    @staticmethod
    def _build_control_mapping(parameters):
        control_mapping = collections.OrderedDict()
        scalar_parameters = []
        trigger_parameters = []
        audio_parameters = []
        control_parameters = []
        mapping = {
            ParameterRate.AUDIO: audio_parameters,
            ParameterRate.CONTROL: control_parameters,
            ParameterRate.SCALAR: scalar_parameters,
            ParameterRate.TRIGGER: trigger_parameters,
        }
        for parameter in parameters:
            mapping[parameter.parameter_rate].append(parameter)
        for filtered_parameters in mapping.values():
            filtered_parameters.sort(key=lambda x: x.name)
        control_ugens = []
        indexed_parameters = []
        starting_control_index = 0
        if scalar_parameters:
            control = Control(
                parameters=scalar_parameters,
                calculation_rate=CalculationRate.SCALAR,
                starting_control_index=starting_control_index,
            )
            control_ugens.append(control)
            for parameter in scalar_parameters:
                indexed_parameters.append((starting_control_index, parameter))
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        if trigger_parameters:
            control = TrigControl(
                parameters=trigger_parameters,
                starting_control_index=starting_control_index,
            )
            control_ugens.append(control)
            for parameter in trigger_parameters:
                indexed_parameters.append((starting_control_index, parameter))
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        if audio_parameters:
            control = AudioControl(
                parameters=audio_parameters,
                starting_control_index=starting_control_index,
            )
            control_ugens.append(control)
            for parameter in audio_parameters:
                indexed_parameters.append((starting_control_index, parameter))
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        if control_parameters:
            if any(_.lag for _ in control_parameters):
                control = LagControl(
                    parameters=control_parameters,
                    calculation_rate=CalculationRate.CONTROL,
                    starting_control_index=starting_control_index,
                )
            else:
                control = Control(
                    parameters=control_parameters,
                    calculation_rate=CalculationRate.CONTROL,
                    starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            for parameter in control_parameters:
                indexed_parameters.append((starting_control_index, parameter))
                starting_control_index += len(parameter)
            for i, output_proxy in enumerate(control._get_parameter_output_proxies()):
                control_mapping[output_proxy] = control[i]
        control_ugens = tuple(control_ugens)
        indexed_parameters.sort(key=lambda pair: parameters.index(pair[1]))
        indexed_parameters = tuple(indexed_parameters)
        return control_ugens, control_mapping, indexed_parameters

    @staticmethod
    def _build_input_mapping(ugens):
        import supriya.ugens

        input_mapping = {}
        for ugen in ugens:
            if not isinstance(ugen, supriya.ugens.PV_ChainUGen):
                continue
            if isinstance(ugen, supriya.ugens.PV_Copy):
                continue
            for i, input_ in enumerate(ugen.inputs):
                if not isinstance(input_, OutputProxy):
                    continue
                source = input_.source
                if not isinstance(source, supriya.ugens.PV_ChainUGen):
                    continue
                if source not in input_mapping:
                    input_mapping[source] = []
                input_mapping[source].append((ugen, i))
        return input_mapping

    @staticmethod
    def _cleanup_local_bufs(ugens):
        import supriya.ugens

        local_bufs = []
        processed_ugens = []
        for ugen in ugens:
            if isinstance(ugen, supriya.ugens.MaxLocalBufs):
                continue
            if isinstance(ugen, supriya.ugens.LocalBuf):
                local_bufs.append(ugen)
            processed_ugens.append(ugen)
        if local_bufs:
            max_local_bufs = supriya.ugens.MaxLocalBufs(len(local_bufs))
            for local_buf in local_bufs:
                inputs = list(local_buf.inputs[:2])
                inputs.append(max_local_bufs[0])
                local_buf._inputs = tuple(inputs)
            index = processed_ugens.index(local_bufs[0])
            processed_ugens[index:index] = [max_local_bufs]
        return tuple(processed_ugens)

    @staticmethod
    def _cleanup_pv_chains(ugens):
        import supriya.ugens

        input_mapping = SynthDef._build_input_mapping(ugens)
        for antecedent, descendants in input_mapping.items():
            if len(descendants) == 1:
                continue
            for descendant, input_index in descendants[:-1]:
                fft_size = antecedent.fft_size
                new_buffer = supriya.ugens.LocalBuf(fft_size)
                pv_copy = supriya.ugens.PV_Copy(antecedent, new_buffer)
                inputs = list(descendant._inputs)
                inputs[input_index] = pv_copy[0]
                descendant._inputs = tuple(inputs)
                index = ugens.index(descendant)
                replacement = []
                if isinstance(fft_size, UGenMethodMixin):
                    replacement.append(fft_size)
                replacement.extend([new_buffer, pv_copy])
                ugens[index:index] = replacement
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
        control_ugens = tuple(_ for _ in ugens if isinstance(_, Control))
        return control_ugens

    @staticmethod
    def _collect_indexed_parameters(control_ugens, parameter_names=None):
        indexed_parameters = []
        parameters = {}
        for control_ugen in control_ugens:
            index = control_ugen.starting_control_index
            for parameter in control_ugen.parameters:
                parameters[parameter.name] = (index, parameter)
                index += len(parameter)
        parameter_names = parameter_names or sorted(parameters)
        for parameter_name in parameter_names:
            indexed_parameters.append(parameters[parameter_name])
        indexed_parameters = tuple(indexed_parameters)
        return indexed_parameters

    @staticmethod
    def _extract_parameters(ugens):
        parameters = set()
        for ugen in ugens:
            if isinstance(ugen, Parameter):
                parameters.add(ugen)
        ugens = tuple(ugen for ugen in ugens if ugen not in parameters)
        parameters = tuple(sorted(parameters, key=lambda x: x.name))
        return ugens, parameters

    @staticmethod
    def _initialize_topological_sort(ugens):
        ugens = list(ugens)
        sort_bundles = collections.OrderedDict()
        width_first_antecedents = []
        for ugen in ugens:
            sort_bundles[ugen] = UGenSortBundle(ugen, width_first_antecedents)
            if isinstance(ugen, WidthFirstUGen):
                width_first_antecedents.append(ugen)
        for ugen in ugens:
            sort_bundle = sort_bundles[ugen]
            sort_bundle._initialize_topological_sort(sort_bundles)
            sort_bundle.descendants[:] = sorted(
                sort_bundles[ugen].descendants, key=lambda x: ugens.index(ugen)
            )
        return sort_bundles

    @staticmethod
    def _optimize_ugen_graph(ugens):
        sort_bundles = SynthDef._initialize_topological_sort(ugens)
        for ugen in ugens:
            ugen._optimize_graph(sort_bundles)
        return tuple(sort_bundles)

    def _register_with_local_server(self, server):
        synthdef_name = self.actual_name
        server._synthdefs[synthdef_name] = self

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
                available_ugens, out_stack, sort_bundles
            )
        return out_stack

    ### PUBLIC METHODS ###

    def allocate(self, server):
        self._allocate_synthdefs((self,), server)
        return self

    def compile(self, use_anonymous_name=False):
        from supriya.synthdefs import SynthDefCompiler

        synthdefs = [self]
        result = SynthDefCompiler.compile_synthdefs(
            synthdefs, use_anonymous_names=use_anonymous_name
        )
        return result

    def free(self, server):
        import supriya.commands

        assert self in server
        synthdef_name = self.actual_name
        del server._synthdefs[synthdef_name]
        request = supriya.commands.SynthDefFreeRequest(synthdef=self)
        if server.is_running:
            request.communicate(server=server)

    def to_dict(self):
        """
        Convert SynthDef to JSON-serializable dictionay.

        ::

            >>> import json
            >>> result = supriya.assets.synthdefs.default.to_dict()
            >>> result = json.dumps(
            ...     result,
            ...     indent=4,
            ...     separators=(",", ": "),
            ...     sort_keys=True,
            ... )
            >>> print(result)
            {
                "synthdef": {
                    "hash": "da0982184cc8fa54cf9d288a0fe1f6ca",
                    "name": "default",
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
            "name": self.actual_name,
            "hash": self.anonymous_name,
            "parameters": {},
        }
        for parameter_name, parameter in self.parameters.items():
            range_ = [0, 1]
            if parameter.range_:
                range_ = [parameter.range_.minimum, parameter.range_.maximum]
            rate = parameter.parameter_rate.name.lower()
            result["parameters"][parameter_name] = {
                "rate": rate,
                "range": range_,
                "unit": parameter.unit,
                "value": parameter.value,
            }
        result = {"synthdef": result}
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
        return max(self.audio_input_channel_count, self.audio_output_channel_count)

    @property
    def audio_input_channel_count(self):
        """
        Gets audio input channel count of synthdef.

        ::

            >>> with supriya.SynthDefBuilder() as builder:
            ...     audio_in = supriya.ugens.In.ar(channel_count=1)
            ...     control_in = supriya.ugens.In.kr(channel_count=2)
            ...     sin = supriya.ugens.SinOsc.ar(
            ...         frequency=audio_in,
            ...     )
            ...     source = audio_in * control_in[1]
            ...     audio_out = supriya.ugens.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()

        ::

            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.audio_input_channel_count
            1

        Returns integer.
        """
        ugens = tuple(
            _ for _ in self.input_ugens if _.calculation_rate == CalculationRate.AUDIO
        )
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

            >>> with supriya.SynthDefBuilder() as builder:
            ...     audio_in = supriya.ugens.In.ar(channel_count=1)
            ...     control_in = supriya.ugens.In.kr(channel_count=2)
            ...     sin = supriya.ugens.SinOsc.ar(
            ...         frequency=audio_in,
            ...     )
            ...     source = audio_in * control_in[1]
            ...     audio_out = supriya.ugens.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()

        ::

            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.audio_output_channel_count
            4

        Returns integer.
        """
        ugens = tuple(
            _ for _ in self.output_ugens if _.calculation_rate == CalculationRate.AUDIO
        )
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
        return max(self.control_input_channel_count, self.control_output_channel_count)

    @property
    def control_input_channel_count(self):
        """
        Gets control input channel count of synthdef.

        ::

            >>> with supriya.SynthDefBuilder() as builder:
            ...     audio_in = supriya.ugens.In.ar(channel_count=1)
            ...     control_in = supriya.ugens.In.kr(channel_count=2)
            ...     sin = supriya.ugens.SinOsc.ar(
            ...         frequency=audio_in,
            ...     )
            ...     source = audio_in * control_in[1]
            ...     audio_out = supriya.ugens.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()

        ::

            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.control_input_channel_count
            2

        Returns integer.
        """
        ugens = tuple(
            _ for _ in self.input_ugens if _.calculation_rate == CalculationRate.CONTROL
        )
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

            >>> with supriya.SynthDefBuilder() as builder:
            ...     audio_in = supriya.ugens.In.ar(channel_count=1)
            ...     control_in = supriya.ugens.In.kr(channel_count=2)
            ...     sin = supriya.ugens.SinOsc.ar(
            ...         frequency=audio_in,
            ...     )
            ...     source = audio_in * control_in[1]
            ...     audio_out = supriya.ugens.Out.ar(source=[source] * 4)
            ...
            >>> synthdef = builder.build()

        ::

            >>> supriya.graph(synthdef)  # doctest: +SKIP

        ::

            >>> synthdef.control_output_channel_count
            0

        Returns integer.
        """
        ugens = tuple(
            _
            for _ in self.output_ugens
            if _.calculation_rate == CalculationRate.CONTROL
        )
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
        return "gate" in self.parameter_names

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
        return {
            parameter.name: parameter for index, parameter in self.indexed_parameters
        }

    @property
    def parameter_names(self):
        return [parameter.name for index, parameter in self.indexed_parameters]

    @property
    def ugens(self):
        return self._ugens


class UGenSortBundle(SupriyaObject):

    ### INITIALIZER ###

    def __init__(self, ugen, width_first_antecedents):
        self.antecedents = []
        self.descendants = []
        self.ugen = ugen
        self.width_first_antecedents = tuple(width_first_antecedents)

    ### PRIVATE METHODS ###

    def _initialize_topological_sort(self, sort_bundles):
        for input_ in self.ugen.inputs:
            if isinstance(input_, OutputProxy):
                input_ = input_.source
            elif not isinstance(input_, UGen):
                continue
            input_sort_bundle = sort_bundles[input_]
            if input_ not in self.antecedents:
                self.antecedents.append(input_)
            if self.ugen not in input_sort_bundle.descendants:
                input_sort_bundle.descendants.append(self.ugen)
        for input_ in self.width_first_antecedents:
            input_sort_bundle = sort_bundles[input_]
            if input_ not in self.antecedents:
                self.antecedents.append(input_)
            if self.ugen not in input_sort_bundle.descendants:
                input_sort_bundle.descendants.append(self.ugen)

    def _make_available(self, available_ugens):
        if not self.antecedents:
            if self.ugen not in available_ugens:
                available_ugens.append(self.ugen)

    def _schedule(self, available_ugens, out_stack, sort_bundles):
        for ugen in reversed(self.descendants):
            sort_bundle = sort_bundles[ugen]
            sort_bundle.antecedents.remove(self.ugen)
            sort_bundle._make_available(available_ugens)
        out_stack.append(self.ugen)

    ### PUBLIC METHODS ###

    def clear(self):
        self.antecedents[:] = []
        self.descendants[:] = []
        self.width_first_antecedents[:] = []


class SuperColliderSynthDef(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = ("_body", "_name", "_rates")

    ### INITIALIZER ###

    def __init__(self, name, body, rates=None):
        self._name = name
        self._body = body
        self._rates = rates

    ### PRIVATE METHODS ###

    def _build_sc_input(self, directory_path):
        input_ = []
        input_.append("a = SynthDef(")
        input_.append("    \\{}, {{".format(self.name))
        for line in self.body.splitlines():
            input_.append("    " + line)
        if self.rates:
            input_.append("}}, {});".format(self.rates))
        else:
            input_.append("});")
        input_.append('"Defined SynthDef".postln;')
        input_.append('a.writeDefFile("{}");'.format(directory_path))
        input_.append('"Wrote SynthDef".postln;')
        input_.append("0.exit;")
        input_ = "\n".join(input_)
        return input_

    ### PUBLIC METHODS ###

    def compile(self):
        sclang_path = sclang.find()
        with tempfile.TemporaryDirectory() as directory:
            directory_path = pathlib.Path(directory)
            sc_input = self._build_sc_input(directory_path)
            print(sc_input)
            sc_file_path = directory_path / f"{self.name}.sc"
            sc_file_path.write_text(sc_input)
            command = " ".join([str(sclang_path), "-D", str(sc_file_path)])
            print(command)
            subprocess.run(command, shell=True)
            result = (directory_path / f"{self.name}.scsyndef").read_bytes()
        return bytes(result)

    ### PUBLIC PROPERTIES ###

    @property
    def body(self):
        return self._body

    @property
    def rates(self):
        return self._rates

    @property
    def name(self):
        return self._name
