from supriya.midi.MidiMessage import MidiMessage


class NoteOffMessage(MidiMessage):

    ### CLASS VARIABLES ###

    __slots__ = ("_pitch", "_velocity")

    ### INITIALIZER ###

    def __init__(self, channel_number=None, pitch=None, timestamp=None, velocity=None):
        MidiMessage.__init__(self, channel_number=channel_number, timestamp=timestamp)
        self._pitch = pitch
        self._velocity = velocity

    ### PUBLIC PROPERTIES ###

    @property
    def pitch(self):
        return self._pitch

    @property
    def velocity(self):
        return self._velocity
