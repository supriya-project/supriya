# -*- encoding: utf-8 -*-
import uuid
from abjad import new
from supriya.tools.patterntools.EventPattern import EventPattern


class Pbus(EventPattern):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_calculation_rate',
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pattern,
        calculation_rate='audio',
        release_time=0.25,
        ):
        from supriya.tools import synthdeftools
        self._pattern = pattern
        self._calculation_rate = synthdeftools.CalculationRate.from_expr(
            calculation_rate)
        release_time = float(release_time)
        assert 0 <= release_time
        self._release_time = release_time

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, expr, state):
        expr = super(Pbus, self)._coerce_iterator_output(expr)
        expr = new(
            expr,
            target_node=state['group_uuid'],
            out=state['bus_uuid'],
            )
        return expr

    def _handle_first(self, expr, state):
        from supriya import synthdefs
        from supriya.tools import patterntools
        synthdef = expr.get('synthdef') or synthdefs.default
        channel_count = synthdef.audio_output_channel_count
        bus_event = patterntools.BusEvent(
            calculation_rate=self.calculation_rate,
            channel_count=channel_count,
            uuid=state['bus_uuid'],
            )
        group_event = patterntools.GroupEvent(
            uuid=state['group_uuid'],
            )
        link_event = patterntools.SynthEvent(
            add_action='ADD_AFTER',
            amplitude=1.0,
            target_node=state['group_uuid'],
            uuid=state['link_uuid'],
            )
        events = [bus_event, group_event, link_event]
        return events, expr

    def _handle_last(self, expr, state):
        from supriya.tools import patterntools
        delta = expr.delta
        delta += (self._release_time or 0)
        expr = new(expr, delta=delta)
        link_event = patterntools.SynthEvent(
            uuid=state['link_uuid'],
            is_stop=True,
            )
        group_event = patterntools.GroupEvent(
            uuid=state['group_uuid'],
            is_stop=True,
            )
        bus_event = patterntools.BusEvent(
            uuid=state['bus_uuid'],
            is_stop=True,
            )
        events = [link_event, group_event, bus_event]
        return expr, events

    def _iterate(self):
        return self._pattern._iterate()

    def _setup_state(self):
        return {
            'bus_uuid': uuid.uuid4(),
            'link_uuid': uuid.uuid4(),
            'group_uuid': uuid.uuid4(),
            }

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return self._pattern.arity

    @property
    def calculation_rate(self):
        return self._calculation_rate

    @property
    def is_infinite(self):
        return self._pattern.is_infinite

    @property
    def pattern(self):
        return self._pattern
