import bisect
import dataclasses
import threading


@dataclasses.dataclass(order=True)
class Block:
    start_offset: int = 0
    stop_offset: int = 0

    @property
    def size(self) -> float:
        return self.stop_offset - self.start_offset


class BlockAllocator:
    """
    A block allocator.

    ::

        >>> from supriya.contexts.allocators import BlockAllocator
        >>> allocator = BlockAllocator(heap_maximum=16)

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

    def __init__(self, heap_maximum: int = 1024, heap_minimum: int = 0) -> None:
        self._used_dict: dict[int, Block] = {}
        self._free_heap: list[Block] = [
            Block(
                start_offset=heap_minimum,
                stop_offset=heap_maximum,
            )
        ]
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

    def allocate(self, size: int = 1) -> int | None:
        with self._lock:
            for i, block in enumerate(self._free_heap):
                if size <= block.size:
                    break
            else:
                return None
            if size < block.size:
                self._free_heap[i] = Block(
                    start_offset=block.start_offset + size,
                    stop_offset=block.stop_offset,
                )
            else:
                self._free_heap.pop(i)
            self._used_dict[block.start_offset] = Block(
                start_offset=block.start_offset,
                stop_offset=block.start_offset + size,
            )
            return int(block.start_offset)

    def free(self, index: int) -> None:
        with self._lock:
            if (block := self._used_dict.pop(index, None)) is None:
                return
            self._free_heap.insert(
                index := bisect.bisect(self._free_heap, block), block
            )
            # coalesce right
            if (
                index < (len(self._free_heap) - 1)
                and self._free_heap[index].stop_offset
                == self._free_heap[index + 1].start_offset
            ):
                self._free_heap[index].stop_offset = self._free_heap.pop(
                    index + 1
                ).stop_offset
            # coalesce left
            if (
                index > 0
                and self._free_heap[index].start_offset
                == self._free_heap[index - 1].stop_offset
            ):
                self._free_heap[index - 1].stop_offset = self._free_heap.pop(
                    index
                ).stop_offset


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
