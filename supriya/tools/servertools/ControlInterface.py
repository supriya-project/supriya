# -*- encoding: utf-8 -*-
import abc
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class ControlInterface(SupriyaObject):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_synth_controls',
        '_client',
        )

    ### SPECIAL METHODS ###

    def __iter__(self):
        return iter(self._synth_controls)

    def __len__(self):
        return len(self._synth_controls)

    @abc.abstractmethod
    def __setitem__(self, items, values):
        raise NotImplementedError

    ### PRIVATE METHODS ###

    def _set(self, **settings):
        from supriya.tools import requesttools
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        n_set_settings = {}
        n_map_settings = {}
        n_mapa_settings = {}
        for control_name, value in settings.items():
            control = self[control_name]
            if isinstance(value, (int, float)):
                n_set_settings[control_name] = value
                control._set_to_number(value)
            elif isinstance(value, servertools.Bus):
                if value.calculation_rate == synthdeftools.CalculationRate.CONTROL:
                    n_map_settings[control_name] = value
                else:
                    n_mapa_settings[control_name] = value
                control._map_to_bus(value)
            elif value is None:
                n_map_settings[control_name] = -1
                control._unmap()
            else:
                raise ValueError(value)
        messages = []
        if self.client.is_allocated:
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
        return tuple(messages)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def as_dict(self):
        raise NotImplementedError

    @abc.abstractmethod
    def reset(self):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def node_id(self):
        return int(self.client)
