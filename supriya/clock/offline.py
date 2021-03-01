import logging
import queue
from typing import Optional, Tuple

from .bases import BaseTempoClock
from .ephemera import Moment

logger = logging.getLogger("supriya.clock")


class OfflineTempoClock(BaseTempoClock):
    def __init__(self, require_step=False):
        super().__init__()
        self.require_step = bool(require_step)

    ### SCHEDULING METHODS ###

    def _run(self, *args, offline=False, **kwargs):
        logger.debug(f"[{self.name}] Thread start")
        self._process_command_deque(first_run=True)
        while self._is_running and self._event_queue.qsize():
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
        logger.debug(f"[{self.name}] Terminating")

    def _wait_for_moment(self, offline=False) -> Optional[Moment]:
        current_time = self._event_queue.peek().seconds
        return self._seconds_to_moment(current_time)

    def _wait_for_queue(self, offline=False) -> bool:
        logger.debug(f"[{self.name}] ... Waiting for events")
        self._process_command_deque()
        while not self._event_queue.qsize():
            if not self._is_running:
                return False
            self._process_command_deque()
        return True

    ### PUBLIC METHODS ###

    def get_current_time(self) -> float:
        if not self._is_running:
            return 0.0
        return self._state.previous_seconds

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
        self._run()

    def stop(self):
        self._stop()
