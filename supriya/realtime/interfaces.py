import abc
import collections
import copy
import re
from collections.abc import Iterable

from supriya.system import SupriyaObject


class ControlInterface(SupriyaObject):

    # TODO: This should inherit from collections.Mapping

    ### CLASS VARIABLES ###

    __slots__ = ("_synth_controls", "_client")

    _bus_pattern = re.compile(r"(?P<type>c|a)(?P<id>\d+)")

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __setitem__(self, items, values):
        raise NotImplementedError

    ### PRIVATE METHODS ###

    def _set(self, **settings):
        # TODO: Reimplement as _apply_local() on request classes
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
                    )
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
                try:
                    control._set_to_number(float(value))
                except TypeError:
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
    def reset(self):
        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def node_id(self):
        return int(self.client)


class GroupControl:

    ### CLASS VARIABLES ###

    __slots__ = ("_client", "_name")

    ### INITIALIZER ###

    def __init__(self, client=None, name=None):
        self._client = client
        self._name = str(name)

    ### SPECIAL METHODS ###

    def __repr__(self):
        class_name = type(self).__name__
        calculation_rates = sorted(
            set(
                synth.controls[self.name].calculation_rate
                for synth in self.client._synth_controls["amplitude"]
            )
        )
        return '<{}: {!r} "{}" [{}]>'.format(
            class_name,
            self.client.client,
            self.name,
            ", ".join(_.token for _ in calculation_rates),
        )

    def __str__(self):
        return self.name

    ### PRIVATE METHODS ###

    def _map_to_bus(self, bus):
        pass

    def _set_to_number(self, number):
        pass

    def _unmap(self):
        pass

    ### PUBLIC METHODS ###

    def set(self, expr):
        self._client[self.name] = expr

    ### PUBLIC PROPERTIES ###

    @property
    def client(self):
        return self._client

    @property
    def group(self):
        return self.client.client

    @property
    def name(self):
        return self._name

    @property
    def node(self):
        return self.client.client


class GroupInterface(ControlInterface):
    """
    Interface to group controls.

    ::

        >>> server = supriya.Server().boot()
        >>> group = supriya.Group().allocate(server)
        >>> group.extend(
        ...     [
        ...         supriya.Synth(synthdef=supriya.assets.synthdefs.test),
        ...         supriya.Synth(synthdef=supriya.assets.synthdefs.default),
        ...         supriya.Synth(synthdef=supriya.assets.synthdefs.default),
        ...     ]
        ... )

    ::

        >>> control = group.controls["amplitude"]

    ::

        >>> group.controls["frequency"] = 777

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_group_controls",)

    ### INITIALIZER ###

    def __init__(self, client=None):
        self._synth_controls = {}
        self._group_controls = {}
        self._client = client

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        return item in self._synth_controls

    def __getitem__(self, item):
        return self._group_controls[item]

    def __iter__(self):
        return iter(sorted(self._group_controls))

    def __len__(self):
        return len(self._group_controls)

    def __repr__(self):
        class_name = type(self).__name__
        return "<{}: {!r}>".format(class_name, self.client)

    def __setitem__(self, items, values):
        import supriya.realtime

        if not isinstance(items, tuple):
            items = (items,)
        assert all(_ in self._synth_controls for _ in items)
        if not isinstance(values, tuple):
            values = (values,)
        assert len(items) == len(values)
        settings = dict(zip(items, values))
        for key, value in settings.items():
            for synth in self._synth_controls.get(key, ()):
                control = synth.controls[key]
                if isinstance(value, supriya.realtime.Bus):
                    control._map_to_bus(value)
                elif value is None:
                    control._unmap()
                else:
                    control._set_to_number(value)
        requests = self._set(**settings)
        supriya.commands.RequestBundle(contents=requests).communicate(
            server=self.client.server, sync=True
        )

    ### PUBLIC METHODS ###

    def add_controls(self, control_interface_dict):
        import supriya.realtime

        for control_name in control_interface_dict:
            if control_name not in self._synth_controls:
                self._synth_controls[control_name] = copy.copy(
                    control_interface_dict[control_name]
                )
                proxy = supriya.realtime.GroupControl(client=self, name=control_name)
                self._group_controls[control_name] = proxy
            else:
                self._synth_controls[control_name].update(
                    control_interface_dict[control_name]
                )

    def as_dict(self):
        result = {}
        for control_name, node_set in self._synth_controls.items():
            result[control_name] = copy.copy(node_set)
        return result

    def remove_controls(self, control_interface_dict):
        for control_name in control_interface_dict:
            if control_name not in self._synth_controls:
                continue
            current_nodes = self._synth_controls[control_name]
            nodes_to_remove = control_interface_dict[control_name]
            current_nodes.difference_update(nodes_to_remove)
            if not current_nodes:
                del self._synth_controls[control_name]
                del self._group_controls[control_name]

    def reset(self):
        self._synth_controls.clear()


class SynthControl:

    ### CLASS VARIABLES ###

    __slots__ = (
        "_calculation_rate",
        "_client",
        "_index",
        "_default_value",
        "_last_unmapped_value",
        "_name",
        "_range",
        "_unit",
        "_value",
        "__weakref__",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        client=None,
        index=None,
        name=None,
        range_=None,
        calculation_rate=None,
        unit=None,
        value=None,
    ):
        import supriya.realtime
        import supriya.synthdefs

        self._client = client
        self._name = str(name)
        if isinstance(range_, supriya.synthdefs.Range):
            self._range = range_
        else:
            self._range = None
        self._calculation_rate = supriya.CalculationRate.from_expr(calculation_rate)
        self._unit = unit
        self._value = value
        self._default_value = value
        if not isinstance(value, supriya.realtime.Bus):
            self._last_unmapped_value = self._value
        else:
            self._last_unmapped_value = self._default_value
        if index is not None:
            index = int(index)
        self._index = index

    ### SPECIAL METHODS ###

    def __call__(self, expr):
        return self.set(expr)

    def __repr__(self):
        class_name = type(self).__name__
        return '<{}: {!r} "{}": {} [{}]>'.format(
            class_name,
            self.client.client,
            self.name,
            self.value,
            self.calculation_rate.token,
        )

    def __str__(self):
        return self.name

    ### PRIVATE METHODS ###

    def _map_to_bus(self, bus):
        import supriya.realtime

        if not isinstance(self.value, supriya.realtime.Bus):
            self._last_unmapped_value = self._value
        self._value = bus

    def _set_to_number(self, value):
        self._value = float(value)
        self._last_unmapped_value = self._value

    def _unmap(self):
        self._value = self._last_unmapped_value

    ### PUBLIC METHODS ###

    @classmethod
    def from_parameter(cls, parameter, index=0, client=None):
        import supriya.synthdefs

        assert isinstance(parameter, supriya.synthdefs.Parameter)
        name = parameter.name
        range_ = parameter.range_
        calculation_rate = supriya.CalculationRate.from_expr(parameter)
        unit = parameter.unit
        value = parameter.value
        synth_control = SynthControl(
            client=client,
            index=index,
            name=name,
            range_=range_,
            calculation_rate=calculation_rate,
            unit=unit,
            value=value,
        )
        return synth_control

    def get(self):
        return self._value

    def reset(self):
        self._value = self._default_value

    def set(self, expr):
        import supriya.commands
        import supriya.realtime
        import supriya.synthdefs

        if isinstance(expr, supriya.realtime.Bus):
            self._map_to_bus(expr)
            if expr.calculation_rate == supriya.CalculationRate.CONTROL:
                request = supriya.commands.NodeMapToControlBusRequest(
                    self.node, **{self.name: self._value}
                )
            else:
                request = supriya.commands.NodeMapToAudioBusRequest(
                    self.node, **{self.name: self._value}
                )
        elif expr is None:
            self._unmap()
            request = supriya.commands.NodeMapToControlBusRequest(
                self.node, **{self.name: -1}
            )
        else:
            self._set_to_number(expr)
            request = supriya.commands.NodeSetRequest(
                self.node, **{self.name: self._value}
            )
        if self.node.is_allocated:
            request.communicate(server=self.node.server)
        return self.get()

    ### PUBLIC PROPERTIES ###

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def client(self):
        return self._client

    @property
    def default_value(self):
        return self._default_value

    @property
    def index(self):
        return self._index

    @property
    def last_unmapped_value(self):
        return self._last_unmapped_value

    @property
    def name(self):
        return self._name

    @property
    def range_(self):
        return self._range

    @property
    def node(self):
        return self.client.client

    @property
    def synth(self):
        return self.client.client

    @property
    def unit(self):
        return self._unit

    @property
    def value(self):
        return self._value


class SynthInterface(ControlInterface):

    ### CLASS VARIABLES ###

    __slots__ = ("_synthdef", "_synth_control_map")

    ### INITIALIZER ###

    def __init__(self, client=None, synthdef=None):
        import supriya.realtime
        import supriya.synthdefs

        assert isinstance(synthdef, supriya.synthdefs.SynthDef)
        self._client = client
        synth_controls = []
        synth_control_map = collections.OrderedDict()
        for index, parameter in synthdef.indexed_parameters:
            synth_control = supriya.realtime.SynthControl.from_parameter(
                parameter, client=self, index=index
            )
            synth_controls.append(synth_control)
            synth_control_map[synth_control.name] = synth_control
        self._synth_controls = tuple(synth_controls)
        self._synth_control_map = synth_control_map
        self._synthdef = synthdef or self._client.synthdef

    ### SPECIAL METHODS ###

    def __contains__(self, item):
        return item in self._synth_control_map

    def __getitem__(self, item):
        if isinstance(item, str):
            return self._synth_control_map[item]
        elif isinstance(item, Iterable):
            return tuple(self._synth_control_map[x] for x in item)
        raise ValueError

    def __iter__(self):
        return iter(sorted(self._synth_control_map))

    def __len__(self):
        return len(self._synth_control_map)

    def __repr__(self):
        """
        Get interpreter representation of synth interface.

        ::

            >>> synth = supriya.Synth()
            >>> print(repr(synth.controls))
            <SynthInterface: <- Synth: ??? default>>

        """
        class_name = type(self).__name__
        return "<{}: {!r}>".format(class_name, self.client)

    def __setitem__(self, items, values):
        import supriya.realtime

        if not isinstance(items, tuple):
            items = (items,)
        if not isinstance(values, tuple):
            values = (values,)
        assert len(items) == len(values)
        synth_controls = self.__getitem__(items)
        synth_control_names = [x.name for x in synth_controls]
        settings = dict(zip(synth_control_names, values))
        requests = self._set(**settings)
        if not self.client.is_allocated:
            return
        supriya.commands.RequestBundle(contents=requests).communicate(
            server=self.client.server, sync=True
        )

    def __str__(self):
        """
        Get string representation of synth interface.

        ::

            >>> synth = supriya.Synth()
            >>> print(str(synth.controls))
            <- Synth: ??? default>:
                (kr) amplitude: 0.1
                (kr) frequency: 440.0
                (kr) gate:      1.0
                (ir) out:       0.0
                (kr) pan:       0.5

        """
        result = []
        string = "{!r}:".format(self.client)
        result.append(string)
        maximum_length = 0
        control_names = sorted(self)
        maximum_length = max(maximum_length, max(len(_) for _ in control_names))
        maximum_length += 1
        for control_name in control_names:
            synth_control = self[control_name]
            value = str(synth_control.value)
            spacing = " " * (maximum_length - len(control_name))
            string = "    ({}) {}:{}{}".format(
                synth_control.calculation_rate.token, control_name, spacing, value
            )
            result.append(string)
        result = "\n".join(result)
        return result

    ### PRIVATE METHODS ###

    def _make_synth_new_settings(self):
        import supriya.commands
        import supriya.realtime
        import supriya.synthdefs

        audio_map = {}
        control_map = {}
        requests = []
        settings = {}
        for synth_control in self.synth_controls:
            if isinstance(synth_control.value, supriya.realtime.Bus):
                if (
                    synth_control.value.calculation_rate
                    == supriya.CalculationRate.AUDIO
                ):
                    audio_map[synth_control.name] = synth_control.value
                else:
                    control_map[synth_control.name] = synth_control.value
            elif synth_control.value != synth_control.default_value:
                settings[synth_control.name] = synth_control.value
        if audio_map:
            request = supriya.commands.NodeMapToAudioBusRequest(
                node_id=self.client, **audio_map
            )
            requests.append(request)
        if control_map:
            request = supriya.commands.NodeMapToControlBusRequest(
                node_id=self.client, **control_map
            )
            requests.append(request)
        return settings, requests

    ### PUBLIC METHODS ###

    def as_dict(self):
        result = {}
        for control_name in self:
            control = self[control_name]
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
