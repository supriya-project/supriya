from supriya.contexts.allocators import BlockAllocator


def test_allocate():
    allocator = BlockAllocator(heap_minimum=0, heap_maximum=16)
    assert allocator.allocate(4) == 0
    assert allocator.allocate(4) == 4
    assert allocator.allocate(4) == 8
    assert allocator.allocate(4) == 12
    assert allocator.allocate(4) is None
    allocator.free(0)
    allocator.free(4)
    allocator.free(8)
    allocator.free(12)
    assert allocator.allocate(20) is None
    assert allocator.allocate_at(4, 2) == 4
    assert allocator.allocate(4) == 0
    assert allocator.allocate(4) == 6
    allocator.free(4)
    assert allocator.allocate(1) == 4
    assert allocator.allocate(1) == 5


def test_allocate_block_within_block():
    allocator = BlockAllocator()
    assert allocator.allocate_at(0, 3) == 0
    assert allocator.allocate_at(0, 2) is None
    assert allocator.allocate_at(1, 2) is None
    assert allocator.allocate_at(2, 2) is None
    assert allocator.allocate_at(6, 3) == 6
    assert allocator.allocate_at(5, 2) is None
    assert allocator.allocate_at(2, 5) is None
    assert allocator.allocate_at(0, 9) is None
    assert allocator.allocate_at(3, 3) == 3
    assert allocator.free(99) is None
