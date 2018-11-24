from supriya.midi.MidiMessage import MidiMessage


class NoteOffMessage(MidiMessage):

    ### CLASS VARIABLES ###

    __slots__ = ("_note_number", "_velocity")

    ### INITIALIZER ###

    def __init__(
        self, channel_number=None, note_number=None, timestamp=None, velocity=None
    ):
        MidiMessage.__init__(self, channel_number=channel_number, timestamp=timestamp)
        self._note_number = note_number
        self._velocity = velocity

    ### PUBLIC PROPERTIES ###

    @property
    def note_number(self):
        return self._note_number

    @property
    def velocity(self):
        return self._velocity
