# -*- encoding: utf-8 -*-
from __future__ import print_function
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class MidiDispatcher(SupriyaObject):

    ### CLASS VARIABLES ###

    _mapping = {}
    _midi_inputs = None

    ### PRIVATE METHODS ###

    @staticmethod
    def _callback(message, timestamp):
        status_byte, data_byte_one, data_byte_two = message
        message = status_byte >> 4
        channel = status_byte & 0x0f
        result = (message, channel, data_byte_one, data_byte_two) 
        print(result, timestamp)

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
        midi_in.callback = MidiDispatcher._callback