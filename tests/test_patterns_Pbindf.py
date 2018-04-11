import uqbar.strings
from patterns_testbase import TestCase
import supriya.patterns


class TestCase(TestCase):

    pattern = supriya.patterns.Pbindf(
        supriya.patterns.Pbind(
            duration=supriya.patterns.Pseq([1.0, 2.0, 3.0], 1),
            ),
        amplitude=supriya.patterns.Pseq([0.111, 0.333, 0.666, 1.0]),
        pan=supriya.patterns.Pseq([0., 0.5, 1.0, 0.5]),
        )

    def test___iter__(self):
        events = [event for event in self.pattern]
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=0.111,
                delta=1.0,
                duration=1.0,
                pan=0.0,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=0.333,
                delta=2.0,
                duration=2.0,
                pan=0.5,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=0.666,
                delta=3.0,
                duration=3.0,
                pan=1.0,
                uuid=UUID('C'),
                )
            ''')

    def test_send(self):
        events, iterator = [], iter(self.pattern)
        for _ in range(1):
            events.append(next(iterator))
        try:
            events.append(iterator.send(True))
            events.extend(iterator)
        except StopIteration:
            pass
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=0.111,
                delta=1.0,
                duration=1.0,
                pan=0.0,
                uuid=UUID('A'),
                )
            ''')
