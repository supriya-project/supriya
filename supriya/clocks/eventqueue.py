import queue

from .ephemera import Event


class EventQueue(queue.PriorityQueue[Event]):
    ### PRIVATE METHODS ###

    def _init(self, maxsize):
        self.queue = []
        self.items = {}

    def _put(self, item: Event):
        entry = [item, True]
        if item in self.items:
            self.items[item][-1] = False
        self.items[item] = entry
        super()._put(entry)

    def _get(self) -> Event:
        while self.queue:
            item, active = super()._get()
            if active:
                del self.items[item]
                return item
        raise queue.Empty

    ### PUBLIC METHODS ###

    def clear(self) -> None:
        with self.mutex:
            self._init(None)

    def peek(self) -> Event:
        with self.mutex:
            item = self._get()
            entry = [item, True]
            self.items[item] = entry
            super()._put(entry)
        return item

    def remove(self, item: Event) -> None:
        with self.mutex:
            entry = self.items.pop(item, None)
            if entry is not None:
                entry[-1] = False
