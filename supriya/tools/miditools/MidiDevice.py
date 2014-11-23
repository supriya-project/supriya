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

    def close_port(self):
        self._midi_dispatcher.close_port()

    def list_ports(self):
        return self._midi_dispatcher.list_ports()

    def open_port(self, port=None):
        self._midi_dispatcher.open_port(port)
        return self

    ### PUBLIC PROPERTIES ###

    @property
    def midi_controllers(self):
        return tuple(self._midi_controllers.items())