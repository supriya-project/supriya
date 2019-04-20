import uuid

from uqbar.objects import new

from supriya.patterns.Pattern import Pattern


class EventPattern(Pattern):

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def _coerce_iterator_output(self, expr, state=None):
        import supriya.patterns

        if not isinstance(expr, supriya.patterns.Event):
            expr = supriya.patterns.NoteEvent(**expr)
        if expr.get("uuid") is None:
            expr = new(expr, uuid=uuid.uuid4())
        return expr

    ### PUBLIC METHODS ###

    def play(self, clock=None, server=None):
        import supriya.patterns
        import supriya.realtime

        event_player = supriya.patterns.RealtimeEventPlayer(
            self, clock=clock, server=server or supriya.realtime.Server.default()
        )
        event_player.start()
        return event_player

    def with_bus(self, calculation_rate="audio", channel_count=None, release_time=0.25):
        import supriya.patterns

        return supriya.patterns.Pbus(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            release_time=release_time,
        )

    def with_effect(self, synthdef, release_time=0.25, **settings):
        import supriya.patterns

        return supriya.patterns.Pfx(
            self, synthdef=synthdef, release_time=release_time, **settings
        )

    def with_group(self, release_time=0.25):
        import supriya.patterns

        return supriya.patterns.Pgroup(self, release_time=release_time)
