import uuid
from abjad import new
from supriya.tools.patterntools.Pattern import Pattern


class EventPattern(Pattern):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def _coerce_iterator_output(self, expr, state=None):
        from supriya.tools import patterntools
        if not isinstance(expr, patterntools.Event):
            expr = patterntools.NoteEvent(**expr)
        if expr.get('uuid') is None:
            expr = new(expr, uuid=uuid.uuid4())
        return expr

    ### PUBLIC METHODS ###

    def play(self, clock=None, server=None):
        from supriya.tools import patterntools
        from supriya.tools import servertools
        event_player = patterntools.RealtimeEventPlayer(
            self,
            clock=clock,
            server=server or servertools.Server.get_default_server(),
            )
        event_player.start()
        return event_player

    def with_bus(
        self,
        calculation_rate='audio',
        channel_count=None,
        release_time=0.25,
        ):
        from supriya.tools import patterntools
        return patterntools.Pbus(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            release_time=release_time,
            )

    def with_effect(
        self,
        synthdef,
        release_time=0.25,
        **settings
        ):
        from supriya.tools import patterntools
        return patterntools.Pfx(
            self,
            synthdef=synthdef,
            release_time=release_time,
            **settings
            )

    def with_group(self, release_time=0.25):
        from supriya.tools import patterntools
        return patterntools.Pgroup(
            self,
            release_time=release_time,
            )
