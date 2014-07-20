# -*- encoding: utf-8 -*-
from __future__ import print_function
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class MidiDispatcher(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_midi_map',
        '_midi_in',
        )

    ### CLASS VARIABLES ###

    def __init__(self):
        self._midi_map = {}
        self._midi_in = None

    ### SPECIAL METHODS ###

    def __call__(self, message, timestamp):
        from supriya.tools import miditools
        midi_message = miditools.MidiManager.handle_message(message, timestamp)
        callbacks = self._midi_map.get(None, [])
        callbacks += self._midi_map.get(type(midi_message), [])
        for callback in callbacks:
            if callback.channel_number is not None:
                if callback.channel_number != midi_message.channel_number:
                    continue
            callback(midi_message)
            if callback.is_one_shot:
                self.unregister_callback(callback)

    ### PUBLIC METHODS ###

    def initialize(self):
        import rtmidi_python
        midi_in = self._midi_in
        if midi_in is not None:
            midi_in.close_port()
            midi_in.callback = None
        else:
            self._midi_in = rtmidi_python.MidiIn()
            midi_in = self._midi_in
        midi_in.ignore_types(
            midi_sense=True,
            midi_sysex=True,
            midi_time=True,
            )
        midi_in.open_port()
        midi_in.callback = self.__call__
        return self

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