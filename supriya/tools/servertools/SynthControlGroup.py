# -*- encoding: utf-8 -*-
import collections
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class SynthControlGroup(SupriyaObject, collections.Mapping):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        '_synthdef',
        '_synth_controls',
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
            for parameter in synthdef.parameters:
                synth_control = servertools.SynthControl.from_parameter(
                    parameter,
                    client=self,
                    )
                synth_controls.append(synth_control)
                synth_control_map[synth_control.name] = synth_control
            self._synth_controls = tuple(synth_controls)
        self._synth_control_map = synth_control_map

    ### SPECIAL METHODS ###

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

    def __iter__(self):
        return iter(self._synth_controls)

    def __len__(self):
        return len(self._synth_controls)

    def __setitem__(self, items, values):
        if not isinstance(items, tuple):
            items = (items,)
        if not isinstance(values, tuple):
            values = (values,)
        assert len(items) == len(values)
        synth_controls = self.__getitem__(items)
        synth_control_names = [x.name for x in synth_controls]
        settings = dict(zip(synth_control_names, values))
        self._set(**settings)

    ### PRIVATE METHODS ###

    def _set(self, **settings):
        from supriya.tools import requesttools
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        n_set_settings = {}
        n_map_settings = {}
        n_mapa_settings = {}
        for synth_control_name, value in settings.items():
            if isinstance(value, (int, float)):
                n_set_settings[synth_control_name] = value
            elif isinstance(value, servertools.Bus):
                if value.rate == synthdeftools.Rate.CONTROL:
                    n_map_settings[synth_control_name] = value
                else:
                    n_mapa_settings[synth_control_name] = value
            else:
                raise ValueError(value)
            self[synth_control_name]._value = value
        messages = []
        if n_set_settings:
            request = requesttools.NodeSetRequest(
                self.node_id,
                **n_set_settings
                )
            message = request.to_osc_message()
            messages.append(message)
        if n_map_settings:
            request = requesttools.NodeMapToControlBusRequest(
                self.node_id,
                **n_map_settings
                )
            message = request.to_osc_message()
            messages.append(message)
        if n_mapa_settings:
            request = requesttools.NodeMapToAudioBusRequest(
                self.node_id,
                **n_mapa_settings
                )
            message = request.to_osc_message()
            messages.append(message)
        for message in messages:
            self.client.server.send_message(message)

    ### PUBLIC METHODS ###

    def reset(self):
        for synth_control in self._synth_controls:
            synth_control.reset()

    def set(self, **kwargs):
        self._set(
            **kwargs
            )

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def node_id(self):
        return int(self.client)

    @property
    def synthdef(self):
        return self._synthdef