from dataclasses import dataclass
from typing import Optional, Tuple

import hypothesis
import hypothesis.strategies as st

import supriya.realtime
from tests.proptest import hp_global_settings

hp_settings = hypothesis.settings(hp_global_settings, max_examples=200)


@dataclass
class SampleBlockAllocator:
    allocator: supriya.realtime.BlockAllocator
    heap_minimum: int = 0
    heap_maximum: int = 1048576
    heap_min_size: int = 64
    block_sizes: Tuple[int] = (0,)
    allocate_at_indices: Tuple[int] = (0,)
    free_at_indices: Tuple[int] = (0,)


@st.composite
def st_block_allocator(
    draw, min_blocks_num: int = 1, max_block_size: Optional[int] = None
) -> SampleBlockAllocator:

    heap_minimum = draw(
        st.integers(
            min_value=SampleBlockAllocator.heap_minimum,
            max_value=SampleBlockAllocator.heap_maximum
            - SampleBlockAllocator.heap_min_size,
        )
    )
    heap_maximum = draw(
        st.integers(
            min_value=heap_minimum + SampleBlockAllocator.heap_min_size,
            max_value=SampleBlockAllocator.heap_maximum,
        )
    )
    allocator = supriya.realtime.BlockAllocator(
        heap_minimum=heap_minimum, heap_maximum=heap_maximum
    )

    sample = SampleBlockAllocator(
        allocator, heap_minimum=heap_minimum, heap_maximum=heap_maximum
    )

    if not max_block_size:
        max_block_size = heap_maximum - heap_minimum
    sample.block_sizes = tuple(
        draw(
            st.lists(
                st.integers(min_value=1, max_value=max_block_size),
                min_size=min_blocks_num,
            )
        )
    )
    st_indices = st.lists(
        st.integers(min_value=heap_minimum, max_value=heap_maximum),
        min_size=min_blocks_num,
    )
    sample.allocate_at_indices = tuple(draw(st_indices))
    sample.free_at_indices = tuple(draw(st_indices))

    return sample


@hypothesis.settings(hp_settings)
@hypothesis.given(sample=st_block_allocator())
def test_allocate_continuous(sample):

    available_indices = sample.heap_maximum - sample.heap_minimum
    allocated_blocks = 0
    for size in sample.block_sizes:
        result = sample.allocator.allocate(size)
        if allocated_blocks + size > available_indices:
            assert result is None
            break
        else:
            assert result == sample.heap_minimum + allocated_blocks
        allocated_blocks += size


@hypothesis.settings(hp_settings)
@hypothesis.given(sample=st_block_allocator(min_blocks_num=16, max_block_size=512))
def test_allocate_at(sample):

    available_indices = {
        _: True for _ in range(sample.heap_minimum, sample.heap_maximum)
    }
    for size, index in zip(sample.block_sizes, sample.allocate_at_indices):
        hypothesis.assume(index + size <= sample.heap_maximum)
        result = sample.allocator.allocate_at(index, size)
        if not all(available_indices[_] for _ in range(index, index + size)):
            assert result is None
        else:
            assert result == index
            available_indices.update({_: False for _ in range(index, index + size)})


@hypothesis.settings(hp_settings, deadline=None)
@hypothesis.given(sample=st_block_allocator(min_blocks_num=16, max_block_size=512))
def test_allocate_at_and_free(sample):

    available_indices = {
        _: True for _ in range(sample.heap_minimum, sample.heap_maximum)
    }
    allocated_ranges = []
    for size, index_allocate, index_free in zip(
        sample.block_sizes, sample.allocate_at_indices, sample.free_at_indices
    ):
        hypothesis.assume(index_allocate + size <= sample.heap_maximum)
        result = sample.allocator.allocate_at(index_allocate, size)
        if not all(
            available_indices[_] for _ in range(index_allocate, index_allocate + size)
        ):
            assert result is None
        else:
            assert result == index_allocate
            available_indices.update(
                {_: False for _ in range(index_allocate, index_allocate + size)}
            )
            allocated_ranges.append((index_allocate, index_allocate + size))

        sample.allocator.free(index_free)
        if index_free in (_ for _ in available_indices if not available_indices[_]):
            for ran in allocated_ranges:
                if index_free in range(*ran):
                    available_indices.update({_: True for _ in range(*ran)})
                    allocated_ranges.remove(ran)
                    break
