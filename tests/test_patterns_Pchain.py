import uqbar.strings
from patterntools_testbase import TestCase
import supriya.patterns


class TestCase(TestCase):

    pattern = supriya.patterns.Pchain([
        supriya.patterns.Pbind(
            amplitude=1.0,
            duration=supriya.patterns.Pseq([1.0, 2.0, 3.0], 1),
            frequency=supriya.patterns.Pseq([440, 660, 880], 1),
            ),
        supriya.patterns.Pbind(
            amplitude=supriya.patterns.Pseq([0.111, 0.333, 0.666, 1.0]),
            ),
        supriya.patterns.Pbind(
            pan=supriya.patterns.Pseq([0., 0.5, 1.0, 0.5]),
            ),
        ])

    def test___iter__(self):
        events = list(self.pattern)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=0.111,
                delta=1.0,
                duration=1.0,
                frequency=440,
                pan=0.0,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=0.333,
                delta=2.0,
                duration=2.0,
                frequency=660,
                pan=0.5,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=0.666,
                delta=3.0,
                duration=3.0,
                frequency=880,
                pan=1.0,
                uuid=UUID('C'),
                )
            ''')
