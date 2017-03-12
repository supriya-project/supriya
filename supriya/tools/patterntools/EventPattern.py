# -*- encoding: utf-8 -*-
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

    def play(self, clock=None, event_template=None, server=None):
        from supriya.tools import patterntools
        from supriya.tools import servertools
        event_player = patterntools.RealtimeEventPlayer(
            self,
            clock=clock,
            server=server or servertools.Server.get_default_server(),
            )
        event_player.start()
        return event_player
