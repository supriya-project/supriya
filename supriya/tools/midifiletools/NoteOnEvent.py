# -*- encoding: utf-8 -*-
from supriya.tools.midifiletools.TrackEvent import TrackEvent


class NoteOnEvent(TrackEvent):
    r'''Note on event.
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