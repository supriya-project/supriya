# -*- encoding: utf-8 -*-
import uuid
from abjad import new
from supriya.tools.patterntools.Pattern import Pattern


class EventPattern(Pattern):

    ### SPECIAL METHODS ###

    def _coerce_iterator_output(self, expr, state=None):
        from supriya.tools import patterntools
        if not isinstance(expr, patterntools.Event):
            expr = patterntools.NoteEvent(**expr)
        if not expr.get('uuid'):
            expr = new(expr, uuid=uuid.uuid4())
        return expr

    ### PUBLIC METHODS ###

    def inscribe(self, session, event_template=None):
        from supriya.tools import patterntools
        event_player = patterntools.NonrealtimeEventPlayer(
            self,
            session=session,
            event_template=event_template,
            )
        event_player()

    def play(self, clock=None, event_template=None, server=None):
        from supriya.tools import patterntools
        from supriya.tools import servertools
        event_player = patterntools.RealtimeEventPlayer(
            self,
            clock=clock,
            event_template=event_template,
            server=server or servertools.Server.get_default_server(),
            )
        event_player.start()
        return event_player
