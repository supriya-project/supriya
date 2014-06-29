# -*- encoding: utf-8 -*-
import collections
import copy
from supriya.tools.servertools.ServerObjectProxy import ServerObjectProxy


class StaticSynthDef(ServerObjectProxy):

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
        ugens, control_proxies = self._extract_control_proxies(ugens)
        control_ugens, control_mapping = self._collect_controls(
            control_proxies,
            )
        ugens = self._remap_controls(ugens, control_mapping)
        ugens = self._optimize_ugen_graph(ugens)
        ugens = self._sort_ugens_topologically(ugens)
        self._ugens = ugens

    ### PRIVATE METHODS ###

    def _collect_constants(self, ugens):
        pass

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
            synthdeftools.Rate.AUDIO: audio_control_proxies,
            synthdeftools.Rate.CONTROL: control_control_proxies,
            synthdeftools.Rate.SCALAR: scalar_control_proxies,
            synthdeftools.Rate.TRIGGER: trigger_control_proxies,
            }
        for control_proxy in control_proxies:
            mapping[control_proxy.rate].add(control_proxy)
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
            for i, control_proxy in scalar_control_proxies:
                control_mapping[control_proxy] = control[i]
        if trigger_control_proxies:
            control = ugentools.TrigControl(
                control_names=trigger_control_proxies,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            starting_control_index += len(trigger_control_proxies)
            for i, control_proxy in trigger_control_proxies:
                control_mapping[control_proxy] = control[i]
        if audio_control_proxies:
            control = ugentools.AudioControl(
                control_names=audio_control_proxies,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            starting_control_index += len(audio_control_proxies)
            for i, control_proxy in audio_control_proxies:
                control_mapping[control_proxy] = control[i]
        if control_control_proxies:
            control = ugentools.Control(
                control_names=control_control_proxies,
                starting_control_index=starting_control_index,
                )
            control_ugens.append(control)
            starting_control_index += len(control_control_proxies)
            for i, control_proxy in control_control_proxies:
                control_mapping[control_proxy] = control[i]
        return control_ugens, control_mapping

    def _collect_parameters(self, controls):
        pass

    @staticmethod
    def _extract_control_proxies(ugens):
        from supriya.tools import synthdeftools
        control_proxies = set()
        for ugen in ugens:
            if isinstance(ugen, synthdeftools.SynthDefControl):
                control_proxies.add(ugen)
        ugens = ugens.difference(control_proxies)
        return ugens

    @staticmethod
    def _flatten_ugens(ugens):
        def recurse(ugen):
            for input_ in ugen.inputs:
                if isinstance(input_, synthdeftools.SynthDefControl):
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

    def _optimize_ugen_graph(ugens):
        pass

    def _remap_controls(ugens, control_mapping):
        for ugen in ugens:
            inputs = list(ugen.inputs)
            for i, input_ in enumerate(inputs):
                if input_ in control_mapping:
                    output_proxy = control_mapping[input_]
                    inputs[i] = output_proxy
            ugen._inputs = tuple(inputs)

    def _sort_ugens_topologically(ugens):
        pass
