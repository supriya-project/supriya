# -*- encoding: utf-8 -*-
import os
import unittest
from supriya.tools import miditools


@unittest.skipIf(os.environ.get('TRAVIS') == 'true', 'No MIDI on Travis-CI')
class Test(unittest.TestCase):

    def test_01(self):

        dispatcher = miditools.MidiDispatcher()

        callback_a = miditools.MidiController(
            channel_number=None,
            controller_number=None,
            )

        callback_b = miditools.MidiController(
            channel_number=1,
            controller_number=None,
            )

        callback_c = miditools.MidiController(
            channel_number=None,
            controller_number=17,
            )

        callback_d = miditools.MidiController(
            channel_number=1,
            controller_number=17,
            )

        callback_e = miditools.MidiController(
            channel_number=2,
            controller_number=17,
            )

        callback_f = miditools.MidiController(
            channel_number=2,
            controller_number=18,
            )

        dispatcher.register_callback(callback_a)
        dispatcher.register_callback(callback_b)
        dispatcher.register_callback(callback_c)
        dispatcher.register_callback(callback_d)
        dispatcher.register_callback(callback_e)
        dispatcher.register_callback(callback_f)

        message = miditools.ControllerChangeMessage(
            channel_number=1,
            controller_number=17,
            controller_value=64,
            )
        collected_callbacks = dispatcher.collect_callbacks(message)
        assert collected_callbacks == set([
            callback_a,
            callback_b,
            callback_c,
            callback_d,
            ])

        message = miditools.ControllerChangeMessage(
            channel_number=1,
            controller_number=18,
            controller_value=64,
            )
        collected_callbacks = dispatcher.collect_callbacks(message)
        assert collected_callbacks == set([
            callback_a,
            callback_b,
            ])

        message = miditools.ControllerChangeMessage(
            channel_number=2,
            controller_number=18,
            controller_value=64,
            )
        collected_callbacks = dispatcher.collect_callbacks(message)
        assert collected_callbacks == set([
            callback_a,
            callback_f,
            ])

        message = miditools.ControllerChangeMessage(
            channel_number=3,
            controller_number=17,
            controller_value=64,
            )
        collected_callbacks = dispatcher.collect_callbacks(message)
        assert collected_callbacks == set([
            callback_a,
            callback_c,
            ])