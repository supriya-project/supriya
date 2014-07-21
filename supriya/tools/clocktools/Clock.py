# -*- encoding: utf-8 -*-
import time
import threading
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Clock(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_lock',
        '_next_event_time',
        '_queue',
        '_timer',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._lock = threading.RLock()
        self._next_event_time = 0
        self._queue = []
        self._timer = None

    ### PRIVATE METHODS ###

    def _execute(self, scheduled_time):
        print('TRYING TO EXECUTE')
        if scheduled_time != self._next_event_time:
            return
        with self._lock:
            now = time.time()
            events = []
            while self._queue and self._queue[0][0] <= scheduled_time:
                pair = self._queue.pop(0)
                events.append(pair[1])
            for event in events:
                print(event)
                event(self, now)
            self._new_timer()

    def _new_timer(self):
        print('NEW TIMER')
        now = time.time()
        scheduled_time = self._queue[0][0]
        delta = scheduled_time - now
        print('DELTA', delta)
        self._next_event_time = scheduled_time
        self._timer = threading.Timer(
            delta,
            self._execute,
            (scheduled_time,),
            )
        self._timer.start()

    ### PUBLIC METHODS ###

    def schedule(self, event, relative_time):
        absolute_time = time.time() + relative_time
        self.schedule_absolutely(event, absolute_time)

    def schedule_absolutely(self, event, absolute_time):
        from supriya.tools import clocktools
        event = clocktools.Event(
            scheduled_time=absolute_time,
            payload=event,
            )
        now = time.time()
        if absolute_time <= now:
            event(self, now)
            return
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