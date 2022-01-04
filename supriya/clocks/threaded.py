import atexit
import logging
import queue
import threading
from typing import Optional, Tuple

from .bases import BaseClock
from .ephemera import Moment

logger = logging.getLogger("supriya.clocks")


class Clock(BaseClock):

    ### CLASS VARIABLES ###

    _default_clock = None

    ### INITIALIZER ###

    def __init__(self):
        BaseClock.__init__(self)
        self._event = threading.Event()
        self._thread = threading.Thread(target=self._run, daemon=True)
        atexit.register(self.stop)

    ### SCHEDULING METHODS ###

    def _enqueue_command(self, command):
        super()._enqueue_command(command)
        self._event.set()

    def _run(self, *args, offline=False, **kwargs):
        logger.debug(f"[{self.name}] Thread start")
        self._process_command_deque(first_run=True)
        while self._is_running:
            logger.debug(f"[{self.name}] Loop start")
            if not self._wait_for_queue():
                return
            try:
                current_moment = self._wait_for_moment()
            except queue.Empty:
                continue
            if current_moment is None:
                return
            current_moment = self._perform_events(current_moment)
            self._state = self._state._replace(
                previous_seconds=current_moment.seconds,
                previous_offset=current_moment.offset,
            )
            if not offline:
                self._event.wait(timeout=self._slop)
        logger.debug(f"[{self.name}] Terminating")

    def _wait_for_moment(self, offline=False) -> Optional[Moment]:
        current_time = self.get_current_time()
        next_time = self._event_queue.peek().seconds
        logger.debug(
            f"[{self.name}] ... Waiting for next moment at {next_time} from {current_time}"
        )
        while current_time < next_time:
            if not offline:
                self._event.wait(timeout=self._slop)
            if not self._is_running:
                return None
            self._process_command_deque()
            next_time = self._event_queue.peek().seconds
            current_time = self.get_current_time()
            self._event.clear()
        return self._seconds_to_moment(current_time)

    def _wait_for_queue(self, offline=False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        self._event.clear()
        while not self._event_queue.qsize():
            if not offline:
                self._event.wait(timeout=self._slop)
            if not self._is_running:
                return False
            self._process_command_deque()
            self._event.clear()
        return True

    ### PUBLIC METHODS ###

    def cancel(self, event_id) -> Optional[Tuple]:
        event = super().cancel(event_id)
        self._event.set()
        return event

    @classmethod
    def default(cls):
        if cls._default_clock is None:
            cls._default_clock = cls()
        return cls._default_clock

    def start(
        self,
        initial_time: Optional[float] = None,
        initial_offset: float = 0.0,
        initial_measure: int = 1,
        beats_per_minute: Optional[float] = None,
        time_signature: Optional[Tuple[int, int]] = None,
    ):
        self._start(
            initial_time=initial_time,
            initial_offset=initial_offset,
            initial_measure=initial_measure,
            beats_per_minute=beats_per_minute,
            time_signature=time_signature,
        )
        self._thread = threading.Thread(target=self._run, args=(self,), daemon=True)
        self._thread.start()

    def stop(self):
        if self._stop():
            self._event.set()
            self._thread.join()
