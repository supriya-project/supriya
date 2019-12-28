from uuid import UUID, uuid4

import rtmidi

from supriya.midi import ControllerChangeMessage, NoteOffMessage, NoteOnMessage

from .bases import ApplicationObject


class Controller(ApplicationObject):
    def __init__(self, *, name=None, uuid=None):
        ApplicationObject.__init__(self, name=name)
        self._midi_in = rtmidi.MidiIn()
        self._midi_out = rtmidi.MidiOut()
        self._uuid = uuid or uuid4()
        self._port = None

    def __str__(self):
        obj_name = type(self).__name__
        port = self._midi_in.get_port_name(self.port) if self.port is not None else "..."
        return "\n".join([
            f"<{obj_name} [{port}] {self.uuid}>",
            *(f"    {line}" for child in self for line in str(child).splitlines()),
        ])

    def _applicate(self, new_application):
        ApplicationObject._applicate(self, new_application)

    def _deapplicate(self, old_application):
        ApplicationObject._deapplicate(self, old_application)

    def _handle_midi_in(self, *args):
        self._debug_tree(self, "MIDI In", suffix=repr(args))
        message = None
        event, timestamp = args[0]
        status_byte, data = event[0], event[1:]
        message_type = status_byte >> 4
        channel_number = status_byte & 0x0F
        if message_type == 8:
            message = NoteOffMessage(
                channel_number=channel_number,
                note_number=data[0],
                velocity=data[1],
                timestamp=timestamp,
            )
        elif message_type == 9:
            class_ = NoteOnMessage
            if data[1] == 0:
                class_ = NoteOffMessage
            message = class_(
                channel_number=channel_number,
                note_number=data[0],
                velocity=data[1],
                timestamp=timestamp,
            )
        elif message_type == 11:
            message = ControllerChangeMessage(
                channel_number=channel_number,
                controller_number=data[0],
                controller_value=data[1],
                timestamp=timestamp,
            )
        if message is None:
            return
        transport = self.transport
        if transport is not None:
            transport.perform([message])

    def _reconcile(self, **kwargs):
        difference = self._get_state_difference()
        if "application" in difference:
            old_application, new_application = difference.pop("application")
            if old_application:
                self._deapplicate(old_application)
            if new_application:
                self._applicate(new_application)
            for child in self:
                child._set(application=new_application)

    def close_port(self):
        self._midi_in.close_port()
        self._midi_out.close_port()
        self._port = None
        return self

    def open_port(self, port=None):
        if port is None:
            self._midi_in.open_virtual_port()
            self._midi_out.open_virtual_port()
        else:
            self._port = port
            self._midi_in.open_port(port)
            self._midi_out.open_port(port)
        self._midi_in.ignore_types(active_sense=True, sysex=True, timing=True)
        self._midi_in.set_callback(self._handle_midi_in)
        return self

    @property
    def port(self):
        return self._port

    @property
    def uuid(self) -> UUID:
        return self._uuid
