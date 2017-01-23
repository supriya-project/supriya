# -*- encoding: utf-8 -*-
from patterntools_testbase import TestCase
from supriya.tools import patterntools


class TestCase(TestCase):

    def test___iter___01(self):
        pattern = patterntools.Pwhite(
            minimum=0.,
            maximum=1.,
            repetitions=100,
            )
        result = list(pattern)
        assert len(result) == 100
        assert all(0. <= x <= 1. for x in result)

    def test___iter___02(self):
        pattern = patterntools.Pwhite(
            minimum=-5,
            maximum=23,
            repetitions=127,
            )
        result = list(pattern)
        assert len(result) == 127
        assert all(-5 <= x <= 23 for x in result)

    def test_send_01(self):
        pattern = patterntools.Pwhite()
        iterator = iter(pattern)
        next(iterator)
        with self.assertRaises(StopIteration):
            iterator.send(True)

    def test_send_02(self):
        pattern = patterntools.Pwhite()
        iterator = iter(pattern)
        for _ in range(10):
            next(iterator)
        with self.assertRaises(StopIteration):
            iterator.send(True)
