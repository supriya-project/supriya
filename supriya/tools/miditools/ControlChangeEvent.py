# -*- encoding: utf-8 -*-
from supriya.tools.miditools.TrackEvent import TrackEvent


class ControlChangeEvent(TrackEvent):
    r'''Control change event.
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