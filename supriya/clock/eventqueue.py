import queue


class EventQueue(queue.PriorityQueue):

    ### PRIVATE METHODS ###

    def _init(self, maxsize):
        self.queue = []
        self.items = {}

    def _put(self, item):
        entry = [item, True]
        if item in self.items:
            self.items[item][-1] = False
        self.items[item] = entry
        super()._put(entry)

    def _get(self):
        while self.queue:
            item, active = super()._get()
            if active:
                del self.items[item]
                return item
        raise queue.Empty

    ### PUBLIC METHODS ###

    def clear(self):
        with self.mutex:
            self._init(None)

    def peek(self):
        with self.mutex:
            item = self._get()
            entry = [item, True]
            self.items[item] = entry
            super()._put(entry)
        return item

    def remove(self, item):
        with self.mutex:
            entry = self.items.pop(item, None)
            if entry is not None:
                entry[-1] = False
