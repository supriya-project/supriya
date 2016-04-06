# -*- encoding: utf-8 -*-
import collections
from supriya.tools.servertools.ControlInterface import ControlInterface


class SynthInterface(ControlInterface):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_synthdef',
        '_synth_control_map',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        synthdef=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        self._client = client
        synth_controls = []
        synth_control_map = collections.OrderedDict()
        if synthdef is not None:
            assert isinstance(synthdef, synthdeftools.SynthDef)
            for index, parameter in synthdef.indexed_parameters:
                synth_control = servertools.SynthControl.from_parameter(
                    parameter,
                    client=self,
                    index=index,
                    )
                synth_controls.append(synth_control)
                synth_control_map[synth_control.name] = synth_control
            self._synth_controls = tuple(synth_controls)
        self._synth_control_map = synth_control_map
        self._synthdef = synthdef or self._client.synthdef

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        if isinstance(item, str):
            return item in self._synth_control_map
        return False

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self._synth_controls[item]
        elif isinstance(item, str):
            return self._synth_control_map[item]
        elif isinstance(item, tuple):
            result = []
            for x in item:
                result.append(self.__getitem__(x))
            return tuple(result)
        return ValueError(item)

    def __setitem__(self, items, values):
        from supriya.tools import servertools
        if not isinstance(items, tuple):
            items = (items,)
        if not isinstance(values, tuple):
            values = (values,)
        assert len(items) == len(values)
        synth_controls = self.__getitem__(items)
        synth_control_names = [x.name for x in synth_controls]
        settings = dict(zip(synth_control_names, values))
        messages = self._set(**settings)
        if self.client.is_allocated:
            message_bundler = servertools.MessageBundler(
                server=self.client.server,
                sync=False,
                )
            with message_bundler:
                message_bundler.add_messages(messages)

    def __str__(self):
        result = []
        string = '{}: ({})'.format(
            repr(self.client),
            self.synthdef.actual_name,
            )
        result.append(string)
        maximum_length = 0
        for synth_control in self:
            maximum_length = max(maximum_length, len(synth_control.name))
        maximum_length += 1
        for synth_control in sorted(self):
            name = synth_control.name
            value = str(synth_control.value)
            spacing = ' ' * (maximum_length - len(name))
            string = '    ({}) {}:{}{}'.format(
                synth_control.calculation_rate.token,
                name,
                spacing,
                value,
                )
            if synth_control.is_bound:
                string += ' (bound)'
            result.append(string)
        result = '\n'.join(result)
        return result

    ### PRIVATE METHODS ###

    def _make_synth_new_settings(self):
        from supriya.tools import requesttools
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        audio_map = {}
        control_map = {}
        node_id = self.client.node_id
        requests = []
        settings = {}
        for synth_control in self.synth_controls:
            if isinstance(synth_control.value, servertools.Bus):
                if synth_control.value.calculation_rate == synthdeftools.CalculationRate.AUDIO:
                    audio_map[synth_control.name] = synth_control.value
                else:
                    control_map[synth_control.name] = synth_control.value
            elif synth_control.value != synth_control.default_value:
                settings[synth_control.name] = synth_control.value
        if audio_map:
            request = requesttools.NodeMapToAudioBusRequest(
                node_id=node_id,
                **audio_map
                )
            requests.append(request)
        if control_map:
            request = requesttools.NodeMapToControlBusRequest(
                node_id=node_id,
                **control_map
                )
            requests.append(request)
        return settings, requests

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_bracketed=True,
            positional_argument_values=self._synth_controls,
            keyword_argument_names=(),
            )

    ### PUBLIC METHODS ###

    def as_dict(self):
        result = {}
        if self.client.register_controls is None or \
            self.client.register_controls:
            for control in self:
                result[control.name] = set([self.client])
        return result

    def reset(self):
        for synth_control in self._synth_controls:
            synth_control.reset()

    ### PUBLIC PROPERTIES ###

    @property
    def synthdef(self):
        return self._synthdef

    @property
    def synth_controls(self):
        return self._synth_controls
