# -*- encoding: utf-8 -*-
import unittest
from supriya.tools import nonrealtimetools


class TestCase(unittest.TestCase):

    def test_01(self):
        session = nonrealtimetools.NRTSession()
        with session.at(1):
            session.add_synth(duration=2)
