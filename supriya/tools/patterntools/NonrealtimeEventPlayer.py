# -*- encoding: utf-8 -*-
from supriya.tools.patterntools.EventPlayer import EventPlayer
from supriya.tools.patterntools.Pattern import Pattern
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
        from supriya.tools import patterntools
        should_stop = Pattern.PatternState.CONTINUE
        maximum_offset = None
        if self.duration is not None:
            maximum_offset = offset + self.duration
        offset = offset or 0
        actual_stop_offset = offset
        iterator = iter(self._pattern)
        uuids = {}
        try:
            event = next(iterator)
        except StopIteration:
            return offset
        if (
            self.duration is not None and
            isinstance(event, patterntools.NoteEvent) and
            self._get_stop_offset(offset, event) > maximum_offset
            ):
            return offset
        performed_stop_offset = event._perform_nonrealtime(
            session=self.session,
            uuids=uuids,
            maximum_offset=maximum_offset,
            offset=offset,
            )
        offset += event.delta
        actual_stop_offset = max(
            actual_stop_offset,
            performed_stop_offset,
            )
        while True:
            try:
                event = iterator.send(should_stop)
            except StopIteration:
                break
            if (
                maximum_offset is not None and
                isinstance(event, patterntools.NoteEvent) and
                self._get_stop_offset(offset, event) > maximum_offset
                ):
                should_stop = Pattern.PatternState.NONREALTIME_STOP
                continue
            performed_stop_offset = event._perform_nonrealtime(
                session=self.session,
                uuids=uuids,
                maximum_offset=maximum_offset,
                offset=offset,
                )
            offset += event.delta
            actual_stop_offset = max(
                actual_stop_offset,
                performed_stop_offset,
                )
        return actual_stop_offset

    ### PRIVATE METHODS ###

    def _debug(self, event, offset):
        print('    EVENT:', type(event).__name__, offset, event.get('uuid'),
            event.get('duration'))

    def _get_stop_offset(self, offset, event):
        duration = event.get('duration') or 0
        delta = event.get('delta') or 0
        return offset + max(duration, delta)

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return self._duration

    @property
    def session(self):
        return self._session
