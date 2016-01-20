# -*- encoding: utf-8 -*-
import unittest
from abjad.tools import durationtools
from supriya.tools import nonrealtimetools
from supriya.tools import requesttools
from supriya.tools import servertools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


class TestCase(unittest.TestCase):

    def build_synthdef(self):
        builder = synthdeftools.SynthDefBuilder(
            frequency=440,
            amplitude=1.,
            in_bus=0,
            out_bus=2,
            )
        with builder:
            input_ = ugentools.In.ar(bus=builder['in_bus'])
            source = ugentools.SinOsc.ar(frequency=builder['frequency'])
            source *= builder['amplitude']
            source *= input_
            ugentools.Out.ar(
                bus=builder['out_bus'],
                source=source,
                )
        return builder.build()

    def test_01(self):
        session = nonrealtimetools.NRTSession()
        with session.at(0):
            synth_one = session.add_synth(
                duration=4,
                synthdef=self.build_synthdef(),
                )
        with session.at(2):
            synth_two = session.add_synth(
                duration=6,
                synthdef=self.build_synthdef(),
                frequency=330,
                )

        with session.at(2):
            synth_one['frequency'] = 550
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
            assert synth_two['frequency'] == 330
        with session.at(3):
            assert synth_one['frequency'] == 660
            assert synth_two['frequency'] == 770
        with session.at(4):
            assert synth_two['frequency'] == 880
        with session.at(5):
            assert synth_two['frequency'] == 880

        id_mapping = {synth_one: 1001, synth_two: 1002}

        return

        assert synth_one._collect_requests(id_mapping) == {
            durationtools.Offset(0, 1): [requesttools.SynthNewRequest(
                add_action=servertools.AddAction.ADD_TO_HEAD,
                node_id=1001,
                synthdef='0b294b53cc4d32c522f3e537ffb23f91',
                target_node_id=0
                )],
            durationtools.Offset(2, 1): [requesttools.NodeSetRequest(
                node_id=1001,
                frequency=550
                )],
            durationtools.Offset(3, 1): [requesttools.NodeSetRequest(
                node_id=1001,
                frequency=660
                )],
            durationtools.Offset(4, 1): [requesttools.NodeFreeRequest(
                node_ids=(1001,)
                )],
            }

        assert synth_two._collect_requests(id_mapping) == {
            durationtools.Offset(2, 1): [requesttools.SynthNewRequest(
                add_action=servertools.AddAction.ADD_TO_HEAD,
                node_id=1002,
                synthdef='0b294b53cc4d32c522f3e537ffb23f91',
                target_node_id=0,
                frequency=330
                )],
            durationtools.Offset(3, 1): [requesttools.NodeSetRequest(
                node_id=1002,
                frequency=770
                )],
            durationtools.Offset(4, 1): [requesttools.NodeSetRequest(
                node_id=1002,
                frequency=880
                )],
            durationtools.Offset(6, 1): [requesttools.NodeFreeRequest(
                node_ids=(1002,)
                )],
            }

