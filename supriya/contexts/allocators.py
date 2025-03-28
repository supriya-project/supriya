import dataclasses
import threading

from ..utils import Interval, IntervalTree


@dataclasses.dataclass(frozen=True)
class Block(Interval):
    start_offset: float = float("-inf")
    stop_offset: float = float("inf")
    used: bool = False


class BlockAllocator:
    """
    A block allocator.

    ::

        >>> from supriya.contexts.allocators import BlockAllocator
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

    ### INITIALIZER ###

    def __init__(self, heap_maximum: int | None = None, heap_minimum: int = 0) -> None:
        self._free_heap = IntervalTree(accelerated=True)
        self._heap_maximum = heap_maximum
        self._heap_minimum = heap_minimum
        self._lock = threading.Lock()
        self._used_heap = IntervalTree(accelerated=True)
        free_block = Block(
            start_offset=heap_minimum,
            stop_offset=heap_maximum or float("inf"),
            used=False,
        )
        self._free_heap.add(free_block)

    ### SPECIAL METHODS ###

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        del state["_lock"]
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self._lock = threading.Lock()

    ### PUBLIC METHODS ###

    def allocate(self, desired_block_size: int = 1) -> int | None:
        desired_block_size = int(desired_block_size)
        if desired_block_size <= 0:
            raise ValueError("desired_block_size must be greater than zero")
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
                    new_free_block = dataclasses.replace(
                        free_block, start_offset=split_offset, used=False
                    )
                    self._free_heap.add(new_free_block)
                    used_block = dataclasses.replace(
                        free_block, stop_offset=split_offset, used=True
                    )
                else:
                    used_block = dataclasses.replace(free_block, used=True)
                self._used_heap.add(used_block)
                block_id = used_block.start_offset
        return int(block_id) if block_id is not None else None

    def allocate_at(self, index: int, desired_block_size: int = 1) -> int | None:
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
                if len(starting_blocks) == 0:
                    return None
                if len(starting_blocks) != 1:
                    raise RuntimeError
                free_block = starting_blocks[0]
                used_block = Block(
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

    def free(self, block_id: int) -> None:
        block_id = int(block_id)
        with self._lock:
            cursor = self._used_heap.get_moment_at(block_id)
            blocks = sorted(
                set(cursor.start_intervals) or set(cursor.overlap_intervals)
            )
            if len(blocks) == 0:
                return None
            if len(blocks) != 1:
                raise RuntimeError
            used_block = blocks[0]
            self._used_heap.remove(used_block)
            start_offset = used_block.start_offset
            stopping_blocks = self._free_heap.find_intervals_stopping_at(start_offset)
            if stopping_blocks:
                if len(stopping_blocks) != 1:
                    raise RuntimeError
                stopping_block = stopping_blocks[0]
                self._free_heap.remove(stopping_block)
                start_offset = stopping_block.start_offset
            stop_offset = used_block.stop_offset
            starting_blocks = self._free_heap.find_intervals_starting_at(stop_offset)
            if starting_blocks:
                if len(starting_blocks) != 1:
                    raise RuntimeError
                starting_block = starting_blocks[0]
                self._free_heap.remove(starting_block)
                stop_offset = starting_block.stop_offset
            free_block = Block(
                start_offset=start_offset, stop_offset=stop_offset, used=False
            )
            self._free_heap.add(free_block)

    ### PUBLIC PROPERTIES ###

    @property
    def heap_maximum(self) -> int | None:
        """
        Maximum allocatable index.
        """
        return self._heap_maximum

    @property
    def heap_minimum(self) -> int:
        """
        Minimum allocatable index.
        """
        return self._heap_minimum


class NodeIdAllocator:
    """
    A node ID allocator.

    ::

        >>> from supriya.contexts.allocators import NodeIdAllocator
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

    def __init__(
        self, client_id: int = 0, initial_node_id: int = 1000, locked=True
    ) -> None:
        if client_id > 31:
            raise ValueError
        self._initial_node_id = initial_node_id
        self._client_id = client_id
        self._mask = self._client_id << 26
        self._temp = self._initial_node_id
        self._next_permanent_id = 1
        self._freed_permanent_ids: set[int] = set()
        self._lock = threading.Lock()

    ### SPECIAL METHODS ###

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        del state["_lock"]
        return state

    def __setstate__(self, state: dict) -> None:
        self.__dict__.update(state)
        self._lock = threading.Lock()

    ### PUBLIC METHODS ###

    def allocate(self, count: int = 1) -> int:
        return self.allocate_node_id(count)

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

    def free(self, node_id: int) -> None:
        if node_id < self._initial_node_id:
            self.free_permanent_node_id(node_id)

    def free_permanent_node_id(self, node_id: int) -> None:
        with self._lock:
            node_id = node_id & 0x03FFFFFF
            if node_id < self._initial_node_id:
                self._freed_permanent_ids.add(node_id)
