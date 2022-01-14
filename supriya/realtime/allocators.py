import threading
from typing import Set

from uqbar.objects import new

from supriya.intervals import IntervalTree
from supriya.intervals.Interval import Interval
from supriya.system import SupriyaObject


class Block(Interval):

    ### CLASS VARIABLES ###

    __slots__ = ("_used",)

    ### INITIALIZER ###

    def __init__(
        self,
        start_offset: float = float("-inf"),
        stop_offset: float = float("inf"),
        used: bool = False,
    ):
        Interval.__init__(self, start_offset=start_offset, stop_offset=stop_offset)
        self._used = bool(used)

    ### PUBLIC PROPERTIES ###

    @property
    def used(self) -> bool:
        return self._used


class BlockAllocator(SupriyaObject):
    """
    A block allocator.

    ::

        >>> from supriya.realtime import BlockAllocator
        >>> allocator = BlockAllocator(
        ...     heap_maximum=16,
        ... )

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

    __slots__ = ("_free_heap", "_heap_maximum", "_heap_minimum", "_lock", "_used_heap")

    ### INITIALIZER ###

    def __init__(self, heap_maximum=None, heap_minimum=0):
        import supriya.realtime

        self._free_heap = IntervalTree(accelerated=True)
        self._heap_maximum = heap_maximum
        self._heap_minimum = heap_minimum
        self._lock = threading.Lock()
        self._used_heap = IntervalTree(accelerated=True)
        free_block = supriya.realtime.Block(
            start_offset=heap_minimum, stop_offset=heap_maximum, used=False
        )
        self._free_heap.add(free_block)

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
                        free_block, start_offset=split_offset, used=False
                    )
                    self._free_heap.add(new_free_block)
                    used_block = new(free_block, stop_offset=split_offset, used=True)
                else:
                    used_block = new(free_block, used=True)
                self._used_heap.add(used_block)
                block_id = used_block.start_offset
        if block_id is None:
            return block_id
        return int(block_id)

    def allocate_at(self, index=None, desired_block_size=1):
        import supriya.realtime

        index = int(index)
        desired_block_size = int(desired_block_size)
        block_id = None
        with self._lock:
            start_offset = index
            stop_offset = index + desired_block_size
            start_cursor = self._free_heap.get_moment_at(start_offset)
            starting_blocks = sorted(
                start_cursor.start_intervals + start_cursor.overlap_intervals
            )
            stop_cursor = self._free_heap.get_moment_at(stop_offset)
            stop_blocks = sorted(
                stop_cursor.overlap_intervals + stop_cursor.stop_intervals
            )
            if starting_blocks == stop_blocks:
                assert len(starting_blocks) == 1
                free_block = starting_blocks[0]
                used_block = supriya.realtime.Block(
                    start_offset=start_offset, stop_offset=stop_offset, used=True
                )
                self._used_heap.add(used_block)
                self._free_heap.remove(free_block)
                free_blocks = free_block - used_block
                for free_block in free_blocks:
                    self._free_heap.add(free_block)
                block_id = index
        if block_id is None:
            return block_id
        return int(block_id)

    def free(self, block_id):
        import supriya.realtime

        block_id = int(block_id)
        with self._lock:
            cursor = self._used_heap.get_moment_at(block_id)
            blocks = sorted(
                set(cursor.start_intervals) or set(cursor.overlap_intervals)
            )
            assert len(blocks) == 1
            used_block = blocks[0]
            self._used_heap.remove(used_block)
            start_offset = used_block.start_offset
            stopping_blocks = self._free_heap.find_intervals_stopping_at(start_offset)
            if stopping_blocks:
                assert len(stopping_blocks) == 1
                stopping_block = stopping_blocks[0]
                self._free_heap.remove(stopping_block)
                start_offset = stopping_block.start_offset
            stop_offset = used_block.stop_offset
            starting_blocks = self._free_heap.find_intervals_starting_at(stop_offset)
            if starting_blocks:
                assert len(starting_blocks) == 1
                starting_block = starting_blocks[0]
                self._free_heap.remove(starting_block)
                stop_offset = starting_block.stop_offset
            free_block = supriya.realtime.Block(
                start_offset=start_offset, stop_offset=stop_offset, used=False
            )
            self._free_heap.add(free_block)

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


class NodeIdAllocator(SupriyaObject):
    """
    A node ID allocator.

    ::

        >>> from supriya.realtime import NodeIdAllocator
        >>> allocator = NodeIdAllocator()
        >>> for _ in range(3):
        ...     allocator.allocate_node_id()
        ...
        1000
        1001
        1002

    ::

        >>> for _ in range(3):
        ...     allocator.allocate_permanent_node_id()
        ...
        1
        2
        3

    ::

        >>> allocator.free_permanent_node_id(2)

    ::

        >>> allocator.allocate_permanent_node_id()
        2

    """

    ### INITIALIZER ###

    def __init__(self, client_id: int = 0, initial_node_id: int = 1000):
        if client_id > 31:
            raise ValueError
        self._initial_node_id = initial_node_id
        self._client_id = client_id
        self._mask = self._client_id << 26
        self._temp = self._initial_node_id
        self._next_permanent_id = 1
        self._freed_permanent_ids: Set[int] = set()
        self._lock = threading.Lock()

    ### PUBLIC METHODS ###

    def allocate_node_id(self, count: int = 1) -> int:
        with self._lock:
            x = self._temp
            temp = x + count
            if 0x03FFFFFF < temp:
                temp = (temp % 0x03FFFFFF) + self._initial_node_id
            self._temp = temp
            x = x | self._mask
        return x

    def allocate_permanent_node_id(self) -> int:
        with self._lock:
            if self._freed_permanent_ids:
                x = min(self._freed_permanent_ids)
                self._freed_permanent_ids.remove(x)
            else:
                x = self._next_permanent_id
                self._next_permanent_id = min(x + 1, self._initial_node_id - 1)
            x = x | self._mask
        return x

    def free_permanent_node_id(self, node_id: int) -> None:
        with self._lock:
            node_id = node_id & 0x03FFFFFF
            if node_id < self._initial_node_id:
                self._freed_permanent_ids.add(node_id)
