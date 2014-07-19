# -*- encoding: utf-8 -*-
from __future__ import print_function
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class MidiDispatcher(SupriyaObject):

    ### CLASS VARIABLES ###

    _midi_map = {}
    _midi_inputs = None

    ### SPECIAL METHODS ###

    def __call__(self, message, timestamp):
        from supriya.tools import miditools
        message = miditools.MidiManager.handle_message(message, timestamp)
        callbacks = self._response_map.get(None, [])
        callbacks += self._response_map.get(type(message), [])
        for callback in callbacks:
            callback(message)
            if callback.is_one_shot:
                self.unregister_callback(callback)

    ### PUBLIC METHODS ###

    @staticmethod
    def initialize():
        import rtmidi_python
        midi_in = MidiDispatcher._midi_in
        if midi_in is not None:
            midi_in.close_port()
            midi_in.callback = None
        else:
            MidiDispatcher._midi_in = rtmidi_python.MidiIn()
            midi_in = MidiDispatcher._midi_in
        midi_in.ignore_types(
            midi_sense=True,
            midi_sysex=True,
            midi_time=True,
            )
        midi_in.open_port()
        midi_in.callback = MidiDispatcher.__call__

    def register_callback(self, callback):
        from supriya.tools import miditools
        assert isinstance(callback, miditools.MidiCallback)
        midi_prototype = callback.midi_prototype
        for class_ in midi_prototype:
            if class_ not in self._midi_map:
                self._midi_map[class_] = []
            self._midi_map[class_].append(callback)

    def unregister_callback(self, callback):
        from supriya.tools import miditools
        assert isinstance(callback, miditools.MidiCallback)
        midi_prototype = callback.midi_prototype
        for class_ in midi_prototype:
            if class_ in self._midi_map:
                if callback in self._midi_map[class_]:
                    self._midi_map[class_].remove(callback)
                if not self._midi_map[class_]:
                    del(self._midi_map[class_])