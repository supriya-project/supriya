# -*- encoding: utf-8 -*-
from supriya.tools.midifiletools.TrackEvent import TrackEvent


class NoteOffEvent(TrackEvent):
    r'''Note off event.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
       )

    ### INITIALIZER ###

    def __init__(
        self,
        delta_time=0,
        ):
        TrackEvent.__init__(
            self,
            delta_time=delta_time,
            )