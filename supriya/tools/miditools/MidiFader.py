# -*- encoding: utf-8- -*-
from supriya.tools.miditools.MidiController import MidiController


class MidiFader(MidiController):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        channel_number=None,
        controller_number=None,
        ):
        from supriya.tools import synthdeftools
        MidiController.__init__(
            self,
            channel_number=channel_number,
            controller_number=controller_number,
            )
        self._output_range = synthdeftools.Range(0, 127)