# -*- encoding: utf-8 -*-
import uuid
from abjad import new
from supriya.tools.patterntools.Ppar import Ppar


class Pgpar(Ppar):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_release_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        patterns,
        release_time=0.25,
        ):
        Ppar.__init__(self, patterns=patterns)
        release_time = float(release_time)
        assert 0 <= release_time
        self._release_time = release_time

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, expr, state):
        from supriya.tools import patterntools
        iterator = expr.get('_iterator')
        iterators_to_group_uuids = state['iterators_to_group_uuids']
        kwargs = {'_iterator': None}
        if (
            isinstance(expr, patterntools.NoteEvent) or
            not expr.get('is_stop')
            ):
            if expr.get('target_node') is None:
                kwargs['target_node'] = iterators_to_group_uuids[iterator]
            expr = new(expr, **kwargs)
        return expr

    def _setup_peripherals(self, initial_expr, state):
        from supriya.tools import patterntools
        group_uuids = state.get('group_uuids')
        peripheral_starts, peripheral_stops = [], []
        delta = self._release_time or 0
        if delta:
            peripheral_stops.append(patterntools.NullEvent(delta=delta))
        for group_uuid in group_uuids:
            start_group_event = patterntools.GroupEvent(
                uuid=group_uuid,
                add_action='ADD_TO_TAIL',
                )
            stop_group_event = patterntools.GroupEvent(
                uuid=group_uuid,
                is_stop=True,
                )
            peripheral_starts.append(start_group_event)
            peripheral_stops.append(stop_group_event)
        return peripheral_starts, peripheral_stops

    def _setup_state(self):
        state = super(Pgpar, self)._setup_state()
        state['group_uuids'] = []
        state['iterators_to_group_uuids'] = {}
        for iterator_group in state['iterator_groups']:
            group_uuid = uuid.uuid4()
            state['group_uuids'].append(group_uuid)
            for iterator in iterator_group:
                state['iterators_to_group_uuids'][iterator] = group_uuid
        return state

    ### PUBLIC PROPERTIES ###

    @property
    def release_time(self):
        return self._release_time
