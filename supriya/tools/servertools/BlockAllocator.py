# -*- encoding: utf-8 -*-
import threading
from abjad.tools.topleveltools import new
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class BlockAllocator(SupriyaObject):
    r'''A block allocator.

    ::

        >>> from supriya.tools import servertools
        >>> allocator = servertools.BlockAllocator(
        ...     heap_maximum=16,
        ...     )

    ::

        >>> allocator.allocate(4)
        0

    ::

        >>> allocator.allocate(4)
        4

    ::

        >>> allocator.allocate(4)
        8

    ::

        >>> allocator.allocate(8) is None
        True

    ::

        >>> allocator.free(8)
        >>> allocator.allocate(8)
        8

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

    def allocate(self, desired_block_size=1):
        desired_block_size = int(desired_block_size)
        assert 0 < desired_block_size
        block_id = None
        with self._lock:
            free_block = None
            for block in self._free_heap:
                if desired_block_size <= block.duration:
                    free_block = block
                    break
            if free_block is not None:
                split_offset = free_block.start_offset + desired_block_size
                self._free_heap.remove(free_block)
                if desired_block_size < free_block.duration:
                    new_free_block = new(
                        free_block,
                        start_offset=split_offset,
                        used=False,
                        )
                    self._free_heap.insert(new_free_block)
                    used_block = new(
                        free_block,
                        stop_offset=split_offset,
                        used=True,
                        )
                else:
                    used_block = new(
                        free_block,
                        used=True,
                        )
                self._used_heap.insert(used_block)
                block_id = used_block.start_offset
        if self.id_class is not None:
            block_id = self.id_class(
                server=self.server,
                value=block_id,
                )
        return block_id

    def free(self, block_id):
        from supriya.tools import servertools
        if self.id_class is not None and isinstance(block_id, self.id_class):
            block_id = block_id.value
        elif not isinstance(block_id, int):
            raise ValueError
        with self._lock:
            cursor = self._used_heap.get_simultaneity_at(block_id)
            blocks = cursor.start_timespans + cursor.overlap_timespans
            assert len(blocks) == 1
            used_block = blocks[0]
            self._used_heap.remove(used_block)
            start_offset = used_block.start_offset
            stopping_blocks = self._free_heap.find_timespans_stopping_at(
                start_offset)
            if stopping_blocks:
                assert len(stopping_blocks) == 1
                stopping_block = stopping_blocks[0]
                self._free_heap.remove(stopping_block)
                start_offset = stopping_block.start_offset
            stop_offset = used_block.stop_offset
            starting_blocks = self._free_heap.find_timespans_starting_at(
                stop_offset)
            if starting_blocks:
                assert len(starting_blocks) == 1
                starting_block = starting_blocks[0]
                self._free_heap.remove(starting_block)
                stop_offset = starting_block.stop_offset
            free_block = servertools.Block(
                start_offset=start_offset,
                stop_offset=stop_offset,
                used=False,
                )
            self._free_heap.insert(free_block)

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
