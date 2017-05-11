# -*- encoding: utf-8 -*-
import collections
from abjad import new
try:
    from queue import PriorityQueue
except ImportError:
    from Queue import PriorityQueue
from supriya.tools.patterntools.EventPattern import EventPattern


class Ppar(EventPattern):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_patterns',
        )

    _IteratorTuple = collections.namedtuple(
        '_IteratorTuple',
        ['offset', 'index', 'iterator'],
        )

    _EventTuple = collections.namedtuple(
        '_EventTuple',
        ['offset', 'iterator_index', 'event_index', 'event'],
        )

    ### INITIALIZER ###

    def __init__(self, patterns):
        from supriya.tools import patterntools
        patterns = list(patterns)
        for i, pattern_group in enumerate(patterns):
            if isinstance(pattern_group, patterntools.EventPattern):
                pattern_group = [pattern_group]
            assert isinstance(pattern_group, collections.Sequence)
            pattern_group = tuple(pattern_group)
            assert all(isinstance(_, patterntools.EventPattern)
                for _ in pattern_group)
            patterns[i] = pattern_group
        assert patterns
        self._patterns = tuple(patterns)

    ### PRIVATE METHODS ###

    def _apply_iterator_recursively(self, expr, iterator):
        from supriya.tools import patterntools
        if isinstance(expr, patterntools.CompositeEvent):
            coerced_events = [
                self._apply_iterator_recursively(child_event, iterator)
                for child_event in expr.get('events') or ()
                ]
            expr = new(expr, events=coerced_events)
        else:
            expr = new(expr, _iterator=iterator)
        return expr

    def _coerce_iterator_output(self, expr, state):
        expr = super(Ppar, self)._coerce_iterator_output(expr, state)
        return new(expr, _iterator=None)

    def _iterate(self, state=None):
        while True:
            self._debug('LOOP START')
            self._debug('    STOPPED?:', state['has_stopped'])
            self._debug('    VISITED?:', state['visited_iterators'])
            if not state['iterator_queue'].empty():
                self._debug('PRIME QUEUES')
                self._prime_queues(state)
            elif state['event_queue'].empty():
                self._debug('ALL DONE')
                return
            if state['event_queue'].qsize() > 1:
                self._debug('YIELDING INNER')
                event_tuple_a = self._fetch_event_tuple_a(state)
                if not event_tuple_a:
                    continue
                event_tuple_b = self._fetch_event_tuple_b(state)
                event = self._pre_process_event(
                    event_tuple_a,
                    event_tuple_b,
                    )
                self._debug(
                    '    EVENT', type(event).__name__,
                    'STOP?', event.get('is_stop'),
                    event.get('frequency') or '',
                    )
                state['should_stop'] = yield event
                self._debug('    STOP?', state['should_stop'])
                self._post_process_event(
                    event,
                    event_tuple_a,
                    event_tuple_b,
                    state,
                    )
            elif (
                state['event_queue'].qsize() == 1 and
                state['iterator_queue'].empty()
                ):
                self._debug('YIELDING FINAL')
                event = self._process_final_event(state)
                self._debug(
                    '    EVENT', type(event).__name__,
                    'STOP?', event.get('is_stop'),
                    event.get('frequency') or '',
                    )
                yield event

    def _fetch_event_tuple_a(self, state):
        event_tuple_a = state['event_queue'].get()
        if (
            state['has_stopped'] and
            event_tuple_a.iterator_index not in state['visited_iterators']
            ):
            return
        return event_tuple_a

    def _fetch_event_tuple_b(self, state):
        return state['event_queue'].get()

    def _pre_process_event(self, event_tuple_a, event_tuple_b):
        delta = float(event_tuple_b.offset - event_tuple_a.offset)
        return new(event_tuple_a.event, delta=delta)

    def _post_process_event(self, event, event_tuple_a, event_tuple_b, state):
        state['event_queue'].put(event_tuple_b)
        if not state['should_stop']:
            state['visited_iterators'].add(event_tuple_a.iterator_index)
            return
        if state['should_stop'] == self.PatternState.NONREALTIME_STOP:
            self._process_nonrealtime_stop(state)
        elif state['should_stop'] == self.PatternState.REALTIME_STOP:
            self._process_nonrealtime_stop(state)
            #self._process_realtime_stop(
            #    event, event_tuple_a, event_tuple_b, state,
            #    )

    def _process_nonrealtime_stop(self, state):
        from supriya.tools import patterntools
        if not state['has_stopped']:
            state['has_stopped'] = True
        self._debug('UNWINDING')
        assert state['event_queue'].qsize() == 1

        event_tuple = state['event_queue'].get()
        if event_tuple.iterator_index not in state['visited_iterators']:
            self._debug('    DISCARDING, UNVISITED', event_tuple)
        elif not isinstance(event_tuple.event, patterntools.CompositeEvent):
            self._debug('    DISCARDING, NON-COMPOSITE', event_tuple)
        elif not event_tuple.event.get('is_stop'):
            self._debug('    DISCARDING, NON-STOP', event_tuple)
        else:
            self._debug('    PRESERVING', event_tuple)
            state['event_queue'].put(event_tuple._replace(offset=0.0))

        iterator_queue = PriorityQueue()
        while not state['iterator_queue'].empty():
            iterator_tuple = state['iterator_queue'].get()
            iterator_tuple = iterator_tuple._replace(offset=0.0)
            iterator_queue.put(iterator_tuple)
        state['iterator_queue'] = iterator_queue

    def _process_realtime_stop(
        self,
        event,
        event_tuple_a,
        event_tuple_b,
        state,
        ):
        if not state['has_stopped']:
            state['visited_iterators'].add(event_tuple_a.iterator_index)
            state['has_stopped'] = True

    def _process_final_event(self, state):
        event_tuple = state['event_queue'].get()
        state['visited_iterators'].add(event_tuple.iterator_index)
        return event_tuple.event

    def _prime_queues(self, state):
        iterator_tuple = state['iterator_queue'].get()
        iterator = iterator_tuple.iterator
        self._debug('    ITER:', iterator_tuple)
        if (
            state['has_stopped'] and
            iterator_tuple.index not in state['visited_iterators']
            ):
            self._debug('    SKIP: STOPPED AND NON-VISITED')
            return
        try:
            event = iterator.send(state['should_stop'])
        except TypeError:
            self._debug('    SEND: NOT YET STARTED')
            try:
                event = next(iterator)
            except StopIteration:
                self._debug('    NEXT: EMPTY')
                return
        except StopIteration:
            self._debug('    SEND: EMPTY')
            return
        self._debug('    EVENT:', event)
        event_index = state['event_counter'][iterator]
        event = self._apply_iterator_recursively(event, iterator)
        event_tuple = self._EventTuple(
            offset=iterator_tuple.offset,
            iterator_index=iterator_tuple.index,
            event_index=event_index,
            event=event,
            )
        state['event_queue'].put(event_tuple)
        state['event_counter'][iterator] += 1
        state['iterator_queue'].put(
            iterator_tuple._replace(
                offset=float(iterator_tuple.offset + event.delta),
                )
            )

    def _setup_state(self):
        iterators, iterator_groups = [], []
        for pattern_group in self.patterns:
            iterator_group = []
            for pattern in pattern_group:
                iterator = iter(pattern)
                iterators.append(iterator)
                iterator_group.append(iterator)
            iterator_groups.append(tuple(iterator_group))
        iterator_queue = PriorityQueue()
        for i, iterator in enumerate(iterators):
            iterator_tuple = self._IteratorTuple(
                offset=0,
                index=i,
                iterator=iterator,
                )
            iterator_queue.put(iterator_tuple)
        state = {
            'event_counter': collections.Counter(),
            'event_queue': PriorityQueue(),
            'has_stopped': False,
            'iterator_queue': iterator_queue,
            'iterators': iterators,
            'iterator_groups': tuple(iterator_groups),
            'should_stop': self.PatternState.CONTINUE,
            'visited_iterators': set(),
            }
        return state

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        patterns = []
        for _ in self._patterns:
            patterns.extend(_)
        return max(self._get_arity(_) for _ in patterns)

    @property
    def is_infinite(self):
        patterns = []
        for _ in self._patterns:
            patterns.extend(_)
        return all(_.is_infinite for _ in patterns)

    @property
    def patterns(self):
        return self._patterns
