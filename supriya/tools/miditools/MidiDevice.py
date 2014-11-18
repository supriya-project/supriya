# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class MidiDevice(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callback',
        '_midi_controls',
        '_midi_dispatcher',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        midi_controls=None,
        ):
        from supriya.tools import miditools
        self._midi_controls = midi_controls
        self._midi_dispatcher = miditools.MidiDispatcher(debug=True)
        for midi_control in self._midi_controls.values():
            self._midi_dispatcher.register_callback(midi_control)

    ### SPECIAL METHODS ###

    def __getattr__(self, name):
        if name in self._midi_controls:
            return self._midi_controls[name]
        return object.__getattribute__(self, name)

    def __getitem__(self, item):
        return self._midi_controls[item]

    def __iter__(self):
        for key in sorted(self._midi_controls.keys()):
            yield key

    def __len__(self):
        return len(self._midi_controls)

    ### PUBLIC METHODS ###

    def close_port(self):
        self._midi_dispatcher.close_port()

    def list_ports(self):
        return self._midi_dispatcher.list_ports()

    def open_port(self, port=None):
        self._midi_dispatcher.open_port(port)

    ### PUBLIC PROPERTIES ###

    @property
    def midi_controls(self):
        return tuple(self._midi_controls.items())