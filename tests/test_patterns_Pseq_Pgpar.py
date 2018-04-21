import pytest
import supriya.patterns
import uqbar.strings
from patterns_testbase import TestCase


class TestCase(TestCase):

    pattern = supriya.patterns.Pseq([
        supriya.patterns.Pgpar([
            supriya.patterns.Pbind(
                amplitude=1.0,
                duration=supriya.patterns.Pseq([1.0], 1),
                frequency=supriya.patterns.Pseq([440], 1),
                ),
            supriya.patterns.Pbind(
                amplitude=0.75,
                duration=supriya.patterns.Pseq([1.0], 1),
                frequency=supriya.patterns.Pseq([880], 1),
                ),
            ]),
        supriya.patterns.Pgpar([
            supriya.patterns.Pbind(
                amplitude=0.5,
                duration=supriya.patterns.Pseq([2.0], 1),
                frequency=supriya.patterns.Pseq([330], 1),
                ),
            supriya.patterns.Pbind(
                amplitude=0.25,
                duration=supriya.patterns.Pseq([2.0], 1),
                frequency=supriya.patterns.Pseq([660], 1),
                ),
            ]),
        ])

    def test___iter__(self):
        events = list(self.pattern)
        assert pytest.helpers.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            CompositeEvent(
                events=(
                    GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        uuid=UUID('A'),
                        ),
                    GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        uuid=UUID('B'),
                        ),
                    ),
                )
            NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                target_node=UUID('A'),
                uuid=UUID('C'),
                )
            NoteEvent(
                amplitude=0.75,
                delta=1.0,
                duration=1.0,
                frequency=880,
                target_node=UUID('B'),
                uuid=UUID('D'),
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
                    GroupEvent(
                        is_stop=True,
                        uuid=UUID('B'),
                        ),
                    ),
                is_stop=True,
                )
            CompositeEvent(
                events=(
                    GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        uuid=UUID('E'),
                        ),
                    GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        uuid=UUID('F'),
                        ),
                    ),
                )
            NoteEvent(
                amplitude=0.5,
                delta=0.0,
                duration=2.0,
                frequency=330,
                target_node=UUID('E'),
                uuid=UUID('G'),
                )
            NoteEvent(
                amplitude=0.25,
                delta=2.0,
                duration=2.0,
                frequency=660,
                target_node=UUID('F'),
                uuid=UUID('H'),
                )
            CompositeEvent(
                events=(
                    NullEvent(
                        delta=0.25,
                        ),
                    GroupEvent(
                        is_stop=True,
                        uuid=UUID('E'),
                        ),
                    GroupEvent(
                        is_stop=True,
                        uuid=UUID('F'),
                        ),
                    ),
                is_stop=True,
                )
            ''')
