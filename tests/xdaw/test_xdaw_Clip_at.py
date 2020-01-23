from supriya.xdaw import Clip, Note, NoteMoment

offsets = [-0.5, 0, 0.125, 0.25, 0.5, 0.75, 1, 1.25, 2.25]


def test_1():
    clip = Clip()
    assert [clip.at(offset) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-0.5, next_offset=1.0),
        NoteMoment(offset=0, local_offset=0.0, next_offset=1.0),
        NoteMoment(offset=0.125, local_offset=0.125, next_offset=1.0),
        NoteMoment(offset=0.25, local_offset=0.25, next_offset=1.0),
        NoteMoment(offset=0.5, local_offset=0.5, next_offset=1.0),
        NoteMoment(offset=0.75, local_offset=0.75, next_offset=1.0),
        NoteMoment(offset=1, local_offset=0.0, next_offset=2.0),
        NoteMoment(offset=1.25, local_offset=0.25, next_offset=2.0),
        NoteMoment(offset=2.25, local_offset=0.25, next_offset=3.0),
    ]
    assert [clip.at(offset, force_stop=True) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-0.5),
        NoteMoment(offset=0, local_offset=0.0),
        NoteMoment(offset=0.125, local_offset=0.125),
        NoteMoment(offset=0.25, local_offset=0.25),
        NoteMoment(offset=0.5, local_offset=0.5),
        NoteMoment(offset=0.75, local_offset=0.75),
        NoteMoment(offset=1, local_offset=0.0),
        NoteMoment(offset=1.25, local_offset=0.25),
        NoteMoment(offset=2.25, local_offset=0.25),
    ]
    assert [clip.at(offset, start_delta=0.5) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-1.0, next_offset=1.5),
        NoteMoment(offset=0, local_offset=-0.5, next_offset=1.5),
        NoteMoment(offset=0.125, local_offset=-0.375, next_offset=1.5),
        NoteMoment(offset=0.25, local_offset=-0.25, next_offset=1.5),
        NoteMoment(offset=0.5, local_offset=0.0, next_offset=1.5),
        NoteMoment(offset=0.75, local_offset=0.25, next_offset=1.5),
        NoteMoment(offset=1, local_offset=0.5, next_offset=1.5),
        NoteMoment(offset=1.25, local_offset=0.75, next_offset=1.5),
        NoteMoment(offset=2.25, local_offset=0.75, next_offset=2.5),
    ]


def test_2():
    clip = Clip(notes=[Note(0, 1)], is_looping=False)
    assert [clip.at(offset) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-0.5, next_offset=0.0),
        NoteMoment(
            offset=0, local_offset=0.0, next_offset=1.0, start_notes=[Note(0, 1)]
        ),
        NoteMoment(offset=0.125, local_offset=0.125, next_offset=1.0),
        NoteMoment(offset=0.25, local_offset=0.25, next_offset=1.0),
        NoteMoment(offset=0.5, local_offset=0.5, next_offset=1.0),
        NoteMoment(offset=0.75, local_offset=0.75, next_offset=1.0),
        NoteMoment(offset=1, local_offset=1.0, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=1.25, local_offset=1.25),
        NoteMoment(offset=2.25, local_offset=2.25),
    ]
    assert [clip.at(offset, force_stop=True) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-0.5),
        NoteMoment(offset=0, local_offset=0.0),
        NoteMoment(offset=0.125, local_offset=0.125, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=0.25, local_offset=0.25, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=0.5, local_offset=0.5, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=0.75, local_offset=0.75, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=1, local_offset=1.0, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=1.25, local_offset=1.25),
        NoteMoment(offset=2.25, local_offset=2.25),
    ]
    assert [clip.at(offset, start_delta=0.5) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-1.0, next_offset=0.5),
        NoteMoment(offset=0, local_offset=-0.5, next_offset=0.5),
        NoteMoment(offset=0.125, local_offset=-0.375, next_offset=0.5),
        NoteMoment(offset=0.25, local_offset=-0.25, next_offset=0.5),
        NoteMoment(
            offset=0.5, local_offset=0.0, next_offset=1.5, start_notes=[Note(0, 1)]
        ),
        NoteMoment(offset=0.75, local_offset=0.25, next_offset=1.5),
        NoteMoment(offset=1, local_offset=0.5, next_offset=1.5),
        NoteMoment(offset=1.25, local_offset=0.75, next_offset=1.5),
        NoteMoment(offset=2.25, local_offset=1.75),
    ]


def test_3():
    clip = Clip(notes=[Note(0, 1)])
    assert [clip.at(offset) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-0.5, next_offset=0.0),
        NoteMoment(
            offset=0, local_offset=0.0, next_offset=1.0, start_notes=[Note(0, 1)]
        ),
        NoteMoment(offset=0.125, local_offset=0.125, next_offset=1.0),
        NoteMoment(offset=0.25, local_offset=0.25, next_offset=1.0),
        NoteMoment(offset=0.5, local_offset=0.5, next_offset=1.0),
        NoteMoment(offset=0.75, local_offset=0.75, next_offset=1.0),
        NoteMoment(
            offset=1,
            local_offset=0.0,
            next_offset=2.0,
            start_notes=[Note(0, 1)],
            stop_notes=[Note(0, 1)],
        ),
        NoteMoment(offset=1.25, local_offset=0.25, next_offset=2.0),
        NoteMoment(offset=2.25, local_offset=0.25, next_offset=3.0),
    ]
    assert [clip.at(offset, force_stop=True) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-0.5),
        NoteMoment(offset=0, local_offset=0.0),
        NoteMoment(offset=0.125, local_offset=0.125, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=0.25, local_offset=0.25, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=0.5, local_offset=0.5, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=0.75, local_offset=0.75, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=1, local_offset=0.0, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=1.25, local_offset=0.25, stop_notes=[Note(0, 1)]),
        NoteMoment(offset=2.25, local_offset=0.25, stop_notes=[Note(0, 1)]),
    ]
    assert [clip.at(offset, start_delta=0.5) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-1.0, next_offset=0.5),
        NoteMoment(offset=0, local_offset=-0.5, next_offset=0.5),
        NoteMoment(offset=0.125, local_offset=-0.375, next_offset=0.5),
        NoteMoment(offset=0.25, local_offset=-0.25, next_offset=0.5),
        NoteMoment(
            offset=0.5,
            local_offset=0.0,
            next_offset=1.5,
            start_notes=[Note(0, 1, pitch=0.0)],
        ),
        NoteMoment(offset=0.75, local_offset=0.25, next_offset=1.5),
        NoteMoment(offset=1, local_offset=0.5, next_offset=1.5),
        NoteMoment(offset=1.25, local_offset=0.75, next_offset=1.5),
        NoteMoment(offset=2.25, local_offset=0.75, next_offset=2.5),
    ]


def test_4():
    clip = Clip(
        notes=[
            Note(0, 0.25, pitch=60),
            Note(0.25, 0.5, pitch=62),
            Note(0.5, 0.75, pitch=64),
            Note(0.75, 1.0, pitch=65),
        ]
    )
    assert [clip.at(offset) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-0.5, next_offset=0.0),
        NoteMoment(
            offset=0,
            local_offset=0.0,
            next_offset=0.25,
            start_notes=[Note(0, 0.25, pitch=60)],
        ),
        NoteMoment(offset=0.125, local_offset=0.125, next_offset=0.25),
        NoteMoment(
            offset=0.25,
            local_offset=0.25,
            next_offset=0.5,
            start_notes=[Note(0.25, 0.5, pitch=62)],
            stop_notes=[Note(0, 0.25, pitch=60)],
        ),
        NoteMoment(
            offset=0.5,
            local_offset=0.5,
            next_offset=0.75,
            start_notes=[Note(0.5, 0.75, pitch=64)],
            stop_notes=[Note(0.25, 0.5, pitch=62)],
        ),
        NoteMoment(
            offset=0.75,
            local_offset=0.75,
            next_offset=1.0,
            start_notes=[Note(0.75, 1.0, pitch=65)],
            stop_notes=[Note(0.5, 0.75, pitch=64)],
        ),
        NoteMoment(
            offset=1,
            local_offset=0.0,
            next_offset=1.25,
            start_notes=[Note(0, 0.25, pitch=60)],
            stop_notes=[Note(0.75, 1.0, pitch=65)],
        ),
        NoteMoment(
            offset=1.25,
            local_offset=0.25,
            next_offset=1.5,
            start_notes=[Note(0.25, 0.5, pitch=62)],
            stop_notes=[Note(0, 0.25, pitch=60)],
        ),
        NoteMoment(
            offset=2.25,
            local_offset=0.25,
            next_offset=2.5,
            start_notes=[Note(0.25, 0.5, pitch=62)],
            stop_notes=[Note(0, 0.25, pitch=60)],
        ),
    ]
    assert [clip.at(offset, force_stop=True) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-0.5),
        NoteMoment(offset=0, local_offset=0.0),
        NoteMoment(
            offset=0.125, local_offset=0.125, stop_notes=[Note(0, 0.25, pitch=60)]
        ),
        NoteMoment(
            offset=0.25, local_offset=0.25, stop_notes=[Note(0, 0.25, pitch=60)]
        ),
        NoteMoment(
            offset=0.5, local_offset=0.5, stop_notes=[Note(0.25, 0.5, pitch=62)]
        ),
        NoteMoment(
            offset=0.75, local_offset=0.75, stop_notes=[Note(0.5, 0.75, pitch=64)]
        ),
        NoteMoment(offset=1, local_offset=0.0, stop_notes=[Note(0.75, 1.0, pitch=65)]),
        NoteMoment(
            offset=1.25, local_offset=0.25, stop_notes=[Note(0, 0.25, pitch=60)]
        ),
        NoteMoment(
            offset=2.25, local_offset=0.25, stop_notes=[Note(0, 0.25, pitch=60)]
        ),
    ]
    assert [clip.at(offset, start_delta=0.5) for offset in offsets] == [
        NoteMoment(offset=-0.5, local_offset=-1.0, next_offset=0.5),
        NoteMoment(offset=0, local_offset=-0.5, next_offset=0.5),
        NoteMoment(offset=0.125, local_offset=-0.375, next_offset=0.5),
        NoteMoment(offset=0.25, local_offset=-0.25, next_offset=0.5),
        NoteMoment(
            offset=0.5,
            local_offset=0.0,
            next_offset=0.75,
            start_notes=[Note(0, 0.25, pitch=60)],
        ),
        NoteMoment(
            offset=0.75,
            local_offset=0.25,
            next_offset=1.0,
            start_notes=[Note(0.25, 0.5, pitch=62)],
            stop_notes=[Note(0, 0.25, pitch=60)],
        ),
        NoteMoment(
            offset=1,
            local_offset=0.5,
            next_offset=1.25,
            start_notes=[Note(0.5, 0.75, pitch=64)],
            stop_notes=[Note(0.25, 0.5, pitch=62)],
        ),
        NoteMoment(
            offset=1.25,
            local_offset=0.75,
            next_offset=1.5,
            start_notes=[Note(0.75, 1.0, pitch=65)],
            stop_notes=[Note(0.5, 0.75, pitch=64)],
        ),
        NoteMoment(
            offset=2.25,
            local_offset=0.75,
            next_offset=2.5,
            start_notes=[Note(0.75, 1.0, pitch=65)],
            stop_notes=[Note(0.5, 0.75, pitch=64)],
        ),
    ]
