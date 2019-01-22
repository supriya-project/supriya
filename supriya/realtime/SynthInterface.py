import collections

from supriya.realtime.ControlInterface import ControlInterface


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
        elif isinstance(item, collections.Iterable):
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
            <SynthInterface: <- Synth: ???>>

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
            <- Synth: ???>: (default)
                (kr) amplitude: 0.1
                (kr) frequency: 440.0
                (kr) gate:      1.0
                (ir) out:       0.0
                (kr) pan:       0.5

        """
        result = []
        string = "{}: ({})".format(repr(self.client), self.synthdef.actual_name)
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
        if self.client.register_controls is None or self.client.register_controls:
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
