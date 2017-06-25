from supriya.tools import patterntools
from patterntools_testbase import TestCase


class TestCase(TestCase):

    pattern_01 = patterntools.Ppar([
        patterntools.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=patterntools.Pseq([1001, 1002, 1003], 1),
            ),
        ])

    pattern_02 = patterntools.Ppar([
        patterntools.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=patterntools.Pseq([1001, 1002], 1),
            ),
        patterntools.Pmono(
            amplitude=1.0,
            duration=0.75,
            frequency=patterntools.Pseq([2001, 2002, 2003], 1),
            ),
        ])

    pattern_06 = patterntools.Ppar([
        patterntools.Pgpar([
            [
                patterntools.Pbind(
                    delta=10,
                    duration=10,
                    frequency=patterntools.Pseq([1001, 1002, 1003]),
                    ),
                patterntools.Pbind(
                    delta=12,
                    duration=10,
                    frequency=patterntools.Pseq([2001, 2002, 2003]),
                    ),
                ],
            ]),
        patterntools.Pgpar([
            [
                patterntools.Pbind(
                    delta=10,
                    duration=10,
                    frequency=patterntools.Pseq([3001, 3002]),
                    ),
                patterntools.Pbind(
                    delta=12,
                    duration=10,
                    frequency=patterntools.Pseq([4001, 4002]),
                    ),
                ],
            ]),
        ])

    def test_send_01(self):
        events = self.setup_send(self.pattern_01, iterations=1)
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1001,
                is_stop=True,
                uuid=UUID('A'),
                )
            ''', replace_uuids=True,
            )
        events = self.setup_send(self.pattern_01, iterations=2)
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1001,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1002,
                is_stop=True,
                uuid=UUID('B'),
                )
            ''', replace_uuids=True,
            )
        events = self.setup_send(self.pattern_01, iterations=3)
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1001,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1002,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=1003,
                is_stop=True,
                uuid=UUID('C'),
                )
            ''', replace_uuids=True,
            )

    def test_send_02(self):
        events = self.setup_send(self.pattern_02, iterations=1)
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                is_stop=True,
                uuid=UUID('A'),
                )
            ''', replace_uuids=True,
            )
        events = self.setup_send(self.pattern_02, iterations=2)
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2001,
                uuid=UUID('B'),
                )
            ''', replace_uuids=True,
            )
        events = self.setup_send(self.pattern_02, iterations=3)
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2001,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=2002,
                uuid=UUID('B'),
                )
            ''', replace_uuids=True,
            )
        events = self.setup_send(self.pattern_02, iterations=4)
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2001,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=2002,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=1.0,
                frequency=1002,
                is_stop=True,
                uuid=UUID('C'),
                )
            ''', replace_uuids=True,
            )
        events = self.setup_send(self.pattern_02, iterations=5)
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2001,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=2002,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=1.0,
                frequency=1002,
                is_stop=True,
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=0.75,
                frequency=2003,
                is_stop=True,
                uuid=UUID('B'),
                )
            ''', replace_uuids=True,
            )

    def test_send_06(self):
        events = self.setup_send(self.pattern_06, iterations=1)
        # This is odd, but in practice you wouldn't stop on this event.
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.GroupEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    ),
                )
            ''', replace_uuids=True,
            )
        events = self.setup_send(self.pattern_06, iterations=2)
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.GroupEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                delta=0.0,
                duration=10,
                frequency=1001,
                is_stop=True,
                target_node=UUID('A'),
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            ''', replace_uuids=True,
            )
        events = self.setup_send(self.pattern_06, iterations=3)
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.GroupEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                delta=0.0,
                duration=10,
                frequency=1001,
                is_stop=True,
                target_node=UUID('A'),
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                delta=0.0,
                duration=10,
                frequency=2001,
                is_stop=True,
                target_node=UUID('A'),
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            ''', replace_uuids=True,
            )
        events = self.setup_send(self.pattern_06, iterations=4)
        # This is odd, but in practice you wouldn't stop on this event.
        self.compare_objects_as_strings(
            events, '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.GroupEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                delta=0.0,
                duration=10,
                frequency=1001,
                is_stop=True,
                target_node=UUID('A'),
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                delta=0.0,
                duration=10,
                frequency=2001,
                is_stop=True,
                target_node=UUID('A'),
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.GroupEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('D'),
                        ),
                    ),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            ''', replace_uuids=True,
            )
