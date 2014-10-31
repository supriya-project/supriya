# -*- encoding: utf-8 -*-
from __future__ import print_function
from supriya.tools.systemtools.Dispatcher import Dispatcher


class MidiDispatcher(Dispatcher):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_midi_in',
        )

    ### CLASS VARIABLES ###

    def __init__(self, debug=False):
        import rtmidi_python
        Dispatcher.__init__(
            self,
            debug=debug,
            )
        self._midi_in = rtmidi_python.MidiIn()
        self._midi_in.ignore_types(
            midi_sense=True,
            midi_sysex=True,
            midi_time=True,
            )
        self._midi_in.callback = self.__call__

    ### SPECIAL METHODS ###

    def __call__(self, message, timestamp):
        Dispatcher.__call__(self, (message, timestamp))

    ### PRIVATE METHODS ###

    def _coerce_input(self, expr):
        from supriya.tools import miditools
        message, timestamp = expr
        midi_message = miditools.MidiManager.handle_message(message, timestamp)
        return (midi_message,)

    ### PUBLIC METHODS ###

    def open_port(self):
        self._midi_in.open_port()

    ### PUBLIC PROPERTIES ###

    @property
    def callback_class(self):
        from supriya.tools import miditools
        return miditools.MidiCallback