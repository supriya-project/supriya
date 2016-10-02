# -*- encoding: utf-8 -*-
from abjad.tools import systemtools
from supriya.tools import patterntools


class TestCase(systemtools.TestCase):

    pattern = patterntools.Pbindf(
        patterntools.Pbind(
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            ),
        amplitude=patterntools.Pseq([0.111, 0.333, 0.666, 1.0]),
        pan=patterntools.Pseq([0., 0.5, 1.0, 0.5]),
        )

    def test_iter(self):
        events = [event for event in self.pattern]
        assert len(events) == 3
        self.compare_strings(
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.111,
                duration=1.0,
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
                pan=1.0,
                uuid=UUID('...'),
                )
            ''',
            format(events[2]),
            )
