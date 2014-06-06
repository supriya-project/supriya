class ContiguousBlockAllocator(object):

    ### CLASS VARIABLES ###

    class ContiguousBlock(object):

        ### CLASS VARIABLES ###

        __slots__ = (
            '_start',
            '_size',
            '_used',
            )

        ### INITIALIZER ###

        def __init__(self, start, size, used=False):
            self._start = int(start)
            self._size = int(size)
            self._used = bool(used)

        ### PUBLIC METHODS ###

        def adjoins(self, block):
            if self.start < block.start and block.start <= self.stop:
                return True
            elif block.start < self.start and self.start <= block.stop:
                return True
            return False

        def join(self, block):
            if not self.adjoins(block):
                return None
            new_start = min(self.start, block.start)
            new_size = max(self.stop, block.stop) - new_start
            return type(self)(new_start, new_size, used=self.used)

        def split(self, size):
            if size < self.size:
                result = [
                    type(self)(
                        self.start,
                        size,
                        used=self.used,
                        ),
                    type(self)(
                        self.start + size,
                        self.size - size,
                        used=self.used,
                        )
                    ]
            elif size == self.size:
                result = [self, None]
            else:
                result = []
            return result

        ### PUBLIC PROPERTIES ###

        @property
        def start(self):
            return self._start

        @property
        def size(self):
            return self._size

        @property
        def stop(self):
            return self.start + self.size

        @property
        def used(self):
            return self._used

        @used.setter
        def used(self, expr):
            self._used = bool(expr)

    __slots__ = (
        '_size',
        '_blocks',
        '_freed_blocks',
        '_initial_position',
        '_maximum_position',
        )

    ### INITIALIZER ###

    def __init__(self, size=None, initial_position=0):
        self._blocks = {}
        self._freed_blocks = {}
        self._initial_position = initial_position
        self._maximum_position = initial_position
        self._size = size

    ### PUBLIC METHODS ###

    def allocate(self, size=1):
        pass

    def free(self, position):
        pass
