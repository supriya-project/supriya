# -*- encoding: utf-8 -*-
import collections
import copy
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
        '_parameter_names',
        '_parameters',
        '_ugens',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        ugens,
        ):
        ugens = copy.deepcopy(ugens)
        ugens = self._flatten_ugens(ugens)
        ugens = self._optimize_ugen_graph(ugens)
        ugens, control_proxies = self._extract_control_proxies(ugens)
        control_ugens, control_mapping = self._collect_controls(
            control_proxies,
            )
        self._remap_controls(ugens, control_mapping)
        ugens.update(control_ugens)
        ugens = self._sort_ugens_topologically(ugens)
        self._ugens = tuple(ugens)
        self._constants = self._collect_constants(self._ugens)

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
    def _collect_controls(control_proxies):
        from supriya.tools import synthdeftools
        from supriya.tools import ugentools
        control_mapping = collections.OrderedDict()
        scalar_control_proxies = []
        trigger_control_proxies = []
        audio_control_proxies = []
        control_control_proxies = []
        mapping = {
            synthdeftools.ControlRate.AUDIO: audio_control_proxies,
            synthdeftools.ControlRate.CONTROL: control_control_proxies,
            synthdeftools.ControlRate.SCALAR: scalar_control_proxies,
            synthdeftools.ControlRate.TRIGGER: trigger_control_proxies,
            }
        for control_proxy in control_proxies:
            mapping[control_proxy.control_rate].append(control_proxy)
        for control_proxies in mapping.values():
            control_proxies.sort(key=lambda x: x.name)
        control_ugens = []
        starting_control_index = 0
        if scalar_control_proxies:
            control = ugentools.Control(
                control_names=scalar_control_proxies,
                rate=synthdeftools.Rate.SCALAR,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            starting_control_index += len(scalar_control_proxies)
            for i, control_proxy in enumerate(scalar_control_proxies):
                control_mapping[control_proxy] = control[i]
        if trigger_control_proxies:
            control = ugentools.TrigControl(
                control_names=trigger_control_proxies,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            starting_control_index += len(trigger_control_proxies)
            for i, control_proxy in enumerate(trigger_control_proxies):
                control_mapping[control_proxy] = control[i]
        if audio_control_proxies:
            control = ugentools.AudioControl(
                control_names=audio_control_proxies,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            starting_control_index += len(audio_control_proxies)
            for i, control_proxy in enumerate(audio_control_proxies):
                control_mapping[control_proxy] = control[i]
        if control_control_proxies:
            control = ugentools.Control(
                control_names=control_control_proxies,
                rate=synthdeftools.Rate.CONTROL,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            starting_control_index += len(control_control_proxies)
            for i, control_proxy in enumerate(control_control_proxies):
                control_mapping[control_proxy] = control[i]
        return control_ugens, control_mapping

    def _collect_parameters(self, controls):
        pass

    @staticmethod
    def _extract_control_proxies(ugens):
        from supriya.tools import synthdeftools
        control_proxies = set()
        for ugen in ugens:
            if isinstance(ugen, synthdeftools.Parameter):
                control_proxies.add(ugen)
        ugens = ugens.difference(control_proxies)
        return ugens, control_proxies

    @staticmethod
    def _flatten_ugens(ugens):
        def recurse(ugen):
            flattened_ugens.add(ugen)
            for input_ in ugen.inputs:
                if isinstance(input_, synthdeftools.Parameter):
                    flattened_ugens.add(input_)
                elif isinstance(input_, synthdeftools.OutputProxy):
                    flattened_ugens.add(input_.source)
                    recurse(input_.source)
                elif isinstance(input_, synthdeftools.UGen):
                    flattened_ugens.add(input_)
                    recurse(input_)
        from supriya.tools import synthdeftools
        flattened_ugens = set()
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
