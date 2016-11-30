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
        should_stop = False
        maximum_offset = None
        if self.duration is not None:
            maximum_offset = offset + self.duration
        offset = offset or 0
        iterator = iter(self._pattern)
        uuids = {}
        while True:
            try:
                if should_stop:
                    print('FETCHING VIA SEND')
                    event = iterator.send(True)
                else:
                    print('FETCHING VIA NEXT')
                    event = next(iterator)
            except StopIteration:
                print('    TERMINATING', offset)
                break
            self._debug(event, offset)
            event._perform_nonrealtime(
                session=self.session,
                uuids=uuids,
                maximum_offset=maximum_offset,
                offset=offset,
                )
            if event.delta:
                offset += event.delta
                if (
                    not should_stop and
                    maximum_offset and
                    maximum_offset <= offset
                ):
                    print('MAXED OUT:', offset, maximum_offset)
                    should_stop = True
        return offset

    ### PRIVATE METHODS ###

    def _debug(self, event, offset):
        print('    EVENT:', type(event).__name__, offset, event.get('uuid'),
            event.get('duration'))

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return self._duration

    @property
    def session(self):
        return self._session
