from supriya.midi.MidiMessage import MidiMessage


class ControllerChangeMessage(MidiMessage):

    ### CLASS VARIABLES ###

    __slots__ = ("_controller_number", "_controller_value")

    ### INITIALIZER ###

    def __init__(
        self,
        channel_number=None,
        controller_number=None,
        controller_value=None,
        timestamp=None,
    ):
        MidiMessage.__init__(self, channel_number=channel_number, timestamp=timestamp)
        self._controller_number = controller_number
        self._controller_value = controller_value

    ### PUBLIC PROPERTIES ###

    @property
    def controller_number(self):
        return self._controller_number

    @property
    def controller_value(self):
        return self._controller_value

    @property
    def dispatcher_key(self):
        return (type(self), self._channel_number, self._controller_number)
