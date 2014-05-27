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

        def __init__(self, start, size):
            self._start = start
            self._size = size
            self._used = False

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
            return type(self)(new_start, new_size)

        def split(self, span):
            if span < self.size:
                result = [
                    type(self)(self.start, span),
                    type(self)(self.start + span, self.size - span)
                    ]
            elif span == self.size:
                result = [self, None]
            else:
                result = []
            return result

        ### PUBLIC PROPERTIES ###

        @property
        def address(self):
            return self._start

        @property
        def start(self):
            return self._start

        @property
        def size(self):
            return self._size

        @property
        def stop(self):
            return self.start + self.size

    __slots__ = (
        '_size',
        '_array',
        '_freed',
        '_position',
        '_top',
        )

    ### INITIALIZER ###

    def __init__(self, size=None, position=0):
        self._size = size
        self._position = position

    ### PUBLIC METHODS ###

    def alloc(self, size=1):
        pass

    def reserve(self, address, size=1, warn=True):
        pass

    def free(self, address):
        pass

    @property
    def blocks(self):
        pass

