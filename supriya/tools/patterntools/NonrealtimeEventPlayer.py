# -*- encoding: utf-8 -*-
from abjad import new
from supriya.tools.patterntools.EventPlayer import EventPlayer


class NonrealtimeEventPlayer(EventPlayer):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_maximum_duration',
        '_session',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pattern,
        session,
        event_template=None,
        maximum_duration=None,
        ):
        from supriya.tools import nonrealtimetools
        EventPlayer.__init__(
            self,
            pattern,
            event_template,
            )
        assert isinstance(session, nonrealtimetools.Session)
        self._session = session
        if self.pattern.is_infinite:
            maximum_duration = float(maximum_duration)
            assert maximum_duration
        self._maximum_duration = maximum_duration

    ### SPECIAL METHODS ###

    def __call__(self):
        from abjad.tools import systemtools
        self._cumulative_time = 0
        initial_offset = self.session.active_moments[-1].offset
        self._iterator = iter(self._pattern)
        uuids = {}
        for event in self._iterator:
            if not isinstance(event, dict):
                agent = systemtools.StorageFormatAgent(event)
                event = agent.get_template_dict()
            event = new(
                self.event_template,
                **event
                )
            event._perform_nonrealtime(
                session=self.session,
                uuids=uuids,
                offset=initial_offset + self._cumulative_time,
                )
            self._cumulative_time += event.delta

    ### PUBLIC PROPERTIES ###

    @property
    def maximum_duration(self):
        return self._maximum_duration

    @property
    def session(self):
        return self._session
