# -*- encoding: utf-8 -*-
from supriya.tools.patterntools.EventPlayer import EventPlayer
from supriya.tools.nonrealtimetools.SessionObject import SessionObject


class NonrealtimeEventPlayer(EventPlayer):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_duration',
        '_session',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pattern,
        session,
        duration=None,
        ):
        from supriya.tools import nonrealtimetools
        EventPlayer.__init__(
            self,
            pattern,
            )
        assert isinstance(session, nonrealtimetools.Session)
        self._session = session
        if self.pattern.is_infinite:
            duration = float(duration)
            assert duration
        self._duration = duration

    ### SPECIAL METHODS ###

    @SessionObject.require_offset
    def __call__(self, offset=None):
        maximum_offset = None
        offset = offset or 0
        self._iterator = iter(self._pattern)
        uuids = {}
        if self.duration is not None:
            maximum_offset = offset + self.duration
        for event in self._iterator:
            event._perform_nonrealtime(
                session=self.session,
                uuids=uuids,
                maximum_offset=maximum_offset,
                offset=offset,
                )
            if event.delta:
                offset += event.delta
            if maximum_offset is not None and offset >= maximum_offset:
                self._iterator.send(True)
        return offset

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return self._duration

    @property
    def session(self):
        return self._session
