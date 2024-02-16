import queue
from typing import Dict, List, Optional

from .ephemera import Event


class EventQueue(queue.PriorityQueue[Event]):
    ### PRIVATE METHODS ###

    def _init(self, maxsize: Optional[int]) -> None:
        self.queue: List[Event] = []
        self.flags: Dict[Event, bool] = {}

    def _put(self, event: Event) -> None:
        self.flags[event] = True
        super()._put(event)

    def _get(self) -> Event:
        while self.queue:
            if not self.flags.pop((event := super()._get()), None):
                continue
            return event
        raise queue.Empty

    ### PUBLIC METHODS ###

    def clear(self) -> None:
        with self.mutex:
            self._init(None)

    def peek(self) -> Event:
        with self.mutex:
            self._put(event := self._get())
        return event

    def remove(self, event: Event) -> None:
        with self.mutex:
            self.flags.pop(event, None)
