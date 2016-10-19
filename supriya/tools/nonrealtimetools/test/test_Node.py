# -*- encoding: utf-8 -*-
from supriya.tools import nonrealtimetools
from supriya.tools import osctools
from base import TestCase


class TestCase(TestCase):

    def test_01(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            synth = session.add_synth(synthdef=self.build_basic_synthdef())
            group_one = session.add_group()
            group_two = session.add_group()
        with session.at(1):
            group_one.move_node(synth)
            group_two.move_node(group_one)
        assert session.to_osc_bundles(duration=2) == [
            osctools.OscBundle(
                timestamp=0.0,
                contents=(
                    osctools.OscMessage('/d_recv', bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 d719856d7deff2696a3f807f5dc79809\x00\x00\x00\x02C\xdc\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02\x06SinOsc\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')),
                    osctools.OscMessage('/s_new', 'd719856d7deff2696a3f807f5dc79809', 1000, 0, 0),
                    osctools.OscMessage('/g_new', 1001, 0, 0),
                    osctools.OscMessage('/g_new', 1002, 0, 0),
                    )
                ),
            osctools.OscBundle(
                timestamp=1.0,
                contents=(
                    osctools.OscMessage('/g_head', 1001, 1000),
                    osctools.OscMessage('/g_head', 1002, 1001),
                    )
                ),
            osctools.OscBundle(
                timestamp=2.0,
                contents=(
                    osctools.OscMessage('/n_free', 1000, 1001, 1002),
                    osctools.OscMessage(0),
                    )
                ),
            ]

    def test_02(self):
        r'''This should fail.'''
        session = nonrealtimetools.Session()
        with session.at(0):
            group_one = session.add_group()
            group_two = session.add_group()
        with session.at(1):
            group_one.move_node(group_two)
        with session.at(2):
            with self.assertRaises(ValueError):
                group_two.move_node(group_one)
