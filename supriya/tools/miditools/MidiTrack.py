# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class MidiTrack(SupriyaValueObject):
    r'''MIDI track.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_track_events',
        )

    ### INITIALIZER ###

    def __init__(self, track_events=None):
        from supriya.tools import miditools
        prototype = miditools.TrackEvent
        if track_events is not None:
            assert all(isinstance(_, prototype) for _ in track_events)
            track_events = tuple(track_events)
        self._track_events = track_events

    ### PUBLIC PROPERTIES ###

    @property
    def track_events(self):
        r'''Gets track events in MIDI track.
        '''
        return self._track_events


