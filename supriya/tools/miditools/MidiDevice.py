# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class MidiDevice(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callback',
        '_midi_controllers',
        '_midi_dispatcher',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        midi_controllers=None,
        ):
        from supriya.tools import miditools
        self._midi_controllers = midi_controllers
        self._midi_dispatcher = miditools.MidiDispatcher(debug=True)
        for midi_controller in self._midi_controllers.values():
            self._midi_dispatcher.register_callback(midi_controller)

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        if name in self._midi_controllers:
            return self._midi_controllers[name]
        return object.__getattribute__(self, name)

    def __getitem__(self, item):
        return self._midi_controllers[item]

    def __iter__(self):
        for key in sorted(self._midi_controllers.keys()):
            yield key

    def __len__(self):
        return len(self._midi_controllers)

    ### PUBLIC METHODS ###

    def autobind(self, synth):
        from supriya import bind
        from supriya.tools import miditools
        from supriya.tools import servertools
        from supriya.tools import synthdeftools
        assert isinstance(synth, servertools.Synth)
        buttons, faders = [], []
        for controller_name in sorted(self):
            controller = self[controller_name]
            if isinstance(controller, miditools.MidiButton):
                buttons.append(controller)
            else:
                faders.append(controller)
        control_rate_controls, trigger_rate_controls = [], []
        parameters = synth.synthdef.parameters
        controls = synth.controls._synth_control_map
        for control_name, control in sorted(controls.items()):
            if control.calculation_rate in (
                synthdeftools.CalculationRate.AUDIO,
                synthdeftools.CalculationRate.SCALAR,
                ):
                continue
            elif parameters[control_name].parameter_rate is \
                synthdeftools.ParameterRate.TRIGGER:
                trigger_rate_controls.append(control)
            else:
                control_rate_controls.append(control)
        bindings = []
        for fader, control in zip(faders, control_rate_controls):
            bindings.append(bind(fader, control))
        for button, control in zip(buttons, trigger_rate_controls):
            bindings.append(bind(button, control))
        return bindings

    def close_port(self):
        self._midi_dispatcher.close_port()

    def list_ports(self):
        return self._midi_dispatcher.list_ports()

    def open_port(self, port=None):
        port = port or 0
        self._midi_dispatcher.open_port(port)
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def midi_controllers(self):
        return tuple(self._midi_controllers.items())
