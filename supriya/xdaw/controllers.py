from uuid import UUID, uuid4

import rtmidi

from .bases import ApplicationObject


class Controller(ApplicationObject):
    def __init__(self, *, name=None, uuid=None):
        ApplicationObject.__init__(self, name=name)
        self._midi_in = rtmidi.MidiIn()
        self._midi_out = rtmidi.MidiOut()
        self._uuid = uuid or uuid4()

    def __str__(self):
        return f"<{type(self).__name__} [{self.port}] {self.uuid}>"

    def _applicate(self, new_application):
        ApplicationObject._applicate(self, new_application)

    def _deapplicate(self, old_application):
        ApplicationObject._deapplicate(self, old_application)

    def _handle_midi_in(self, message, timestamp=None):
        if timestamp is None:
            message, timestamp = message
        transport = self.transport
        if transport is not None:
            transport.perform([message])

    def _reconcile(self, **kwargs):
        difference = ApplicationObject._reconcile(self)
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
        return self

    def open_port(self, port=None, virtual=False):
        if port is None:
            virtual = True
        if virtual:
            self._midi_in.open_virtual_port()
            self._midi_out.open_virtual_port()
        else:
            self._midi_in.open_port(port)
            self._midi_out.open_port(port)
        self._midi_in.ignore_types(active_sense=True, sysex=True, timing=True)
        self._midi_in.set_callback(self._handle_midi_in)

    @property
    def port(self) -> int:
        return self._port

    @property
    def uuid(self) -> UUID:
        return self._uuid
