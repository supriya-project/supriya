import pytest
import uqbar.strings

import supriya.patterns

pattern_01 = supriya.patterns.Pn(
    supriya.patterns.Pbind(foo=supriya.patterns.Pseq(["A", "B", "C"])), repetitions=2
)


pattern_02 = supriya.patterns.Pn(
    supriya.patterns.Pbind(foo=supriya.patterns.Pseq(["A", "B", "C"])),
    key="repeat",
    repetitions=3,
)


def test___iter___01():
    events = list(pattern_01)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        NoteEvent(
            foo='A',
            uuid=UUID('A'),
        )
        NoteEvent(
            foo='B',
            uuid=UUID('B'),
        )
        NoteEvent(
            foo='C',
            uuid=UUID('C'),
        )
        NoteEvent(
            foo='A',
            uuid=UUID('D'),
        )
        NoteEvent(
            foo='B',
            uuid=UUID('E'),
        )
        NoteEvent(
            foo='C',
            uuid=UUID('F'),
        )
        """
    )


def test___iter___02():
    events = list(pattern_02)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        NoteEvent(
            foo='A',
            repeat=True,
            uuid=UUID('A'),
        )
        NoteEvent(
            foo='B',
            uuid=UUID('B'),
        )
        NoteEvent(
            foo='C',
            uuid=UUID('C'),
        )
        NoteEvent(
            foo='A',
            repeat=True,
            uuid=UUID('D'),
        )
        NoteEvent(
            foo='B',
            uuid=UUID('E'),
        )
        NoteEvent(
            foo='C',
            uuid=UUID('F'),
        )
        NoteEvent(
            foo='A',
            repeat=True,
            uuid=UUID('G'),
        )
        NoteEvent(
            foo='B',
            uuid=UUID('H'),
        )
        NoteEvent(
            foo='C',
            uuid=UUID('I'),
        )
        """
    )
