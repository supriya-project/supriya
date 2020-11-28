import pytest
import uqbar.strings

import supriya.patterns

pattern_01 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=supriya.patterns.Pseq([1001, 1002, 1003], 1),
        )
    ]
)


pattern_02 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=supriya.patterns.Pseq([1001, 1002], 1),
        ),
        supriya.patterns.Pmono(
            amplitude=1.0,
            duration=0.75,
            frequency=supriya.patterns.Pseq([2001, 2002, 2003], 1),
        ),
    ]
)


pattern_06 = supriya.patterns.Ppar(
    [
        supriya.patterns.Pgpar(
            [
                [
                    supriya.patterns.Pbind(
                        delta=10,
                        duration=10,
                        frequency=supriya.patterns.Pseq([1001, 1002, 1003]),
                    ),
                    supriya.patterns.Pbind(
                        delta=12,
                        duration=10,
                        frequency=supriya.patterns.Pseq([2001, 2002, 2003]),
                    ),
                ]
            ]
        ),
        supriya.patterns.Pgpar(
            [
                [
                    supriya.patterns.Pbind(
                        delta=10,
                        duration=10,
                        frequency=supriya.patterns.Pseq([3001, 3002]),
                    ),
                    supriya.patterns.Pbind(
                        delta=12,
                        duration=10,
                        frequency=supriya.patterns.Pseq([4001, 4002]),
                    ),
                ]
            ]
        ),
    ]
)


def test_send_01():
    events = pytest.helpers.setup_pattern_send(pattern_01, iterations=1)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1001,
            uuid=UUID('A'),
        )
        """
    )
    events = pytest.helpers.setup_pattern_send(pattern_01, iterations=2)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1001,
            uuid=UUID('A'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1002,
            uuid=UUID('B'),
        )
        """
    )
    events = pytest.helpers.setup_pattern_send(pattern_01, iterations=3)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1001,
            uuid=UUID('A'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1002,
            uuid=UUID('B'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=1.0,
            duration=1.0,
            frequency=1003,
            uuid=UUID('C'),
        )
        """
    )


def test_send_02():
    events = pytest.helpers.setup_pattern_send(pattern_02, iterations=1)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        NoteEvent(
            amplitude=1.0,
            delta=0.0,
            duration=1.0,
            frequency=1001,
            uuid=UUID('A'),
        )
        """
    )
    events = pytest.helpers.setup_pattern_send(pattern_02, iterations=2)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        NoteEvent(
            amplitude=1.0,
            delta=0.0,
            duration=1.0,
            frequency=1001,
            uuid=UUID('A'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=0.75,
            duration=0.75,
            frequency=2001,
            is_stop=False,
            uuid=UUID('B'),
        )
        """
    )
    events = pytest.helpers.setup_pattern_send(pattern_02, iterations=3)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        NoteEvent(
            amplitude=1.0,
            delta=0.0,
            duration=1.0,
            frequency=1001,
            uuid=UUID('A'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=0.75,
            duration=0.75,
            frequency=2001,
            is_stop=False,
            uuid=UUID('B'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=0.25,
            duration=0.75,
            frequency=2002,
            is_stop=False,
            uuid=UUID('B'),
        )
        """
)
    events = pytest.helpers.setup_pattern_send(pattern_02, iterations=4)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
) == uqbar.strings.normalize(
        """
        NoteEvent(
            amplitude=1.0,
            delta=0.0,
            duration=1.0,
            frequency=1001,
            uuid=UUID('A'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=0.75,
            duration=0.75,
            frequency=2001,
            is_stop=False,
            uuid=UUID('B'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=0.25,
            duration=0.75,
            frequency=2002,
            is_stop=False,
            uuid=UUID('B'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=0.5,
            duration=1.0,
            frequency=1002,
            uuid=UUID('C'),
        )
        """
    )
    events = pytest.helpers.setup_pattern_send(pattern_02, iterations=5)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        NoteEvent(
            amplitude=1.0,
            delta=0.0,
            duration=1.0,
            frequency=1001,
            uuid=UUID('A'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=0.75,
            duration=0.75,
            frequency=2001,
            is_stop=False,
            uuid=UUID('B'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=0.25,
            duration=0.75,
            frequency=2002,
            is_stop=False,
            uuid=UUID('B'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=0.5,
            duration=1.0,
            frequency=1002,
            uuid=UUID('C'),
        )
        NoteEvent(
            amplitude=1.0,
            delta=0.75,
            duration=0.75,
            frequency=2003,
            uuid=UUID('B'),
        )
        """
    )


def test_send_06():
    events = pytest.helpers.setup_pattern_send(pattern_06, iterations=1)
    # This is odd, but in practice you wouldn't stop on this event.
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        CompositeEvent(
            events=(
                GroupEvent(
                    add_action=AddAction.ADD_TO_TAIL,
                    uuid=UUID('A'),
                ),
            ),
        )
        """
    )
    events = pytest.helpers.setup_pattern_send(pattern_06, iterations=2)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        CompositeEvent(
            events=(
                GroupEvent(
                    add_action=AddAction.ADD_TO_TAIL,
                    uuid=UUID('A'),
                ),
            ),
        )
        NoteEvent(
            delta=0.0,
            duration=10,
            frequency=1001,
            target_node=UUID('A'),
            uuid=UUID('B'),
        )
        CompositeEvent(
            events=(
                NullEvent(
                    delta=0.25,
                ),
                GroupEvent(
                    is_stop=True,
                    uuid=UUID('A'),
                ),
            ),
            is_stop=True,
        )
        """
    )
    events = pytest.helpers.setup_pattern_send(pattern_06, iterations=3)
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        CompositeEvent(
            events=(
                GroupEvent(
                    add_action=AddAction.ADD_TO_TAIL,
                    uuid=UUID('A'),
                ),
            ),
        )
        NoteEvent(
            delta=0.0,
            duration=10,
            frequency=1001,
            target_node=UUID('A'),
            uuid=UUID('B'),
        )
        NoteEvent(
            delta=0.0,
            duration=10,
            frequency=2001,
            target_node=UUID('A'),
            uuid=UUID('C'),
        )
        CompositeEvent(
            events=(
                NullEvent(
                    delta=0.25,
                ),
                GroupEvent(
                    is_stop=True,
                    uuid=UUID('A'),
                ),
            ),
            is_stop=True,
        )
        """
    )
    events = pytest.helpers.setup_pattern_send(pattern_06, iterations=4)
    # This is odd, but in practice you wouldn't stop on this event.
    assert pytest.helpers.get_objects_as_string(
        events, replace_uuids=True
    ) == uqbar.strings.normalize(
        """
        CompositeEvent(
            events=(
                GroupEvent(
                    add_action=AddAction.ADD_TO_TAIL,
                    uuid=UUID('A'),
                ),
            ),
        )
        NoteEvent(
            delta=0.0,
            duration=10,
            frequency=1001,
            target_node=UUID('A'),
            uuid=UUID('B'),
        )
        NoteEvent(
            delta=0.0,
            duration=10,
            frequency=2001,
            target_node=UUID('A'),
            uuid=UUID('C'),
        )
        CompositeEvent(
            events=(
                GroupEvent(
                    add_action=AddAction.ADD_TO_TAIL,
                    uuid=UUID('D'),
                ),
            ),
        )
        CompositeEvent(
            events=(
                NullEvent(
                    delta=0.25,
                ),
                GroupEvent(
                    is_stop=True,
                    uuid=UUID('A'),
                ),
            ),
            is_stop=True,
        )
        """
    )
