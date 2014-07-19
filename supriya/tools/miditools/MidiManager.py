# -*- encoding: utf-8 -*-
from __future__ import print_function
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class MidiManager(SupriyaObject):

    ### PUBLIC METHODS ###

    @staticmethod
    def handle_controller_change_message(channel_number, data, timestamp):
        pass

    @staticmethod
    def handle_note_off_message(channel_number, data, timestamp):
        pass

    @staticmethod
    def handle_note_on_message(channel_number, data, timestamp):
        pass

    @staticmethod
    def handle_message(message, timestamp):
        status_byte, data = message[0], message[1:]
        message_type = status_byte >> 4
        channel_number = status_byte & 0x0f
        if message_type in _message_handlers:
            handler = _message_handlers[message_type]
            result = handler(channel_number, data, timestamp)
        else:
            raise ValueError(message)
        return result


_message_handlers = {
    8: MidiManager.handle_note_on_message,
    9: MidiManager.handle_note_off_message,
    11: MidiManager.handle_controller_change_message,
    }