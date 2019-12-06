class Chord(DeviceObject):

    def __init__(self, name=None, uuid=None):
        DeviceObject.__init__(self, name=name, uuid=uuid)
        self.transpositions = []
        self._event_handlers[NoteOnMessage] = self._handle_note_on
        self._event_handlers[NoteOnMessage] = self._handle_note_off
