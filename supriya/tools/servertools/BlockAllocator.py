# -*- encoding: utf-8 -*-
import threading
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BlockAllocator(SupriyaObject):
    r'''A block allocator.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_free_heap',
        '_heap_maximum',
        '_heap_minimum',
        '_id_class',
        '_lock',
        '_server',
        '_used_heap',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        heap_maximum=None,
        heap_minimum=0,
        id_class=None,
        server=None,
        ):
        from supriya.tools import servertools
        from supriya.tools import timetools
        self._free_heap = timetools.TimespanCollection()
        self._heap_maximum = heap_maximum
        self._heap_minimum = heap_minimum
        self._id_class = id_class
        self._lock = threading.Lock()
        self._server = server
        self._used_heap = timetools.TimespanCollection()
        free_block = servertools.Block(
            start_offset=heap_minimum,
            stop_offset=heap_maximum,
            used=False,
            )
        self._free_heap.insert(free_block)

    ### PUBLIC METHODS ###

    def allocate(self, block_size=1):
        block_size = int(block_size)
        assert 0 < block_size
        with self._lock:
            pass

    def free(self, block_id):
        with self._lock:
            pass

    ### PUBLIC PROPERTIES ###

    @property
    def heap_maximum(self):
        return self._heap_maximum

    @property
    def heap_minimum(self):
        return self._heap_minimum

    @property
    def id_class(self):
        return self._id_class

    @property
    def server(self):
        return self._server
