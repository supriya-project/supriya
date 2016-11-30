# -*- encoding: utf-8 -*-
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

    def test_iter(self):
        events = [event for event in self.pattern]
        assert len(events) == 3
        self.compare_strings(
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.111,
                duration=1.0,
                frequency=440,
                is_stop=True,
                pan=0.0,
                uuid=UUID('...'),
                )
            ''',
            format(events[0]),
            )
        self.compare_strings(
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.333,
                duration=2.0,
                frequency=660,
                is_stop=True,
                pan=0.5,
                uuid=UUID('...'),
                )
            ''',
            format(events[1]),
            )
        self.compare_strings(
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.666,
                duration=3.0,
                frequency=880,
                is_stop=True,
                pan=1.0,
                uuid=UUID('...'),
                )
            ''',
            format(events[2]),
            )
