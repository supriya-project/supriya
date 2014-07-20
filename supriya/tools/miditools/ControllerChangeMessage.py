# -*- encoding: utf-8 -*-
from supriya.tools.miditools.MidiMessage import MidiMessage


class ControllerChangeMessage(MidiMessage):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_controller_number',
        '_value',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        channel_number=None,
        controller_number=None,
        timestamp=None,
        value=None,
        ):
        MidiMessage.__init__(
            self,
            channel_number=channel_number,
            timestamp=timestamp,
            )
        self._controller_number = controller_number
        self._value = value

    ### PUBLIC PROPERTIES ###

    @property
    def controller_number(self):
        return self._controller_number

    @property
    def value(self):
        return self._value