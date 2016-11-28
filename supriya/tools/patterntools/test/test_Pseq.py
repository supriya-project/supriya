# -*- encoding: utf-8 -*-
from patterntools_testbase import TestCase
from supriya.tools import patterntools


class TestCase(TestCase):

    pattern = patterntools.Pseq([
        patterntools.Pbind(
            amplitude=1.0,
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            frequency=patterntools.Pseq([440, 660, 880], 1),
            ),
        patterntools.Pbind(
            amplitude=1.0,
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            frequency=patterntools.Pseq([440, 660, 880], 1),
            ),
        ])

    def test_send_01(self):
        events, iterator = [], iter(self.pattern)
        for _ in range(2):
            events.append(next(iterator))
        iterator.send(True)
        events.extend(iterator)
        assert [
            (type(x).__name__, x.get('is_stop') or False)
            for x in events] == [
            ('NoteEvent', False),
            ('NoteEvent', False),
            ]
