import supriya.realtime


def test_allocate():

    allocator = supriya.realtime.BlockAllocator(heap_minimum=0, heap_maximum=16)

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
