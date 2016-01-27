# -*- encoding: utf-8 -*-
from supriya import synthdefs
from supriya.tools import nonrealtimetools
from supriya.tools import osctools
from supriya.tools.nonrealtimetools.TestCase import TestCase


class TestCase(TestCase):

    def test_01(self):
        r'''Setting synth properties.'''
        session = nonrealtimetools.Session()
        with session.at(0):
            synth_one = session.add_synth(
                duration=4,
                synthdef=synthdefs.default,
                )
        with session.at(2):
            synth_two = session.add_synth(
                duration=6,
                synthdef=synthdefs.default,
                frequency=330,
                )

        with session.at(2):
            synth_one['frequency'] = 550
            synth_two['frequency'] = 333
        with session.at(3):
            synth_one['frequency'] = 660
            synth_two['frequency'] = 770
        with session.at(4):
            synth_two['frequency'] = 880

        with session.at(0):
            assert synth_one['frequency'] == 440
        with session.at(1):
            assert synth_one['frequency'] == 440
        with session.at(2):
            assert synth_one['frequency'] == 550
            assert synth_two['frequency'] == 333
        with session.at(3):
            assert synth_one['frequency'] == 660
            assert synth_two['frequency'] == 770
        with session.at(4):
            assert synth_two['frequency'] == 880
        with session.at(5):
            assert synth_two['frequency'] == 880

    def test_02(self):
        r'''Durated synths.'''
        synthdef = self.build_duration_synthdef()
        session = nonrealtimetools.Session()
        with session.at(0):
            session.add_synth(duration=2, synthdef=synthdef)
            session.add_synth(duration=4, synthdef=synthdef)
            session.add_synth(duration=6, synthdef=synthdef)
            session.add_synth(synthdef=synthdef)
        with session.at(1):
            session.add_synth(duration=4, synthdef=synthdef)
        assert session.to_osc_bundles(duration=3) == [
            osctools.OscBundle(
                timestamp=0.0,
                contents=(
                    osctools.OscMessage('/d_recv', bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 448a8d487adfc99ec697033edc2a1227\x00\x00\x00\x02\x00\x00\x00\x00?\x80\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x08duration\x00\x00\x00\x00\x00\x00\x00\x03\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x04Line\x02\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00')),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1000, 0, 0, 'duration', 2.0),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1001, 0, 0, 'duration', 3.0),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1002, 0, 0, 'duration', 3.0),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1003, 0, 0, 'duration', 3.0),
                    )
                ),
            osctools.OscBundle(
                timestamp=1.0,
                contents=(
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1004, 0, 0, 'duration', 2.0),
                    )
                ),
            osctools.OscBundle(
                timestamp=2.0,
                contents=(
                    osctools.OscMessage('/n_free', 1000),
                    )
                ),
            osctools.OscBundle(
                timestamp=3.0,
                contents=(
                    osctools.OscMessage('/n_free', 1001, 1002, 1003, 1004),
                    osctools.OscMessage(0),
                    )
                )
            ]
        assert session.to_osc_bundles(duration=4) == [
            osctools.OscBundle(
                timestamp=0.0,
                contents=(
                    osctools.OscMessage('/d_recv', bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 448a8d487adfc99ec697033edc2a1227\x00\x00\x00\x02\x00\x00\x00\x00?\x80\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x08duration\x00\x00\x00\x00\x00\x00\x00\x03\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x04Line\x02\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00')),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1000, 0, 0, 'duration', 2.0),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1001, 0, 0, 'duration', 4.0),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1002, 0, 0, 'duration', 4.0),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1003, 0, 0, 'duration', 4.0),
                    )
                ),
            osctools.OscBundle(
                timestamp=1.0,
                contents=(
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1004, 0, 0, 'duration', 3.0),
                    )
                ),
            osctools.OscBundle(
                timestamp=2.0,
                contents=(
                    osctools.OscMessage('/n_free', 1000),
                    )
                ),
            osctools.OscBundle(
                timestamp=4.0,
                contents=(
                    osctools.OscMessage('/n_free', 1001, 1002, 1003, 1004),
                    osctools.OscMessage(0),
                    )
                )
            ]
        assert session.to_osc_bundles(duration=5) == [
            osctools.OscBundle(
                timestamp=0.0,
                contents=(
                    osctools.OscMessage('/d_recv', bytearray(b'SCgf\x00\x00\x00\x02\x00\x01 448a8d487adfc99ec697033edc2a1227\x00\x00\x00\x02\x00\x00\x00\x00?\x80\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x01\x08duration\x00\x00\x00\x00\x00\x00\x00\x03\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x01\x04Line\x02\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x02\x03Out\x02\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00')),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1000, 0, 0, 'duration', 2.0),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1001, 0, 0, 'duration', 4.0),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1002, 0, 0, 'duration', 5.0),
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1003, 0, 0, 'duration', 5.0),
                    )
                ),
            osctools.OscBundle(
                timestamp=1.0,
                contents=(
                    osctools.OscMessage('/s_new', '448a8d487adfc99ec697033edc2a1227', 1004, 0, 0, 'duration', 4.0),
                    )
                ),
            osctools.OscBundle(
                timestamp=2.0,
                contents=(
                    osctools.OscMessage('/n_free', 1000),
                    )
                ),
            osctools.OscBundle(
                timestamp=4.0,
                contents=(
                    osctools.OscMessage('/n_free', 1001),
                    )
                ),
            osctools.OscBundle(
                timestamp=5.0,
                contents=(
                    osctools.OscMessage('/n_free', 1002, 1003, 1004),
                    osctools.OscMessage(0),
                    )
                )
            ]

    def test_03(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            group_a = session.add_group()
            group_b = group_a.add_group()
            synth_a = group_a.add_synth(synthdef=synthdefs.default)
            synth_b = group_b.add_synth(synthdef=synthdefs.default)
        with session.at(2):
            group_a['frequency'] = 440
            group_b['frequency'] = 441
            synth_a['frequency'] = 442
            synth_b['frequency'] = 443
        with session.at(4): 
            group_b.move_node(synth_a)
            group_a['frequency'] = 444
            group_b['frequency'] = 445
            synth_a['frequency'] = 446
            synth_b['frequency'] = 447
        assert session.to_osc_bundles(duration=6) == [
            osctools.OscBundle(
                timestamp=0.0,
                contents=(
                    osctools.OscMessage('/d_recv', bytearray(b'SCgf\x00\x00\x00\x02\x00\x01\x07default\x00\x00\x00\x0c\x00\x00\x00\x00>\x99\x99\x9a<#\xd7\n?333@\x00\x00\x00\xbe\xcc\xcc\xcd>\xcc\xcc\xcdEz\x00\x00E\x9c@\x00E\x1c@\x00EH\x00\x00?\x80\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00=\xcc\xcc\xcdC\xdc\x00\x00?\x80\x00\x00?\x00\x00\x00\x00\x00\x00\x05\tamplitude\x00\x00\x00\x01\tfrequency\x00\x00\x00\x02\x04gate\x00\x00\x00\x03\x03out\x00\x00\x00\x00\x03pan\x00\x00\x00\x04\x00\x00\x00\x14\x07Control\x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x07Control\x01\x00\x00\x00\x00\x00\x00\x00\x04\x00\x01\x01\x01\x01\x01\x06VarSaw\x02\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x02\x05Linen\x01\x00\x00\x00\x05\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x02\xff\xff\xff\xff\x00\x00\x00\x02\xff\xff\xff\xff\x00\x00\x00\x03\xff\xff\xff\xff\x00\x00\x00\x01\xff\xff\xff\xff\x00\x00\x00\x04\x01\x04Rand\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x05\xff\xff\xff\xff\x00\x00\x00\x00\x00\x0cBinaryOpUGen\x01\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x04\x00\x00\x00\x00\x01\x06VarSaw\x02\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x05\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x02\x04Rand\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x06\x00\x0cBinaryOpUGen\x01\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x07\x00\x00\x00\x00\x01\x06VarSaw\x02\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x08\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x02\x04Sum3\x02\x00\x00\x00\x03\x00\x00\x00\x01\x00\x00\x00\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x06\x00\x00\x00\x00\x00\x00\x00\t\x00\x00\x00\x00\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02\x00\x00\x00\n\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x01\x02\x04Rand\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\x07\xff\xff\xff\xff\x00\x00\x00\x08\x00\x04Rand\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\xff\xff\xff\xff\x00\x00\x00\t\xff\xff\xff\xff\x00\x00\x00\n\x00\x05XLine\x01\x00\x00\x00\x04\x00\x00\x00\x01\x00\x00\x00\x00\x00\x0c\x00\x00\x00\x00\x00\x00\x00\r\x00\x00\x00\x00\xff\xff\xff\xff\x00\x00\x00\x0b\xff\xff\xff\xff\x00\x00\x00\x00\x01\x03LPF\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x00\x00\x0b\x00\x00\x00\x00\x00\x00\x00\x0e\x00\x00\x00\x00\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02\x00\x00\x00\x0f\x00\x00\x00\x00\x00\x00\x00\x03\x00\x00\x00\x00\x02\x0cBinaryOpUGen\x02\x00\x00\x00\x02\x00\x00\x00\x01\x00\x02\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x02\x04Pan2\x02\x00\x00\x00\x03\x00\x00\x00\x02\x00\x00\x00\x00\x00\x11\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x03\xff\xff\xff\xff\x00\x00\x00\x0b\x02\x02\tOffsetOut\x02\x00\x00\x00\x03\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00\x00\x00\x00\x00\x12\x00\x00\x00\x01\x00\x00')),
                    osctools.OscMessage('/g_new', 1000, 0, 0),
                    osctools.OscMessage('/g_new', 1001, 0, 1000),
                    osctools.OscMessage('/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1000),
                    osctools.OscMessage('/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 1001),
                    )
                ),
            osctools.OscBundle(
                timestamp=2.0,
                contents=(
                    osctools.OscMessage('/n_set', 1000, 'frequency', 440),
                    osctools.OscMessage('/n_set', 1002, 'frequency', 442),
                    osctools.OscMessage('/n_set', 1001, 'frequency', 441),
                    osctools.OscMessage('/n_set', 1003, 'frequency', 443),
                    )
                ),
            osctools.OscBundle(
                timestamp=4.0,
                contents=(
                    osctools.OscMessage('/g_head', 1001, 1002),
                    osctools.OscMessage('/n_set', 1000, 'frequency', 444),
                    osctools.OscMessage('/n_set', 1001, 'frequency', 445),
                    osctools.OscMessage('/n_set', 1002, 'frequency', 446),
                    osctools.OscMessage('/n_set', 1003, 'frequency', 447),
                    )
                ),
            osctools.OscBundle(
                timestamp=6.0,
                contents=(
                    osctools.OscMessage('/n_free', 1000, 1001),
                    osctools.OscMessage('/n_set', 1002, 'gate', 0),
                    osctools.OscMessage('/n_set', 1003, 'gate', 0),
                    osctools.OscMessage(0),
                    )
                )
            ]

