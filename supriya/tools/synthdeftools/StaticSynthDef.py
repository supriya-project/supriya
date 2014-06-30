# -*- encoding: utf-8 -*-
import collections
import copy
import hashlib
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class StaticSynthDef(SupriyaObject):
    r'''A synth definition.

    ::

        >>> from supriya.tools import synthdeftools
        >>> from supriya.tools import ugentools
        >>> builder = synthdeftools.SynthDefBuilder(frequency=440)
        >>> sin_osc = ugentools.SinOsc.ar(frequency=builder['frequency'])
        >>> out = ugentools.Out.ar(bus=0, source=sin_osc)
        >>> builder.add_ugen(out)
        >>> synthdef = builder.build()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_compiled_ugen_graph',
        '_constants',
        '_name',
        '_parameters',
        '_ugens',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ugens,
        name=None,
        ):
        from supriya.tools import synthdeftools
        compiler = synthdeftools.SynthDefCompiler
        self._name = name
        ugens = copy.deepcopy(ugens)
        ugens = self._flatten_ugens(ugens)
        ugens = self._optimize_ugen_graph(ugens)
        ugens, parameters = self._extract_parameters(ugens)
        control_ugens, control_mapping = self._collect_controls(
            parameters,
            )
        self._parameters = tuple(control_mapping.keys())
        self._remap_controls(ugens, control_mapping)
        ugens = control_ugens + ugens
        ugens = self._sort_ugens_topologically(ugens)
        self._ugens = tuple(ugens)
        self._constants = self._collect_constants(self._ugens)
        self._compiled_ugen_graph = compiler.compile_ugen_graph(self)

    ### PRIVATE METHODS ###

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
    def _collect_controls(parameters):
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
        for parameters in mapping.values():
            parameters.sort(key=lambda x: x.name)
        control_ugens = []
        starting_control_index = 0
        if scalar_parameters:
            control = ugentools.Control(
                control_names=scalar_parameters,
                rate=synthdeftools.Rate.SCALAR,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            starting_control_index += len(scalar_parameters)
            for i, parameter in enumerate(scalar_parameters):
                control_mapping[parameter] = control[i]
        if trigger_parameters:
            control = ugentools.TrigControl(
                control_names=trigger_parameters,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            starting_control_index += len(trigger_parameters)
            for i, parameter in enumerate(trigger_parameters):
                control_mapping[parameter] = control[i]
        if audio_parameters:
            control = ugentools.AudioControl(
                control_names=audio_parameters,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            starting_control_index += len(audio_parameters)
            for i, parameter in enumerate(audio_parameters):
                control_mapping[parameter] = control[i]
        if control_parameters:
            control = ugentools.Control(
                control_names=control_parameters,
                rate=synthdeftools.Rate.CONTROL,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            starting_control_index += len(control_parameters)
            for i, parameter in enumerate(control_parameters):
                control_mapping[parameter] = control[i]
        control_ugens = tuple(control_ugens)
        return control_ugens, control_mapping

    def _collect_parameters(self, controls):
        pass

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
            flattened_ugens.append(ugen)
            if isinstance(ugen, synthdeftools.Parameter):
                return
            for input_ in ugen.inputs:
                if isinstance(input_, synthdeftools.Parameter):
                    if input_ not in flattened_ugens:
                        flattened_ugens.append(input_)
                elif isinstance(input_, synthdeftools.OutputProxy):
                    if input_.source not in flattened_ugens:
                        flattened_ugens.append(input_.source)
                        recurse(input_.source)
                elif isinstance(input_, synthdeftools.UGen):
                    if input_ not in flattened_ugens:
                        flattened_ugens.append(input_)
                        recurse(input_)
        from supriya.tools import synthdeftools
        flattened_ugens = []
        for ugen in ugens:
            recurse(ugen)
        return flattened_ugens

    @staticmethod
    def _optimize_ugen_graph(ugens):
        return ugens

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
        from supriya.tools import synthdeftools
        ugens = list(ugens)
        available_ugens = []
        sort_bundles = {}
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
        return out_stack

    ### PUBLIC METHODS ###

    def compile(self):
        from supriya.tools.synthdeftools import SynthDefCompiler
        synthdefs = [self]
        result = SynthDefCompiler.compile_synthdefs(synthdefs)
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
    def constants(self):
        return self._constants

    @property
    def name(self):
        return self._name

    @property
    def parameters(self):
        return self._parameters

    @property
    def ugens(self):
        return self._ugens
