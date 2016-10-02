# -*- encoding: utf-8 -*-
import uuid
from abjad import new
try:
    from queue import PriorityQueue
except ImportError:
    from Queue import PriorityQueue
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

    def _coerce_iterator_output(self, event, state):
        iterator = event.get('_iterator')
        group_uuid = state[2][iterator]
        return new(event, target_node=group_uuid, _iterator=None)

    def _handle_first(self, expr, state):
        from supriya.tools import patterntools
        _, group_uuids, _ = state
        events = []
        for group_uuid in group_uuids:
            group_event = patterntools.GroupEvent(
                uuid=group_uuid,
                add_action='ADD_TO_TAIL',
                )
            events.append(group_event)
        return events, expr

    def _handle_last(self, expr, state):
        from supriya.tools import patterntools
        _, group_uuids, _ = state
        delta = expr.delta
        delta += (self._release_time or 0)
        expr = new(expr, delta=delta)
        events = []
        for group_uuid in group_uuids:
            group_event = patterntools.GroupEvent(
                uuid=group_uuid,
                is_stop=True,
                )
            events.append(group_event)
        return expr, events

    def _setup_state(self):
        queue = PriorityQueue()
        group_uuids = []
        iterators_to_group_uuids = {}
        for index, pattern in enumerate(self._patterns, 1):
            iterator = iter(pattern)
            group_uuid = uuid.uuid4()
            payload = ((0.0, index), iterator)
            queue.put(payload)
            group_uuids.append(group_uuid)
            iterators_to_group_uuids[iterator] = group_uuid
        state = (queue, group_uuids, iterators_to_group_uuids)
        return state
