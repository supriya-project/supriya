# -*- encoding: utf-8 -*-
from __future__ import print_function
import time
import threading
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Clock(SupriyaObject):
    r'''A clock.

    ::

        >>> clock = clocktools.Clock()
        >>> print(format(clock))
        supriya.tools.clocktools.Clock(
            start_time=...,
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lock',
        '_next_event_time',
        '_queue',
        '_start_time',
        '_timer',
        )

    ### INITIALIZER ###

    def __init__(self, start_time=None):
        if start_time is None:
            start_time = time.time()
        self._start_time = float(start_time)
        self._lock = threading.RLock()
        self._next_event_time = start_time
        self._queue = []
        self._timer = None

    ### PRIVATE METHODS ###

    def _execute(self, scheduled_time):
        if scheduled_time != self._next_event_time:
            return
        pairs = []
        with self._lock:
            while self._queue and self._queue[0][0] <= scheduled_time:
                pair = self._queue.pop(0)
                pairs.append(pair)
            for scheduled_time, event in pairs:
                reschedule_time = event()
                if reschedule_time is not None:
                    self.schedule(event, reschedule_time)
            self._new_timer()

    def _new_timer(self):
        scheduled_time = self._queue[0][0]
        now = time.time()
        delta = scheduled_time - now
        self._next_event_time = scheduled_time
        self._timer = threading.Timer(
            delta,
            self._execute,
            (scheduled_time,),
            )
        self._timer.start()

    ### PUBLIC METHODS ###

    def reset(self):
        r'''Resets clock.

        Stops current timer and empties the event queue.

        Returns none.
        '''
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            self._queue[:] = []
            self._next_event_time = 0

    def schedule(self, event, relative_time):
        r'''Schedules `event` at `relative_time` relative to the current time
        in seconds.

        Returns none.
        '''
        absolute_time = time.time() + relative_time
        self.schedule_absolutely(event, absolute_time)

    def schedule_absolutely(self, event, absolute_time):
        r'''Schedules `event` at `absolute_time` in seconds.

        Returns none.
        '''
        if absolute_time <= time.time():
            reschedule_time = event()
            if reschedule_time is not None:
                self.schedule(event, reschedule_time)
        with self._lock:
            if absolute_time < self._next_event_time or not self._queue:
                if self._timer is not None:
                    self._timer.cancel()
                self._queue.insert(0, (absolute_time, event))
                self._queue.sort(key=lambda x: x[0])
                self._new_timer()
            else:
                self._queue.append((absolute_time, event))
                self._queue.sort(key=lambda x: x[0])

    ### PUBLIC PROPERTIES ###

    @property
    def start_time(self):
        r'''Gets the start time of the clock.

        Returns float.
        '''
        return self._start_time

