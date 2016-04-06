# -*- encoding: utf-8 -*-
from __future__ import print_function
from supriya.tools.systemtools.SupriyaObject import SupriyaObject
import threading


class MidiDispatcher(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_callback_map',
        '_debug',
        '_lock',
        '_midi_in',
        )

    ### CLASS VARIABLES ###

    def __init__(self, debug=False):
        import rtmidi
        self._callback_map = {}
        self._debug = bool(debug)
        self._lock = threading.RLock()
        self._midi_in = rtmidi.MidiIn()
        self._midi_in.ignore_types(
            active_sense=True,
            sysex=True,
            timing=True,
            )
        self._midi_in.set_callback(self.__call__)

    ### SPECIAL METHODS ###

    def __call__(self, message, timestamp):
        if timestamp is None:
            message, timestamp = message
        midi_message = MidiDispatcher._handle_message(message, timestamp)
        self.dispatch_message(midi_message)

    ### PRIVATE METHODS ###

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

    def _unregister_one_callback(self, callback):
        callback_maps = [self._callback_map]
        dispatcher_key = callback.dispatcher_key
        for key in dispatcher_key:
            callback_maps.append(callback_maps[-1][key])
        callback_set = callback_maps.pop()
        callback_set.remove(callback)
        for key, callback_map in zip(
            reversed(dispatcher_key), reversed(callback_maps)):
            if not callback_map[key]:
                del(callback_map[key])

    ### PUBLIC METHODS ###

    def close_port(self):
        self._midi_in.close_port()

    def collect_callbacks(self, message):
        callbacks = []
        dispatcher_key = message.dispatcher_key
        old_callback_maps = [self._callback_map]
        for key in dispatcher_key:
            new_callback_maps = []
            subkeys = (key, None)
            for old_callback_map in old_callback_maps:
                for subkey in subkeys:
                    new_callback_map = old_callback_map.get(subkey, None)
                    if not new_callback_map:
                        continue
                    if isinstance(new_callback_map, set):
                        callbacks.extend(new_callback_map)
                    else:
                        new_callback_maps.append(new_callback_map)
            old_callback_maps = new_callback_maps
        return set(callbacks)

    def dispatch_message(self, message):
        if self.debug:
            print('RECV', type(self))
            for line in repr(message).splitlines():
                print('    ' + line)
        callback_pairs = []
        with self.lock:
            callbacks = self.collect_callbacks(message)
            for callback in callbacks:
                callback_pairs.append((callback, message))
                if callback.is_one_shot:
                    self._unregister_one_callback(callback)
        for callback, x in callback_pairs:
            callback(x)

    def list_ports(self):
        return self._midi_in.ports

    def open_port(self, port=None, virtual=False):
        if virtual:
            self._midi_in.open_virtual_port()
        else:
            self._midi_in.open_port(port)

    def register_callback(self, callback):
        assert isinstance(callback, self.callback_class)
        with self.lock:
            callback_map = self._callback_map
            dispatcher_key = callback.dispatcher_key
            for key in dispatcher_key[:-1]:
                if key not in callback_map:
                    callback_map[key] = {}
                callback_map = callback_map[key]
            if dispatcher_key[-1] not in callback_map:
                callback_map[dispatcher_key[-1]] = set()
            callback_map[dispatcher_key[-1]].add(callback)

    def unregister_callback(self, callback):
        assert isinstance(callback, self.callback_class)
        with self.lock:
            self._unregister_one_callback(callback)

    ### PUBLIC PROPERTIES ###

    @property
    def callback_class(self):
        from supriya.tools import miditools
        return miditools.MidiCallback

    @property
    def debug(self):
        return self._debug

    @property
    def lock(self):
        return self._lock


_message_handlers = {
    8: MidiDispatcher._handle_note_on_message,
    9: MidiDispatcher._handle_note_off_message,
    11: MidiDispatcher._handle_controller_change_message,
    }
