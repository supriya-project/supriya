from patterntools_testbase import TestCase
from supriya.tools import patterntools


class TestCase(TestCase):

    pattern = patterntools.Pbindf(
        patterntools.Pbind(
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            ),
        amplitude=patterntools.Pseq([0.111, 0.333, 0.666, 1.0]),
        pan=patterntools.Pseq([0., 0.5, 1.0, 0.5]),
        )

    def test___iter__(self):
        events = [event for event in self.pattern]
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.111,
                delta=1.0,
                duration=1.0,
                is_stop=True,
                pan=0.0,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.333,
                delta=2.0,
                duration=2.0,
                is_stop=True,
                pan=0.5,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.666,
                delta=3.0,
                duration=3.0,
                is_stop=True,
                pan=1.0,
                uuid=UUID('C'),
                )
            ''',
            replace_uuids=True,
            )

    def test_send(self):
        events, iterator = [], iter(self.pattern)
        for _ in range(1):
            events.append(next(iterator))
        try:
            events.append(iterator.send(True))
            events.extend(iterator)
        except StopIteration:
            pass
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=0.111,
                delta=1.0,
                duration=1.0,
                is_stop=True,
                pan=0.0,
                uuid=UUID('A'),
                )
            ''',
            replace_uuids=True,
            )
