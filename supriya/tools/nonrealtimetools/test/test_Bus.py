# -*- encoding: utf-8 -*-
import os
from supriya.tools import nonrealtimetools
from supriya.tools import osctools
from base import TestCase


class TestCase(TestCase):

    def setUp(self):
        self.output_filepath = os.path.abspath(os.path.join(
            os.path.dirname(__file__),
            'output.aiff',
            ))
        if os.path.exists(self.output_filepath):
            os.remove(self.output_filepath)

    def tearDown(self):
        if os.path.exists(self.output_filepath):
            os.remove(self.output_filepath)

    def test_01(self):
        session = nonrealtimetools.Session()
        bus_one = session.add_bus()
        bus_two = session.add_bus()
        with session.at(0):
            bus_one.set_(10)
        with session.at(2):
            bus_one.set_(20)
            bus_two.set_(30)
        with session.at(3):
            bus_two.set_(40)
        assert session.to_osc_bundles() == [
            osctools.OscBundle(
                timestamp=0.0,
                contents=(
                    osctools.OscMessage('/c_set', 0, 10.0),
                    )
                ),
            osctools.OscBundle(
                timestamp=2.0,
                contents=(
                    osctools.OscMessage('/c_set', 0, 20.0, 1, 30.0),
                    )
                ),
            osctools.OscBundle(
                timestamp=3.0,
                contents=(
                    osctools.OscMessage('/c_set', 1, 40.0),
                    osctools.OscMessage(0),
                    )
                )
            ]
