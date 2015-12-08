# -*- encoding: utf-8 -*-
import unittest
from supriya.tools import nrttools


class TestCase(unittest.TestCase):

    def test_at(self):
        session = nrttools.NRTSession()
        timeslice = session.at(10) 
        timeslice = session.at(20)
        timeslice = session.at(60)

    def test_get_bus(self):
        session = nrttools.NRTSession()
        control_bus_1 = session.get_bus()
        audio_bus_1 = session.get_bus(kind='audio')
        control_bus_2 = session.get_bus()
        audio_bus_2 = session.get_bus(kind='audio')
        assert audio_bus_1 in session
        assert audio_bus_2 in session
        assert control_bus_1 in session
        assert control_bus_2 in session
        assert audio_bus_1.nrt_id == 1
        assert audio_bus_2.nrt_id == 2
        assert control_bus_1.nrt_id == 1
        assert control_bus_2.nrt_id == 2
