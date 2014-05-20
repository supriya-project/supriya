class ContiguousBlockAllocator(object):

    ### CLASS VARIABLES ###

    class ContiguousBlock(object):
        pass

    __slots__ = (
        '_size',
        '_array',
        '_freed',
        '_position',
        '_top',
        )

    ### INITIALIZER ###

    def __init__(self, size, position=0):
        self._size = size
        self._position = position
