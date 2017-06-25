try:
    from queue import PriorityQueue
except ImportError:
    from Queue import PriorityQueue
import time
import threading
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Clock(SupriyaObject):

    ### CLASS VARIABLES ###

    _default_clock = None

    __slots__ = (
        '_lock',
        '_queue',
        '_timer',
        '_registry',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._lock = threading.RLock()
        self._queue = PriorityQueue()
        self._timer = None
        self._registry = {}

    ### PRIVATE METHODS ###

    def _execute(self, execution_time):
        with self._lock:
            while not self._queue.empty():
                pair = self._queue.get()
                if execution_time < pair[0]:
                    self._queue.put(pair)
                    break
                scheduled_time, registry_key = pair
                if registry_key not in self._registry:
                    continue
                procedure = self._registry[registry_key]
                delta = procedure(execution_time, scheduled_time)
                if delta is not None:
                    rescheduled_time = scheduled_time + delta
                    self.schedule(
                        procedure,
                        rescheduled_time,
                        absolute=True,
                        registry_key=registry_key,
                        )
            if not self._queue.empty():
                self._new_timer()

    def _new_timer(self):
        if self._timer is not None:
            self._timer.cancel()
        pair = self._queue.get()
        self._queue.put(pair)
        scheduled_time, _ = pair
        now = time.time()
        delta = scheduled_time - now
        self._timer = threading.Timer(
            delta,
            self._execute,
            (scheduled_time,),
            )
        self._timer.start()

    ### PUBLIC METHODS ###

    def cancel(self, registry_key):
        with self._lock:
            if registry_key in self._registry:
                self._registry.pop(registry_key)

    @classmethod
    def get_default_clock(cls):
        if cls._default_clock is None:
            cls._default_clock = cls()
        return cls._default_clock

    def reset(self):
        with self._lock:
            if self._timer is not None:
                self._timer.cancel()
                self._timer = None
            self._registry.clear()
            self._queue = PriorityQueue()

    def schedule(
        self,
        procedure,
        scheduled_time=0.,
        absolute=False,
        registry_key=None,
        ):
        registry_key = registry_key or procedure
        now = time.time()
        if not absolute:
            scheduled_time += now
        with self._lock:
            if scheduled_time <= now:
                delta = procedure(now, scheduled_time)
                if delta is not None:
                    reschedule_time = delta + now
                    self.schedule(
                        procedure,
                        reschedule_time,
                        absolute=True,
                        registry_key=registry_key,
                        )
            else:
                self._registry[registry_key] = procedure
                self._queue.put((scheduled_time, registry_key))
                self._new_timer()
        return now
