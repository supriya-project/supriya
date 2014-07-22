# -*- encoding: utf-8 -*-
from __future__ import print_function
import threading
import time
from supriya.tools.clocktools.Clock import Clock


class TempoClock(Clock):
    r'''A tempo clock.

    ::

        >>> class Event(object):
        ...     def __init__(self, payload, delta):
        ...         self.payload = payload
        ...         self.delta = delta
        ...     def __call__(self):
        ...         print(self.payload)
        ...         return self.delta

    ::

        >>> import time
        >>> from supriya.tools import clocktools
        >>> clock = clocktools.TempoClock(beats_per_minute=120)
        >>> clock.schedule(Event('kick', 1), 1)
        >>> clock.schedule(Event('\that', 1), 1.5)
        >>> clock.schedule(Event('snare', 2), 2)
        >>> time.sleep(2.25)
        kick
            hat
        snare
        kick
            hat
        kick
            hat
        snare
        kick
            hat

    ::

        >>> clock.reset()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_beats_per_minute',
        '_start_beat',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        beats_per_minute=60,
        start_beat=None,
        start_time=None,
        ):
        Clock.__init__(
            self,
            start_time=start_time,
            )
        if start_beat is None:
            start_beat = 0
        self._start_beat = int(start_beat)
        self._beats_per_minute = float(beats_per_minute)

    ### PRIVATE METHODS ###

    def _beats_to_time(self, beat):
        last_beat, last_beat_time = self.last_beat, self.last_beat_time
        beat_delta = beat - last_beat
        if beat_delta <= 0:
            return 0
        return last_beat_time + (beat_delta * self.beat_duration)

    def _execute(self, scheduled_beat, scheduled_time):
        if scheduled_time != self._next_event_time:
            return
        pairs = []
        with self._lock:
            while self._queue and self._queue[0][0] <= scheduled_beat:
                pair = self._queue.pop(0)
                pairs.append(pair)
            for scheduled_beat, event in pairs:
                reschedule_beat = event()
                if reschedule_beat is not None:
                    absolute_beat = reschedule_beat + scheduled_beat
                    self.schedule_absolutely(event, absolute_beat)
            self._new_timer()

    def _new_timer(self):
        scheduled_beat = self._queue[0][0]
        scheduled_time = self._beats_to_time(scheduled_beat)
        current_time = time.time()
        delta = scheduled_time - current_time
        self._next_event_time = scheduled_time
        self._timer = threading.Timer(
            delta,
            self._execute,
            (scheduled_beat, scheduled_time),
            )
        self._timer.start()

    def _time_to_beats(self, time):
        delta = time - self.start_time
        beats = (delta / self.beat_duration) + self.start_beat
        return beats

    ### PUBLIC METHODS ###

    def schedule(self, event, relative_beat):
        absolute_beat = self.last_beat + relative_beat
        self.schedule_absolutely(event, absolute_beat)

    def schedule_absolutely(self, event, absolute_beat):
        if absolute_beat <= self.current_beat:
            reschedule_time = event()
            if reschedule_time is not None:
                self.schedule(event, reschedule_time)
        absolute_time = self._beats_to_time(absolute_beat)
        with self._lock:
            if absolute_time < self._next_event_time or not self._queue:
                if self._timer is not None:
                    self._timer.cancel()
                self._queue.insert(0, (absolute_beat, event))
                self._queue.sort(key=lambda x: x[0])
                self._new_timer()
            else:
                self._queue.append((absolute_beat, event))
                self._queue.sort(key=lambda x: x[0])

    ### PUBLIC PROPERTIES ###

    @property
    def beat_duration(self):
        return 60. / self._beats_per_minute

    @property
    def beats_per_minute(self):
        return self._beats_per_minute

    @property
    def current_beat(self):
        current_time = time.time()
        time_delta = current_time - self.start_time
        return (time_delta / self.beat_duration) + self.start_beat

    @property
    def last_beat(self):
        return self.current_beat // 1.

    @property
    def last_beat_time(self):
        return self.start_time + (self.last_beat * self.beat_duration)

    @property
    def next_beat(self):
        return self.last_beat + 1

    @property
    def next_beat_time(self):
        return self.start_time + (self.next_beat * self.beat_duration)

    @property
    def start_beat(self):
        return self._start_beat