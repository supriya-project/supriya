import threading
from supriya import utils
from supriya.system.SupriyaObject import SupriyaObject


class BlockAllocator(SupriyaObject):
    """
    A block allocator.

    ::

        >>> import supriya.realtime
        >>> allocator = supriya.realtime.BlockAllocator(
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

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Server Internals'

    __slots__ = (
        '_free_heap',
        '_heap_maximum',
        '_heap_minimum',
        '_lock',
        '_used_heap',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        heap_maximum=None,
        heap_minimum=0,
        ):
        import supriya.realtime
        import supriya.time
        self._free_heap = supriya.time.TimespanCollection(
            accelerated=True)
        self._heap_maximum = heap_maximum
        self._heap_minimum = heap_minimum
        self._lock = threading.Lock()
        self._used_heap = supriya.time.TimespanCollection(
            accelerated=True)
        free_block = supriya.realtime.Block(
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
                    new_free_block = utils.new(
                        free_block,
                        start_offset=split_offset,
                        used=False,
                        )
                    self._free_heap.insert(new_free_block)
                    used_block = utils.new(
                        free_block,
                        stop_offset=split_offset,
                        used=True,
                        )
                else:
                    used_block = utils.new(
                        free_block,
                        used=True,
                        )
                self._used_heap.insert(used_block)
                block_id = used_block.start_offset
        return block_id

    def allocate_at(self, index=None, desired_block_size=1):
        import supriya.realtime
        index = int(index)
        desired_block_size = int(desired_block_size)
        block_id = None
        with self._lock:
            start_offset = index
            stop_offset = index + desired_block_size
            start_cursor = self._free_heap.get_simultaneity_at(start_offset)
            starting_blocks = sorted(
                start_cursor.start_timespans +
                start_cursor.overlap_timespans
                )
            stop_cursor = self._free_heap.get_simultaneity_at(stop_offset)
            stop_blocks = sorted(
                stop_cursor.overlap_timespans +
                stop_cursor.stop_timespans
                )
            if starting_blocks == stop_blocks:
                assert len(starting_blocks) == 1
                free_block = starting_blocks[0]
                used_block = supriya.realtime.Block(
                    start_offset=start_offset,
                    stop_offset=stop_offset,
                    used=True,
                    )
                self._used_heap.insert(used_block)
                self._free_heap.remove(free_block)
                free_blocks = free_block - used_block
                for free_block in free_blocks:
                    self._free_heap.insert(free_block)
                block_id = index
        return block_id

    def free(self, block_id):
        import supriya.realtime
        block_id = int(block_id)
        with self._lock:
            cursor = self._used_heap.get_simultaneity_at(block_id)
            blocks = sorted(
                set(cursor.start_timespans) or
                set(cursor.overlap_timespans)
                )
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
            free_block = supriya.realtime.Block(
                start_offset=start_offset,
                stop_offset=stop_offset,
                used=False,
                )
            self._free_heap.insert(free_block)

    ### PUBLIC PROPERTIES ###

    @property
    def heap_maximum(self):
        """
        Maximum allocatable index.
        """
        return self._heap_maximum

    @property
    def heap_minimum(self):
        """
        Minimum allocatable index.
        """
        return self._heap_minimum
