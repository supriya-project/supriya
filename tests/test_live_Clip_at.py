from supriya.live import Clip, Note

notes = (
    Note(-1, 3, pitch=-2),
    Note(0, 1, pitch=0),
    Note(0, 1, pitch=2),
    Note(2, 6, pitch=7),
    Note(3, 4, pitch=0),
    Note(3, 4, pitch=2),
    Note(4, 10, pitch=9),
    Note(6, 7, pitch=0),
    Note(6, 7, pitch=2),
)


def test_01():
    clip = Clip(notes=notes, duration=8, is_looping=True)
    assert [clip.at(i) for i in range(-2, 18)] == [
        Clip.Moment(
            offset=-2,
            local_offset=-2.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=-1,
            local_offset=-1.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=0,
            local_offset=0.0,
            next_offset=1.0,
            start_notes=(
                Note(start_offset=0, stop_offset=1, pitch=0, velocity=1.0),
                Note(start_offset=0, stop_offset=1, pitch=2, velocity=1.0),
            ),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=1,
            local_offset=1.0,
            next_offset=2.0,
            start_notes=(),
            stop_notes=(
                Note(start_offset=0, stop_offset=1, pitch=0, velocity=1.0),
                Note(start_offset=0, stop_offset=1, pitch=2, velocity=1.0),
            ),
        ),
        Clip.Moment(
            offset=2,
            local_offset=2.0,
            next_offset=3.0,
            start_notes=(Note(start_offset=2, stop_offset=6, pitch=7, velocity=1.0),),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=3,
            local_offset=3.0,
            next_offset=4.0,
            start_notes=(
                Note(start_offset=3, stop_offset=4, pitch=0, velocity=1.0),
                Note(start_offset=3, stop_offset=4, pitch=2, velocity=1.0),
            ),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=4,
            local_offset=4.0,
            next_offset=6.0,
            start_notes=(Note(start_offset=4, stop_offset=10, pitch=9, velocity=1.0),),
            stop_notes=(
                Note(start_offset=3, stop_offset=4, pitch=0, velocity=1.0),
                Note(start_offset=3, stop_offset=4, pitch=2, velocity=1.0),
            ),
        ),
        Clip.Moment(
            offset=5, local_offset=5.0, next_offset=6.0, start_notes=(), stop_notes=()
        ),
        Clip.Moment(
            offset=6,
            local_offset=6.0,
            next_offset=7.0,
            start_notes=(
                Note(start_offset=6, stop_offset=7, pitch=0, velocity=1.0),
                Note(start_offset=6, stop_offset=7, pitch=2, velocity=1.0),
            ),
            stop_notes=(Note(start_offset=2, stop_offset=6, pitch=7, velocity=1.0),),
        ),
        Clip.Moment(
            offset=7,
            local_offset=7.0,
            next_offset=8.0,
            start_notes=(),
            stop_notes=(
                Note(start_offset=6, stop_offset=7, pitch=0, velocity=1.0),
                Note(start_offset=6, stop_offset=7, pitch=2, velocity=1.0),
            ),
        ),
        Clip.Moment(
            offset=8,
            local_offset=0.0,
            next_offset=9.0,
            start_notes=(
                Note(start_offset=0, stop_offset=1, pitch=0, velocity=1.0),
                Note(start_offset=0, stop_offset=1, pitch=2, velocity=1.0),
            ),
            stop_notes=(Note(start_offset=4, stop_offset=10, pitch=9, velocity=1.0),),
        ),
        Clip.Moment(
            offset=9,
            local_offset=1.0,
            next_offset=10.0,
            start_notes=(),
            stop_notes=(
                Note(start_offset=0, stop_offset=1, pitch=0, velocity=1.0),
                Note(start_offset=0, stop_offset=1, pitch=2, velocity=1.0),
            ),
        ),
        Clip.Moment(
            offset=10,
            local_offset=2.0,
            next_offset=11.0,
            start_notes=(Note(start_offset=2, stop_offset=6, pitch=7, velocity=1.0),),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=11,
            local_offset=3.0,
            next_offset=12.0,
            start_notes=(
                Note(start_offset=3, stop_offset=4, pitch=0, velocity=1.0),
                Note(start_offset=3, stop_offset=4, pitch=2, velocity=1.0),
            ),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=12,
            local_offset=4.0,
            next_offset=14.0,
            start_notes=(Note(start_offset=4, stop_offset=10, pitch=9, velocity=1.0),),
            stop_notes=(
                Note(start_offset=3, stop_offset=4, pitch=0, velocity=1.0),
                Note(start_offset=3, stop_offset=4, pitch=2, velocity=1.0),
            ),
        ),
        Clip.Moment(
            offset=13, local_offset=5.0, next_offset=14.0, start_notes=(), stop_notes=()
        ),
        Clip.Moment(
            offset=14,
            local_offset=6.0,
            next_offset=15.0,
            start_notes=(
                Note(start_offset=6, stop_offset=7, pitch=0, velocity=1.0),
                Note(start_offset=6, stop_offset=7, pitch=2, velocity=1.0),
            ),
            stop_notes=(Note(start_offset=2, stop_offset=6, pitch=7, velocity=1.0),),
        ),
        Clip.Moment(
            offset=15,
            local_offset=7.0,
            next_offset=16.0,
            start_notes=(),
            stop_notes=(
                Note(start_offset=6, stop_offset=7, pitch=0, velocity=1.0),
                Note(start_offset=6, stop_offset=7, pitch=2, velocity=1.0),
            ),
        ),
        Clip.Moment(
            offset=16,
            local_offset=0.0,
            next_offset=17.0,
            start_notes=(
                Note(start_offset=0, stop_offset=1, pitch=0, velocity=1.0),
                Note(start_offset=0, stop_offset=1, pitch=2, velocity=1.0),
            ),
            stop_notes=(Note(start_offset=4, stop_offset=10, pitch=9, velocity=1.0),),
        ),
        Clip.Moment(
            offset=17,
            local_offset=1.0,
            next_offset=18.0,
            start_notes=(),
            stop_notes=(
                Note(start_offset=0, stop_offset=1, pitch=0, velocity=1.0),
                Note(start_offset=0, stop_offset=1, pitch=2, velocity=1.0),
            ),
        ),
    ]


def test_02():
    clip = Clip(notes=notes, duration=8, is_looping=False)
    assert [clip.at(i) for i in range(-2, 18)] == [
        Clip.Moment(
            offset=-2,
            local_offset=-2.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=-1,
            local_offset=-1.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=0,
            local_offset=0.0,
            next_offset=1.0,
            start_notes=(
                Note(start_offset=0, stop_offset=1, pitch=0, velocity=1.0),
                Note(start_offset=0, stop_offset=1, pitch=2, velocity=1.0),
            ),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=1,
            local_offset=1.0,
            next_offset=2.0,
            start_notes=(),
            stop_notes=(
                Note(start_offset=0, stop_offset=1, pitch=0, velocity=1.0),
                Note(start_offset=0, stop_offset=1, pitch=2, velocity=1.0),
            ),
        ),
        Clip.Moment(
            offset=2,
            local_offset=2.0,
            next_offset=3.0,
            start_notes=(Note(start_offset=2, stop_offset=6, pitch=7, velocity=1.0),),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=3,
            local_offset=3.0,
            next_offset=4.0,
            start_notes=(
                Note(start_offset=3, stop_offset=4, pitch=0, velocity=1.0),
                Note(start_offset=3, stop_offset=4, pitch=2, velocity=1.0),
            ),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=4,
            local_offset=4.0,
            next_offset=6.0,
            start_notes=(Note(start_offset=4, stop_offset=10, pitch=9, velocity=1.0),),
            stop_notes=(
                Note(start_offset=3, stop_offset=4, pitch=0, velocity=1.0),
                Note(start_offset=3, stop_offset=4, pitch=2, velocity=1.0),
            ),
        ),
        Clip.Moment(
            offset=5, local_offset=5.0, next_offset=6.0, start_notes=(), stop_notes=()
        ),
        Clip.Moment(
            offset=6,
            local_offset=6.0,
            next_offset=7.0,
            start_notes=(
                Note(start_offset=6, stop_offset=7, pitch=0, velocity=1.0),
                Note(start_offset=6, stop_offset=7, pitch=2, velocity=1.0),
            ),
            stop_notes=(Note(start_offset=2, stop_offset=6, pitch=7, velocity=1.0),),
        ),
        Clip.Moment(
            offset=7,
            local_offset=7.0,
            next_offset=10.0,
            start_notes=(),
            stop_notes=(
                Note(start_offset=6, stop_offset=7, pitch=0, velocity=1.0),
                Note(start_offset=6, stop_offset=7, pitch=2, velocity=1.0),
            ),
        ),
        Clip.Moment(
            offset=8, local_offset=8.0, next_offset=10.0, start_notes=(), stop_notes=()
        ),
        Clip.Moment(
            offset=9, local_offset=9.0, next_offset=10.0, start_notes=(), stop_notes=()
        ),
        Clip.Moment(
            offset=10,
            local_offset=10.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(Note(start_offset=4, stop_offset=10, pitch=9, velocity=1.0),),
        ),
        Clip.Moment(
            offset=11,
            local_offset=11.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=12,
            local_offset=12.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=13,
            local_offset=13.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=14,
            local_offset=14.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=15,
            local_offset=15.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=16,
            local_offset=16.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(),
        ),
        Clip.Moment(
            offset=17,
            local_offset=17.0,
            next_offset=None,
            start_notes=(),
            stop_notes=(),
        ),
    ]
