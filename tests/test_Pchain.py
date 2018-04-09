import uqbar.strings
from patterntools_testbase import TestCase
from supriya.tools import patterntools


class TestCase(TestCase):

    pattern = patterntools.Pchain([
        patterntools.Pbind(
            amplitude=1.0,
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            frequency=patterntools.Pseq([440, 660, 880], 1),
            ),
        patterntools.Pbind(
            amplitude=patterntools.Pseq([0.111, 0.333, 0.666, 1.0]),
            ),
        patterntools.Pbind(
            pan=patterntools.Pseq([0., 0.5, 1.0, 0.5]),
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
