from supriya.xdaw import Clip, Note


def test_1():
    print("A")
    clip = Clip()
    assert clip.notes == []
    print("B")
    clip.add_notes([Note(0, 2), Note(0, 5), Note(5, 10), Note(20, 35)])
    assert clip.notes == [Note(0, 5), Note(5, 10), Note(20, 35)]
    print("C")
    clip.add_notes([Note(25, 35)])
    assert clip.notes == [Note(0, 5), Note(5, 10), Note(20, 25), Note(25, 35)]
    print("D")
    clip.add_notes([Note(0, 1, velocity=127)])
    assert clip.notes == [
        Note(0, 1, velocity=127),
        Note(5, 10),
        Note(20, 25),
        Note(25, 35),
    ]
