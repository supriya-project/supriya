import uqbar.strings
from patterntools_testbase import TestCase
from supriya.tools import patterntools


class TestCase(TestCase):

    pattern = patterntools.Pseq([
        patterntools.Pgpar([
            patterntools.Pbind(
                amplitude=1.0,
                duration=patterntools.Pseq([1.0], 1),
                frequency=patterntools.Pseq([440], 1),
                ),
            patterntools.Pbind(
                amplitude=0.75,
                duration=patterntools.Pseq([1.0], 1),
                frequency=patterntools.Pseq([880], 1),
                ),
            ]),
        patterntools.Pgpar([
            patterntools.Pbind(
                amplitude=0.5,
                duration=patterntools.Pseq([2.0], 1),
                frequency=patterntools.Pseq([330], 1),
                ),
            patterntools.Pbind(
                amplitude=0.25,
                duration=patterntools.Pseq([2.0], 1),
                frequency=patterntools.Pseq([660], 1),
                ),
            ]),
        ])

    def test___iter__(self):
        events = list(self.pattern)
        assert self.get_objects_as_string(
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
