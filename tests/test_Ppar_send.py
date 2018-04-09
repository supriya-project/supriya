import uqbar.strings
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
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1001,
                uuid=UUID('A'),
                )
            ''')
        events = self.setup_send(self.pattern_01, iterations=2)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1001,
                uuid=UUID('A'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1002,
                uuid=UUID('B'),
                )
            ''')
        events = self.setup_send(self.pattern_01, iterations=3)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1001,
                uuid=UUID('A'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1002,
                uuid=UUID('B'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1003,
                uuid=UUID('C'),
                )
            ''')

    def test_send_02(self):
        events = self.setup_send(self.pattern_02, iterations=1)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                uuid=UUID('A'),
                )
            ''')
        events = self.setup_send(self.pattern_02, iterations=2)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                uuid=UUID('A'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2001,
                is_stop=False,
                uuid=UUID('B'),
                )
            ''')
        events = self.setup_send(self.pattern_02, iterations=3)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                uuid=UUID('A'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2001,
                is_stop=False,
                uuid=UUID('B'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=2002,
                is_stop=False,
                uuid=UUID('B'),
                )
            ''')
        events = self.setup_send(self.pattern_02, iterations=4)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                uuid=UUID('A'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2001,
                is_stop=False,
                uuid=UUID('B'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=2002,
                is_stop=False,
                uuid=UUID('B'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.5,
                duration=1.0,
                frequency=1002,
                uuid=UUID('C'),
                )
            ''')
        events = self.setup_send(self.pattern_02, iterations=5)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                uuid=UUID('A'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2001,
                is_stop=False,
                uuid=UUID('B'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=2002,
                is_stop=False,
                uuid=UUID('B'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.5,
                duration=1.0,
                frequency=1002,
                uuid=UUID('C'),
                )
            NoteEvent(
                _iterator=None,
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2003,
                uuid=UUID('B'),
                )
            ''')

    def test_send_06(self):
        events = self.setup_send(self.pattern_06, iterations=1)
        # This is odd, but in practice you wouldn't stop on this event.
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            CompositeEvent(
                events=(
                    GroupEvent(
                        _iterator=None,
                        add_action=AddAction.ADD_TO_TAIL,
                        uuid=UUID('A'),
                        ),
                    ),
                )
            ''')
        events = self.setup_send(self.pattern_06, iterations=2)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            CompositeEvent(
                events=(
                    GroupEvent(
                        _iterator=None,
                        add_action=AddAction.ADD_TO_TAIL,
                        uuid=UUID('A'),
                        ),
                    ),
                )
            NoteEvent(
                _iterator=None,
                delta=0.0,
                duration=10,
                frequency=1001,
                target_node=UUID('A'),
                uuid=UUID('B'),
                )
            CompositeEvent(
                events=(
                    NullEvent(
                        _iterator=None,
                        delta=0.25,
                        ),
                    GroupEvent(
                        _iterator=None,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            ''')
        events = self.setup_send(self.pattern_06, iterations=3)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            CompositeEvent(
                events=(
                    GroupEvent(
                        _iterator=None,
                        add_action=AddAction.ADD_TO_TAIL,
                        uuid=UUID('A'),
                        ),
                    ),
                )
            NoteEvent(
                _iterator=None,
                delta=0.0,
                duration=10,
                frequency=1001,
                target_node=UUID('A'),
                uuid=UUID('B'),
                )
            NoteEvent(
                _iterator=None,
                delta=0.0,
                duration=10,
                frequency=2001,
                target_node=UUID('A'),
                uuid=UUID('C'),
                )
            CompositeEvent(
                events=(
                    NullEvent(
                        _iterator=None,
                        delta=0.25,
                        ),
                    GroupEvent(
                        _iterator=None,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            ''')
        events = self.setup_send(self.pattern_06, iterations=4)
        # This is odd, but in practice you wouldn't stop on this event.
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            CompositeEvent(
                events=(
                    GroupEvent(
                        _iterator=None,
                        add_action=AddAction.ADD_TO_TAIL,
                        uuid=UUID('A'),
                        ),
                    ),
                )
            NoteEvent(
                _iterator=None,
                delta=0.0,
                duration=10,
                frequency=1001,
                target_node=UUID('A'),
                uuid=UUID('B'),
                )
            NoteEvent(
                _iterator=None,
                delta=0.0,
                duration=10,
                frequency=2001,
                target_node=UUID('A'),
                uuid=UUID('C'),
                )
            CompositeEvent(
                events=(
                    GroupEvent(
                        _iterator=None,
                        add_action=AddAction.ADD_TO_TAIL,
                        uuid=UUID('D'),
                        ),
                    ),
                )
            CompositeEvent(
                events=(
                    NullEvent(
                        _iterator=None,
                        delta=0.25,
                        ),
                    GroupEvent(
                        _iterator=None,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            ''')
