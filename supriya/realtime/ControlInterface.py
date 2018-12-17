import abc
import re

from supriya.system.SupriyaObject import SupriyaObject


class ControlInterface(SupriyaObject):

    # TODO: This should inherit from collections.Mapping

    ### CLASS VARIABLES ###

    __documentation_section__ = "Server Internals"

    __slots__ = ("_synth_controls", "_client")

    _bus_pattern = re.compile(r"(?P<type>c|a)(?P<id>\d+)")

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
        import supriya.commands
        import supriya.realtime
        import supriya.synthdefs

        n_set_settings = {}
        n_map_settings = {}
        n_mapa_settings = {}
        for control_name, value in settings.items():
            if control_name not in self:
                continue
            control = self[control_name]
            if isinstance(value, str):
                match = self._bus_pattern.match(value)
                if match:
                    group_dict = match.groupdict()
                    if group_dict["type"] == "c":
                        calculation_rate = "control"
                    else:
                        calculation_rate = "audio"
                    value = supriya.realtime.Bus(
                        bus_group_or_index=int(group_dict["id"]),
                        calculation_rate=calculation_rate,
                    ).allocate()
            if isinstance(value, (int, float)):
                n_set_settings[control_name] = float(value)
                control._set_to_number(value)
            elif isinstance(value, (supriya.realtime.Bus, supriya.realtime.BusGroup)):
                value_rate = value.calculation_rate
                if (
                    isinstance(self.client, supriya.realtime.Synth)
                    and not self.client.is_allocated
                    and control.calculation_rate == supriya.CalculationRate.SCALAR
                ):
                    control._set_to_number(int(value))
                elif value_rate == supriya.CalculationRate.CONTROL:
                    n_map_settings[control_name] = value
                    control._map_to_bus(value)
                elif value_rate == supriya.CalculationRate.AUDIO:
                    n_mapa_settings[control_name] = value
                    control._map_to_bus(value)
            elif value is None:
                n_map_settings[control_name] = -1
                control._unmap()
            else:
                raise ValueError(value)
        requests = []
        if self.client.is_allocated:
            if n_set_settings:
                request = supriya.commands.NodeSetRequest(
                    self.node_id, **n_set_settings
                )
                requests.append(request)
            if n_map_settings:
                request = supriya.commands.NodeMapToControlBusRequest(
                    self.node_id, **n_map_settings
                )
                requests.append(request)
            if n_mapa_settings:
                request = supriya.commands.NodeMapToAudioBusRequest(
                    self.node_id, **n_mapa_settings
                )
                requests.append(request)
        return tuple(requests)

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
