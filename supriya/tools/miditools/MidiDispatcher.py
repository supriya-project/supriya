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
        message, timestamp = expr
        midi_message = MidiDispatcher._handle_message(message, timestamp)
        return (midi_message,)

    @staticmethod
    def _handle_controller_change_message(channel_number, data, timestamp):
        from supriya.tools import miditools
        controller_number, controller_value = data
        message = miditools.ControllerChangeMessage(
            channel_number=channel_number,
            controller_number=controller_number,
            controller_value=controller_value,
            timestamp=timestamp,
            )
        return message

    @staticmethod
    def _handle_note_off_message(channel_number, data, timestamp):
        from supriya.tools import miditools
        note_number, velocity = data
        message = miditools.NoteOffMessage(
            channel_number=channel_number,
            note_number=note_number,
            timestamp=timestamp,
            velocity=velocity,
            )
        return message

    @staticmethod
    def _handle_note_on_message(channel_number, data, timestamp):
        from supriya.tools import miditools
        note_number, velocity = data
        message = miditools.NoteOnMessage(
            channel_number=channel_number,
            note_number=note_number,
            timestamp=timestamp,
            velocity=velocity,
            )
        return message

    @staticmethod
    def _handle_message(message, timestamp):
        status_byte, data = message[0], message[1:]
        message_type = status_byte >> 4
        channel_number = status_byte & 0x0f
        if message_type in _message_handlers:
            _handler = _message_handlers[message_type]
            result = _handler(channel_number, data, timestamp)
        else:
            raise ValueError(message)
        return result

    ### PUBLIC METHODS ###

    def close_port(self):
        self._midi_in.close_port()

    def open_port(self, port=None):
        self._midi_in.open_port(port)

    ### PUBLIC PROPERTIES ###

    @property
    def callback_class(self):
        from supriya.tools import miditools
        return miditools.MidiCallback


_message_handlers = {
    8: MidiDispatcher.handle_note_on_message,
    9: MidiDispatcher.handle_note_off_message,
    11: MidiDispatcher.handle_controller_change_message,
    }