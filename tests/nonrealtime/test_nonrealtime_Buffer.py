import platform

import pytest

import supriya.nonrealtime
import supriya.soundfiles


def test_attributes():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_one = session.add_buffer(frame_count=512)
    with session.at(5):
        buffer_two = session.add_buffer(channel_count=2, duration=10)
    # buffer one
    assert buffer_one.buffer_group is None
    assert buffer_one.channel_count == 1
    assert buffer_one.duration == float("inf")
    assert buffer_one.frame_count == 512
    assert buffer_one.session is session
    assert buffer_one.start_offset == 0
    assert buffer_one.stop_offset == float("inf")
    # buffer two
    assert buffer_two.buffer_group is None
    assert buffer_two.channel_count == 2
    assert buffer_two.duration == 10
    assert buffer_two.frame_count == 1
    assert buffer_two.session is session
    assert buffer_two.start_offset == 5
    assert buffer_two.stop_offset == 15
    assert session.offsets == [float("-inf"), 0, 5, 15, float("inf")]
    assert session.to_lists(duration=20) == [
        [0.0, [["/b_alloc", 0, 512, 1]]],
        [5.0, [["/b_alloc", 1, 1, 2]]],
        [15.0, [["/b_free", 1]]],
        [20.0, [["/b_free", 0], [0]]],
    ]


def test_alloc_read():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.add_buffer(file_path="foo.aiff")
    with session.at(1):
        session.add_buffer(file_path="bar.aiff", frame_count=512, starting_frame=53)
    assert session.to_lists(duration=2) == [
        [0.0, [["/b_allocRead", 0, "foo.aiff", 0, -1]]],
        [1.0, [["/b_allocRead", 1, "bar.aiff", 53, 512]]],
        [2.0, [["/b_free", 0], ["/b_free", 1], [0]]],
    ]


def test_alloc_read_session():
    input_session = pytest.helpers.make_test_session()
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.add_buffer(file_path=input_session)
    assert session.to_lists(duration=2) == [
        [
            0.0,
            [
                [
                    "/b_allocRead",
                    0,
                    "session-7b3f85710f19667f73f745b8ac8080a0.aiff",
                    0,
                    -1,
                ]
            ],
        ],
        [2.0, [["/b_free", 0], [0]]],
    ]


@pytest.mark.skipif(platform.system() == "Windows", reason="requires say/espeak")
def test_alloc_read_say():
    say = supriya.soundfiles.Say("Some text.")
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.add_buffer(file_path=say)
    assert session.to_lists(duration=2) == [
        [
            0.0,
            [["/b_allocRead", 0, "say-5f2b51ca2fdc5baa31ec02e002f69aec.aiff", 0, -1]],
        ],
        [2.0, [["/b_free", 0], [0]]],
    ]


def test_alloc_read_channel():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        session.add_buffer(file_path="foo.aiff", channel_count=(1, 3))
    with session.at(1):
        session.add_buffer(
            channel_count=(0, 2, 4, 6),
            file_path="bar.aiff",
            frame_count=512,
            starting_frame=53,
        )
    with session.at(2):
        session.add_buffer(
            channel_count=8,  # Behavior is subtly different from /b_readChannel
            file_path="baz.aiff",
        )
    assert session.to_lists(duration=3) == [
        [0.0, [["/b_allocReadChannel", 0, "foo.aiff", 0, -1, 1, 3]]],
        [1.0, [["/b_allocReadChannel", 1, "bar.aiff", 53, 512, 0, 2, 4, 6]]],
        [2.0, [["/b_allocReadChannel", 2, "baz.aiff", 0, -1, 0, 1, 2, 3, 4, 5, 6, 7]]],
        [3.0, [["/b_free", 0], ["/b_free", 1], ["/b_free", 2], [0]]],
    ]


def test_copy():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_group = session.add_buffer_group(buffer_count=2, frame_count=512)
    with session.at(1):
        buffer_group[0].copy(
            buffer_group[1],
            frame_count=256,
            source_starting_frame=128,
            target_starting_frame=64,
        )
    assert session.to_lists(duration=2) == [
        [0.0, [["/b_alloc", 0, 512, 1], ["/b_alloc", 1, 512, 1]]],
        [1.0, [["/b_gen", 1, "copy", 64, 0, 128, 256]]],
        [2.0, [["/b_free", 0], ["/b_free", 1], [0]]],
    ]


def test_fill():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_ = session.add_buffer(frame_count=512)
    with session.at(1):
        buffer_.fill([(0, 64, 0.5), (64, 256, 0.25)])
    assert session.to_lists(duration=2) == [
        [0.0, [["/b_alloc", 0, 512, 1]]],
        [1.0, [["/b_fill", 0, 0, 64, 0.5, 64, 256, 0.25]]],
        [2.0, [["/b_free", 0], [0]]],
    ]


def test_fill_via_chebyshev():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_one = session.add_buffer(frame_count=512)
        buffer_two = session.add_buffer(frame_count=512)
    with session.at(1):
        buffer_one.fill_via_chebyshev([1, 2, 3])
        buffer_two.fill_via_chebyshev([0.75, 0.5], False, False, False)
    assert session.to_lists(duration=2) == [
        [0.0, [["/b_alloc", 0, 512, 1], ["/b_alloc", 1, 512, 1]]],
        [
            1.0,
            [
                ["/b_gen", 0, "cheby", 7, 1.0, 2.0, 3.0],
                ["/b_gen", 1, "cheby", 0, 0.75, 0.5],
            ],
        ],
        [2.0, [["/b_free", 0], ["/b_free", 1], [0]]],
    ]


def test_fill_sine_1():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_one = session.add_buffer(frame_count=512)
        buffer_two = session.add_buffer(frame_count=512)
    with session.at(1):
        buffer_one.fill_via_sine_1([1, 2, 3])
        buffer_two.fill_via_sine_1([0.75, 0.5], False, False, False)
    assert session.to_lists(duration=2) == [
        [0.0, [["/b_alloc", 0, 512, 1], ["/b_alloc", 1, 512, 1]]],
        [
            1.0,
            [
                ["/b_gen", 0, "sine1", 7, 1.0, 2.0, 3.0],
                ["/b_gen", 1, "sine1", 0, 0.75, 0.5],
            ],
        ],
        [2.0, [["/b_free", 0], ["/b_free", 1], [0]]],
    ]


def test_fill_sine_2():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_one = session.add_buffer(frame_count=512)
        buffer_two = session.add_buffer(frame_count=512)
    with session.at(1):
        buffer_one.fill_via_sine_2([1, 2, 3], [4, 5, 6])
        buffer_two.fill_via_sine_2([0.75, 0.5], [7, 8], False, False, False)
    assert session.to_lists(duration=2) == [
        [0.0, [["/b_alloc", 0, 512, 1], ["/b_alloc", 1, 512, 1]]],
        [
            1.0,
            [
                ["/b_gen", 0, "sine2", 7, 4.0, 1.0, 5.0, 2.0, 6.0, 3.0],
                ["/b_gen", 1, "sine2", 0, 7.0, 0.75, 8.0, 0.5],
            ],
        ],
        [2.0, [["/b_free", 0], ["/b_free", 1], [0]]],
    ]


def test_fill_sine_3():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_one = session.add_buffer(frame_count=512)
        buffer_two = session.add_buffer(frame_count=512)
    with session.at(1):
        buffer_one.fill_via_sine_3([1, 2, 3], [4, 5, 6], [0.1, 0.2, 0.3])
        buffer_two.fill_via_sine_3([0.75, 0.5], [7, 8], [0.8, 0.6], False, False, False)
    assert session.to_lists(duration=2) == [
        [0.0, [["/b_alloc", 0, 512, 1], ["/b_alloc", 1, 512, 1]]],
        [
            1.0,
            [
                ["/b_gen", 0, "sine3", 7, 4.0, 1.0, 0.1, 5.0, 2.0, 0.2, 6.0, 3.0, 0.3],
                ["/b_gen", 1, "sine3", 0, 7.0, 0.75, 0.8, 8.0, 0.5, 0.6],
            ],
        ],
        [2.0, [["/b_free", 0], ["/b_free", 1], [0]]],
    ]


def test_read():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_one = session.add_buffer(frame_count=1024)
        buffer_two = session.add_buffer(frame_count=512)
    with session.at(1):
        buffer_one.read(
            file_path="foo.aiff",
            frame_count=256,
            starting_frame_in_buffer=64,
            starting_frame_in_file=23,
        )
    with session.at(2):
        buffer_two.read(file_path="bar.aiff", leave_open=True)
    assert session.to_lists(duration=3) == [
        [0.0, [["/b_alloc", 0, 1024, 1], ["/b_alloc", 1, 512, 1]]],
        [1.0, [["/b_read", 0, "foo.aiff", 23, 256, 64, 0]]],
        [2.0, [["/b_read", 1, "bar.aiff", 0, -1, 0, 1]]],
        [3.0, [["/b_free", 0], ["/b_close", 1], ["/b_free", 1], [0]]],
    ]


def test_read_channel():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_one = session.add_buffer(frame_count=1024)
        buffer_two = session.add_buffer(frame_count=512)
    with session.at(1):
        buffer_one.read(
            channel_indices=2,
            file_path="foo.aiff",
            frame_count=256,
            starting_frame_in_buffer=64,
            starting_frame_in_file=23,
        )
    with session.at(2):
        buffer_two.read(
            channel_indices=(1, 3, 5, 7), file_path="bar.aiff", leave_open=True
        )
    assert session.to_lists(duration=3) == [
        [0.0, [["/b_alloc", 0, 1024, 1], ["/b_alloc", 1, 512, 1]]],
        [1.0, [["/b_readChannel", 0, "foo.aiff", 23, 256, 64, 0, 2]]],
        [2.0, [["/b_readChannel", 1, "bar.aiff", 0, -1, 0, 1, 1, 3, 5, 7]]],
        [3.0, [["/b_free", 0], ["/b_close", 1], ["/b_free", 1], [0]]],
    ]


def test_set():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_ = session.add_buffer(frame_count=512)
    with session.at(1):
        buffer_.set([(64, 0.5), (128, 0.75)])
    assert session.to_lists(duration=2) == [
        [0.0, [["/b_alloc", 0, 512, 1]]],
        [1.0, [["/b_set", 0, 64, 0.5, 128, 0.75]]],
        [2.0, [["/b_free", 0], [0]]],
    ]


def test_set_contiguous():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_ = session.add_buffer(frame_count=512)
    with session.at(1):
        buffer_.set_contiguous([(0, (1, 2, 3)), (128, (1, 2, 3))])
    assert session.to_lists(duration=2) == [
        [0.0, [["/b_alloc", 0, 512, 1]]],
        [1.0, [["/b_setn", 0, 0, 3, 1.0, 2.0, 3.0, 128, 3, 1.0, 2.0, 3.0]]],
        [2.0, [["/b_free", 0], [0]]],
    ]


def test_write():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_one = session.add_buffer(frame_count=512)
        buffer_two = session.add_buffer(frame_count=2048)
    with session.at(1):
        buffer_one.write(file_path="foo.aiff", frame_count=128, starting_frame=256)
    with session.at(2):
        buffer_two.write(file_path="bar.aiff", leave_open=True)
    assert session.to_lists(duration=3) == [
        [0.0, [["/b_alloc", 0, 512, 1], ["/b_alloc", 1, 2048, 1]]],
        [1.0, [["/b_write", 0, "foo.aiff", "aiff", "int24", 128, 256, 0]]],
        [2.0, [["/b_write", 1, "bar.aiff", "aiff", "int24", -1, 0, 1]]],
        [3.0, [["/b_free", 0], ["/b_close", 1], ["/b_free", 1], [0]]],
    ]


def test_zero():
    session = supriya.nonrealtime.Session()
    with session.at(0):
        buffer_one = session.add_buffer(duration=9, frame_count=512)
    with session.at(3):
        buffer_two = session.add_buffer(duration=9, frame_count=512)
    with session.at(6):
        buffer_one.zero()
        buffer_two.zero()
    assert session.to_lists(duration=12) == [
        [0.0, [["/b_alloc", 0, 512, 1]]],
        [3.0, [["/b_alloc", 1, 512, 1]]],
        [6.0, [["/b_zero", 0], ["/b_zero", 1]]],
        [9.0, [["/b_free", 0]]],
        [12.0, [["/b_free", 1], [0]]],
    ]
