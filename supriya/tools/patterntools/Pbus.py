# -*- encoding: utf-8 -*-
import uuid
from abjad import new
from supriya.tools.patterntools.EventPattern import EventPattern


class Pbus(EventPattern):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_calculation_rate',
        '_channel_count',
        '_pattern',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        pattern,
        calculation_rate='audio',
        channel_count=None,
        release_time=0.25,
        ):
        from supriya.tools import synthdeftools
        self._pattern = pattern
        calculation_rate = synthdeftools.CalculationRate.from_expr(
            calculation_rate)
        assert calculation_rate in (
            synthdeftools.CalculationRate.AUDIO,
            synthdeftools.CalculationRate.CONTROL,
            )
        self._calculation_rate = calculation_rate
        if channel_count is not None:
            channel_count = int(channel_count)
            assert 0 < channel_count
        self._channel_count = channel_count
        release_time = float(release_time)
        assert 0 <= release_time
        self._release_time = release_time

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, expr, state):
        from supriya.tools import patterntools
        expr = super(Pbus, self)._coerce_iterator_output(expr)
        kwargs = {}
        if expr.get('target_node') is None:
            kwargs['target_node'] = state['group_uuid']
        if (isinstance(expr, patterntools.NoteEvent) and
            expr.get('out') is None):
            kwargs['out'] = state['bus_uuid']
        expr = new(expr, **kwargs)
        return expr

    def _handle_first(self, expr, state):
        from supriya import synthdefs
        from supriya.tools import patterntools
        from supriya.tools import synthdeftools
        channel_count = self.channel_count
        if channel_count is None:
            synthdef = expr.get('synthdef') or synthdefs.default
            channel_count = synthdef.audio_output_channel_count
        if self.calculation_rate == synthdeftools.CalculationRate.AUDIO:
            link_synthdef_name = 'system_link_audio_{}'.format(channel_count)
        else:
            link_synthdef_name = 'system_link_control_{}'.format(channel_count)
        link_synthdef = getattr(synthdefs, link_synthdef_name)
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
            in_=state['bus_uuid'],
            synthdef=link_synthdef,
            target_node=state['group_uuid'],
            uuid=state['link_uuid'],
            )
        return [bus_event, group_event, link_event, expr]

    def _handle_last(self, expr, state=None, yield_count=0):
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
        events = events[-yield_count:]
        events.insert(0, expr)
        return events

    def _iterate(self, state=None):
        return iter(self.pattern)

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
    def channel_count(self):
        return self._channel_count

    @property
    def is_infinite(self):
        return self._pattern.is_infinite

    @property
    def pattern(self):
        return self._pattern
