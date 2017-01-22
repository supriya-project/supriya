# -*- encoding: utf-8 -*-
import collections
from abjad import new
try:
    from queue import PriorityQueue
except ImportError:
    from Queue import PriorityQueue
from supriya.tools.patterntools.CompositeEvent import CompositeEvent
from supriya.tools.patterntools.EventPattern import EventPattern


class Ppar(EventPattern):
    """
    Interleave patterns.

    ::

        >>> one = patterntools.Pbind(
        ...     duration=1.0,
        ...     x=patterntools.Pseq([1, 2, 3, 4]),
        ...     )
        >>> two = patterntools.Pbind(
        ...     duration=0.4,
        ...     x=patterntools.Pseq([10, 20, 30, 40]),
        ...     )
        >>> ppar = patterntools.Ppar([one, two])
        >>> print(format(ppar))
        supriya.tools.patterntools.Ppar(
            (
                supriya.tools.patterntools.Pbind(
                    duration=1.0,
                    x=supriya.tools.patterntools.Pseq(
                        (1, 2, 3, 4),
                        repetitions=1,
                        ),
                    ),
                supriya.tools.patterntools.Pbind(
                    duration=0.4,
                    x=supriya.tools.patterntools.Pseq(
                        (10, 20, 30, 40),
                        repetitions=1,
                        ),
                    ),
                )
            )

    ::

        >>> for x in ppar:
        ...     x
        ...
        NoteEvent(delta=0.0, duration=1.0, is_stop=True, uuid=UUID('...'), x=1)
        NoteEvent(duration=0.4, is_stop=True, uuid=UUID('...'), x=10)
        NoteEvent(duration=0.4, is_stop=True, uuid=UUID('...'), x=20)
        NoteEvent(delta=0.2, duration=0.4, is_stop=True, uuid=UUID('...'), x=30)
        NoteEvent(delta=0.2, duration=1.0, is_stop=True, uuid=UUID('...'), x=2)
        NoteEvent(delta=0.8, duration=0.4, is_stop=True, uuid=UUID('...'), x=40)
        NoteEvent(duration=1.0, is_stop=True, uuid=UUID('...'), x=3)
        NoteEvent(duration=1.0, is_stop=True, uuid=UUID('...'), x=4)

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_patterns',
        )

    DEBUG = False

    ### INITIALIZER ###

    def __init__(self, patterns):
        from supriya.tools import patterntools
        assert all(isinstance(_, patterntools.EventPattern) for _ in patterns)
        assert patterns
        self._patterns = tuple(patterns)

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, event, state):
        return new(event, _iterator=None)

    def _setup_state(self):
        iterators = tuple(iter(pattern) for pattern in self._patterns)
        iterator_queue = PriorityQueue()
        event_counter = collections.Counter()
        event_queue = PriorityQueue()
        visited_iterators = set()
        for i, iterator in enumerate(iterators):
            iterator_queue.put((0., i, iterator))
        state = {
            'event_counter': event_counter,
            'event_queue': event_queue,
            'iterator_queue': iterator_queue,
            'iterators': iterators,
            'visited_iterators': visited_iterators,
            }
        return state

    def _iterate(self, state=None):
        has_stopped = False
        should_stop = self.PatternState.CONTINUE
        iterators = state.get('iterators')
        iterator_queue = state.get('iterator_queue')
        event_counter = state.get('event_counter')
        event_queue = state.get('event_queue')
        visited_iterators = state.get('visited_iterators')

        iterator_offset_n1 = {iterator: 0.0 for iterator in iterators}

        while True:
            self._debug()
            self._debug(
                'LOOP',
                'ST:', should_stop,
                'V:', len(visited_iterators),
                'IQ:', iterator_queue.qsize(),
                'EQ:', event_queue.qsize(),
                )
            if not iterator_queue.empty():
                self._debug('\tFETCH NEW EVENT')
                offset, index, iterator = iterator_queue.get()
                iterator_offset_n1[iterator] = offset
                self._debug('\t\tI-GET: {} {} {}'.format(chr(65 + index) * 3,
                    offset, id(iterator)))
                if should_stop and iterator not in visited_iterators:
                    self._debug('\t\tNON-VISITED')
                    continue
                try:
                    event = iterator.send(should_stop)
                    self._debug('\t\tSEND')
                except TypeError:
                    try:
                        event = next(iterator)
                        self._debug('\t\tNEXT')
                    except StopIteration:
                        event = None
                        self._debug('\t\tSTOP (NEXT)')
                except StopIteration:
                    event = None
                    self._debug('\t\tSTOP')
                if event is not None:
                    count = event_counter[iterator]
                    event = new(event, _iterator=iterator)
                    self._debug('\t\tFETCHED:', type(event).__name__, event.get('is_stop') or False)
                    event_queue.put((offset, index, count, event))
                    offset += event.delta
                    iterator_queue.put((offset, index, iterator))
                    event_counter[iterator] += 1
                    self._debug('\t\tI-PUT: {} {} {}'.format(
                        chr(65 + index) * 3, offset, id(iterator)))

            if self.DEBUG:
                self._debug('\tITERATORS')
                debug_iterators = []
                while not iterator_queue.empty():
                    offset, index, iterator = iterator_queue.get()
                    self._debug('\t\t', chr(65 + index) * 3, offset,
                        id(iterator))
                    debug_iterators.append((offset, index, iterator))
                for iterator in debug_iterators:
                    iterator_queue.put(iterator)

            if event_queue.qsize() > 1:
                self._debug('\tYIELD EVENT (DIFFED)')
                a_offset, a_index, a_count, a_event = event_queue.get()
                if should_stop and iterators[a_index] not in visited_iterators:
                    continue

                b_offset, b_index, b_count, b_event = event_queue.get()
                delta = b_offset - a_offset
                duration = a_event.get('duration')
                event = a_event
                if duration is None or duration != delta:
                    event = new(a_event, delta=b_offset - a_offset)

                should_stop = yield event
                if (
                    not should_stop or (
                        should_stop == self.PatternState.REALTIME_STOP and
                        not has_stopped
                        )
                    ):
                    visited_iterators.add(iterators[a_index])

                self._debug('\t\tYIELDED', chr(65 + a_index) * 3,
                    a_offset, type(event).__name__,
                    event.get('is_stop') or False)

                if not should_stop:
                    self._debug('\t\tREPLACING',
                        type(b_event).__name__, b_event.get('is_stop'))
                    b_event = (b_offset, b_index, b_count, b_event)
                    event_queue.put(b_event)
                elif should_stop == self.PatternState.NONREALTIME_STOP:
                    self._debug('\t\tSHOULD STOP: NONREALTIME')
                    self._debug('\t\tREPLACING',
                        type(b_event).__name__, b_event.get('is_stop'))
                    b_event = (b_offset, b_index, b_count, b_event)
                    event_queue.put(b_event)
                    if not has_stopped:
                        has_stopped = True
                        self._unwind(
                            current_offset=offset,
                            event_queue=event_queue,
                            iterator_queue=iterator_queue,
                            iterators=iterators,
                            stopped_event=a_event,
                            stopped_iterator=iterators[a_index],
                            )
                elif should_stop == self.PatternState.REALTIME_STOP:
                    self._debug('\t\tSHOULD STOP: REALTIME')
                    if (
                        isinstance(b_event, CompositeEvent) and
                        b_event.get('is_stop')
                        ):
                        self._debug('\t\tREPLACING',
                            type(b_event).__name__, b_event.get('is_stop'))
                        b_event = (b_offset, b_index, b_count, b_event)
                        event_queue.put(b_event)
                    else:
                        self._debug('\t\t*NOT* REPLACING',
                            type(b_event).__name__, b_event.get('is_stop'))

            elif event_queue.qsize() == 1 and iterator_queue.empty():
                self._debug('\tYIELD EVENT (FINAL)')
                _, index, _, event = event_queue.get()
                yield event
                visited_iterators.add(iterators[index])
                self._debug('\t\tYIELDED', chr(65 + index) * 3,
                    type(event).__name__, event.get('is_stop'))
            if event_queue.empty() and iterator_queue.empty():
                self._debug('\tEXIT')
                break

    def _unwind(
        self,
        current_offset,
        event_queue,
        iterator_queue,
        iterators,
        stopped_event,
        stopped_iterator,
        ):
        from supriya.tools import patterntools
        self._debug('\t\tUNWINDING')
        iterator_map = {}
        while not iterator_queue.empty():
            offset, index, iterator = iterator_queue.get()
            if iterator is stopped_iterator:
                offset -= stopped_event.delta
            iterator_map[iterator] = (offset, index)
        events = []
        while not event_queue.empty():
            offset, index, count, event = event_queue.get()
            if (
                isinstance(event, patterntools.CompositeEvent)
                ):
                events.append((offset, index, count, event))
            else:
                iterator = iterators[index]
                offset, index = iterator_map[iterator]
                offset -= event.delta
                iterator_map[iterator] = (offset, index)
        for iterator, (offset, index) in iterator_map.items():
            iterator_queue.put((offset, index, iterator))
        for event_tuple in events:
            event_queue.put(event_tuple)

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return max(self._get_arity(_) for _ in self._patterns)

    @property
    def is_infinite(self):
        return all(_.is_infinite for _ in self._patterns)

    @property
    def patterns(self):
        return self._patterns
