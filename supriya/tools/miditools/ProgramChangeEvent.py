# -*- encoding: utf-8 -*-
from supriya.tools.miditools.TrackEvent import TrackEvent


class ProgramChangeEvent(TrackEvent):
    r'''Program change event.
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