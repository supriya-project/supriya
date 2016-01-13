# -*- encoding: utf-8 -*-
import unittest
from supriya.tools import nonrealtimetools


class TestCase(unittest.TestCase):

    def test_01(self):
        session = nonrealtimetools.NRTSession()
        with session.at(5):
            session.add_synth(duration=10)
        assert session.timesteps == [float('-inf'), 5, 15]
