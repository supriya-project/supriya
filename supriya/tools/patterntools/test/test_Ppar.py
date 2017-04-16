# -*- encoding: utf-8 -*-
import pytest

from supriya import synthdefs
from supriya.tools import nonrealtimetools
from supriya.tools import patterntools

from patterntools_testbase import TestCase


class TestCase(TestCase):

    ppar_01 = patterntools.Ppar([
        patterntools.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=patterntools.Pseq([440, 660], 1),
            ),
        patterntools.Pmono(
            amplitude=1.0,
            duration=0.75,
            frequency=patterntools.Pseq([222, 333, 444], 1),
            ),
        ])

    ppar_02 = patterntools.Ppar([
        patterntools.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=patterntools.Pseq([440, 660, 880], 1),
            ),
        ])

    ppar_03 = patterntools.Ppar([
        patterntools.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=patterntools.Pseq([440, 660, 880], 1),
            ),
        patterntools.Pbind(
            amplitude=1.0,
            duration=0.75,
            frequency=patterntools.Pseq([], 1),
            ),
        ])

    ppar_04 = patterntools.Ppar([
        patterntools.Pbus(
            patterntools.Pbind(
                amplitude=1.0,
                duration=1.0,
                frequency=patterntools.Pseq([440, 660], 1),
                ),
            ),
        patterntools.Pbus(
            patterntools.Pmono(
                amplitude=1.0,
                duration=0.75,
                frequency=patterntools.Pseq([222, 333, 444], 1),
                ),
            ),
        ])

    ppar_05 = patterntools.Ppar([
        patterntools.Pbus(
            patterntools.Pbind(
                amplitude=1.0,
                duration=0.75,
                frequency=patterntools.Pseq([440, 660, 880], 1),
                ),
            ),
        ])

    @pytest.mark.timeout(2)
    def test___iter___01(self):
        events = list(self.ppar_01)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=0.75,
                frequency=222,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=333,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=1.0,
                frequency=660,
                is_stop=True,
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=0.75,
                frequency=444,
                is_stop=True,
                uuid=UUID('B'),
                )
            ''',
            replace_uuids=True,
            )

    @pytest.mark.timeout(2)
    def test___iter___02(self):
        events = list(self.ppar_02)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=660,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=880,
                is_stop=True,
                uuid=UUID('C'),
                )
            ''',
            replace_uuids=True,
            )

    @pytest.mark.timeout(2)
    def test___iter___03(self):
        events = list(self.ppar_03)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=660,
                is_stop=True,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=880,
                is_stop=True,
                uuid=UUID('C'),
                )
            ''',
            replace_uuids=True,
            )

    @pytest.mark.timeout(10)
    def test___iter___04(self):
        events = list(self.ppar_04)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.BusEvent(
                        calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                        channel_count=2,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        uuid=UUID('B'),
                        ),
                    supriya.tools.patterntools.SynthEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_AFTER,
                        amplitude=1.0,
                        delta=0.0,
                        fade_time=0.25,
                        in_=UUID('A'),
                        synthdef=<supriya.tools.synthdeftools.SynthDef('system_link_audio_2')>,
                        target_node=UUID('B'),
                        uuid=UUID('C'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                out=UUID('A'),
                target_node=UUID('B'),
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.BusEvent(
                        calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                        channel_count=2,
                        delta=0.0,
                        uuid=UUID('E'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        uuid=UUID('F'),
                        ),
                    supriya.tools.patterntools.SynthEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_AFTER,
                        amplitude=1.0,
                        delta=0.0,
                        fade_time=0.25,
                        in_=UUID('E'),
                        synthdef=<supriya.tools.synthdeftools.SynthDef('system_link_audio_2')>,
                        target_node=UUID('F'),
                        uuid=UUID('G'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=0.75,
                frequency=222,
                out=UUID('E'),
                target_node=UUID('F'),
                uuid=UUID('H'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=333,
                out=UUID('E'),
                target_node=UUID('F'),
                uuid=UUID('H'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=1.0,
                frequency=660,
                is_stop=True,
                out=UUID('A'),
                target_node=UUID('B'),
                uuid=UUID('I'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=0.75,
                frequency=444,
                is_stop=True,
                out=UUID('E'),
                target_node=UUID('F'),
                uuid=UUID('H'),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.25,
                events=(
                    supriya.tools.patterntools.SynthEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('C'),
                        ),
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('B'),
                        ),
                    supriya.tools.patterntools.BusEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                    is_stop=True,
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.SynthEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('G'),
                        ),
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('F'),
                        ),
                    supriya.tools.patterntools.BusEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('E'),
                        ),
                    ),
                    is_stop=True,
                )
            ''',
            replace_uuids=True,
            )

    def test_send_01a(self):
        events = self.setup_send(self.ppar_01, iterations=1)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            ''',
            replace_uuids=True,
            )

    def test_send_01b(self):
        events = self.setup_send(self.ppar_01, iterations=2)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=0.75,
                frequency=222,
                uuid=UUID('B'),
                )
            ''',
            replace_uuids=True,
            )

    def test_send_01c(self):
        events = self.setup_send(self.ppar_01, iterations=3)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=0.75,
                frequency=222,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=333,
                uuid=UUID('B'),
                )
            ''',
            replace_uuids=True,
            )

    def test_send_01d(self):
        events = self.setup_send(self.ppar_01, iterations=4)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                uuid=UUID('A'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=0.75,
                frequency=222,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=333,
                uuid=UUID('B'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=1.0,
                frequency=660,
                is_stop=True,
                uuid=UUID('C'),
                )
            ''',
            replace_uuids=True,
            )

    def test_send_04a(self):
        events = self.setup_send(self.ppar_04, iterations=1)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.BusEvent(
                        calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                        channel_count=2,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        uuid=UUID('B'),
                        ),
                    supriya.tools.patterntools.SynthEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_AFTER,
                        amplitude=1.0,
                        delta=0.0,
                        fade_time=0.25,
                        in_=UUID('A'),
                        synthdef=<supriya.tools.synthdeftools.SynthDef('system_link_audio_2')>,
                        target_node=UUID('B'),
                        uuid=UUID('C'),
                        ),
                    ),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.SynthEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('C'),
                        ),
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('B'),
                        ),
                    supriya.tools.patterntools.BusEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            ''',
            replace_uuids=True,
            )

    def test_send_04b(self):
        events = self.setup_send(self.ppar_04, iterations=2)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.BusEvent(
                        calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                        channel_count=2,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        uuid=UUID('B'),
                        ),
                    supriya.tools.patterntools.SynthEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_AFTER,
                        amplitude=1.0,
                        delta=0.0,
                        fade_time=0.25,
                        in_=UUID('A'),
                        synthdef=<supriya.tools.synthdeftools.SynthDef('system_link_audio_2')>,
                        target_node=UUID('B'),
                        uuid=UUID('C'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                out=UUID('A'),
                target_node=UUID('B'),
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.SynthEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('C'),
                        ),
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('B'),
                        ),
                    supriya.tools.patterntools.BusEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            ''',
            replace_uuids=True,
            )

    def test_send_04c(self):
        events = self.setup_send(self.ppar_04, iterations=3)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.BusEvent(
                        calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                        channel_count=2,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        uuid=UUID('B'),
                        ),
                    supriya.tools.patterntools.SynthEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_AFTER,
                        amplitude=1.0,
                        delta=0.0,
                        fade_time=0.25,
                        in_=UUID('A'),
                        synthdef=<supriya.tools.synthdeftools.SynthDef('system_link_audio_2')>,
                        target_node=UUID('B'),
                        uuid=UUID('C'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                out=UUID('A'),
                target_node=UUID('B'),
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.BusEvent(
                        calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                        channel_count=2,
                        delta=0.0,
                        uuid=UUID('E'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        uuid=UUID('F'),
                        ),
                    supriya.tools.patterntools.SynthEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_AFTER,
                        amplitude=1.0,
                        delta=0.0,
                        fade_time=0.25,
                        in_=UUID('E'),
                        synthdef=<supriya.tools.synthdeftools.SynthDef('system_link_audio_2')>,
                        target_node=UUID('F'),
                        uuid=UUID('G'),
                        ),
                    ),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.25,
                events=(
                    supriya.tools.patterntools.SynthEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('G'),
                        ),
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('F'),
                        ),
                    supriya.tools.patterntools.BusEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('E'),
                        ),
                    ),
                is_stop=True,
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.SynthEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('C'),
                        ),
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('B'),
                        ),
                    supriya.tools.patterntools.BusEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            ''',
            replace_uuids=True,
            )

    def test_send_04d(self):
        events = self.setup_send(self.ppar_04, iterations=4)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.BusEvent(
                        calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                        channel_count=2,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        uuid=UUID('B'),
                        ),
                    supriya.tools.patterntools.SynthEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_AFTER,
                        amplitude=1.0,
                        delta=0.0,
                        fade_time=0.25,
                        in_=UUID('A'),
                        synthdef=<supriya.tools.synthdeftools.SynthDef('system_link_audio_2')>,
                        target_node=UUID('B'),
                        uuid=UUID('C'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                out=UUID('A'),
                target_node=UUID('B'),
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.BusEvent(
                        calculation_rate=supriya.tools.synthdeftools.CalculationRate.AUDIO,
                        channel_count=2,
                        delta=0.0,
                        uuid=UUID('E'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        uuid=UUID('F'),
                        ),
                    supriya.tools.patterntools.SynthEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_AFTER,
                        amplitude=1.0,
                        delta=0.0,
                        fade_time=0.25,
                        in_=UUID('E'),
                        synthdef=<supriya.tools.synthdeftools.SynthDef('system_link_audio_2')>,
                        target_node=UUID('F'),
                        uuid=UUID('G'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=0.75,
                frequency=222,
                out=UUID('E'),
                target_node=UUID('F'),
                uuid=UUID('H'),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.5,
                events=(
                    supriya.tools.patterntools.SynthEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('C'),
                        ),
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('B'),
                        ),
                    supriya.tools.patterntools.BusEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.SynthEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('G'),
                        ),
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('F'),
                        ),
                    supriya.tools.patterntools.BusEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('E'),
                        ),
                    ),
                is_stop=True,
                )
            ''',
            replace_uuids=True,
            )

    def test_nonrealtime_01a(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            final_offset = session.inscribe(self.ppar_01)
        assert session.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdefs.default.compile())],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1000, 0, 0,
                    'amplitude', 1.0, 'frequency', 440],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1001, 0, 0,
                    'amplitude', 1.0, 'frequency', 222]]],
            [0.75, [
                ['/n_set', 1001, 'amplitude', 1.0, 'frequency', 333]]],
            [1.0, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 0,
                    'amplitude', 1.0, 'frequency', 660],
                ['/n_set', 1000, 'gate', 0]]],
            [1.5, [
                ['/n_set', 1001, 'amplitude', 1.0, 'frequency', 444]]],
            [2.0, [
                ['/n_set', 1002, 'gate', 0]]],
            [2.25, [
                ['/n_set', 1001, 'gate', 0], [0]]]]
        assert final_offset == 2.25

    def test_nonrealtime_01b(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            final_offset = session.inscribe(self.ppar_01, duration=1.75)
        assert session.to_lists() == [
            [0.0, [
                ['/d_recv', bytearray(synthdefs.default.compile())],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1000, 0, 0,
                    'amplitude', 1.0, 'frequency', 440],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1001, 0, 0,
                    'amplitude', 1.0, 'frequency', 222]]],
            [0.75, [
                ['/n_set', 1001, 'amplitude', 1.0, 'frequency', 333]]],
            [1.0, [
                ['/n_set', 1000, 'gate', 0]]],
            [1.5, [
                ['/n_set', 1001, 'gate', 0],
                [0]]]]
        assert final_offset == 1.5

    def test_nonrealtime_04a(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            final_offset = session.inscribe(self.ppar_04)
        d_recv_commands = []
        for synthdef in sorted(
            [synthdefs.system_link_audio_2, synthdefs.default],
            key=lambda x: x.anonymous_name,
            ):
            compiled_synthdef = bytearray(synthdef.compile())
            d_recv_commands.append(['/d_recv', compiled_synthdef])
        assert session.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/g_new', 1000, 0, 0],
                ['/s_new', '38a2c79fc9d58d06e361337163a4e80f', 1001, 3, 1000,
                    'fade_time', 0.25, 'in_', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1000,
                    'amplitude', 1.0, 'frequency', 440, 'out', 16],
                ['/g_new', 1003, 0, 0],
                ['/s_new', '38a2c79fc9d58d06e361337163a4e80f', 1004, 3, 1003,
                    'fade_time', 0.25, 'in_', 18],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1005, 0, 1003,
                    'amplitude', 1.0, 'frequency', 222, 'out', 18]]],
            [0.75, [
                ['/n_set', 1005, 'amplitude', 1.0, 'frequency', 333]]],
            [1.0, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1006, 0, 1000,
                    'amplitude', 1.0, 'frequency', 660, 'out', 16],
                ['/n_set', 1002, 'gate', 0]]],
            [1.5, [
                ['/n_set', 1005, 'amplitude', 1.0, 'frequency', 444]]],
            [2.0, [
                ['/n_set', 1001, 'gate', 0],
                ['/n_set', 1006, 'gate', 0]]],
            [2.25, [
                ['/n_free', 1000],
                ['/n_set', 1004, 'gate', 0],
                ['/n_set', 1005, 'gate', 0]]],
            [2.5, [
                ['/n_free', 1003],
                [0]]]]
        assert final_offset == 2.5

    def test_nonrealtime_04b(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            final_offset = session.inscribe(self.ppar_04, duration=1.75)
        d_recv_commands = []
        for synthdef in sorted(
            [synthdefs.system_link_audio_2, synthdefs.default],
            key=lambda x: x.anonymous_name,
            ):
            compiled_synthdef = bytearray(synthdef.compile())
            d_recv_commands.append(['/d_recv', compiled_synthdef])
        assert session.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/g_new', 1000, 0, 0],
                ['/s_new', '38a2c79fc9d58d06e361337163a4e80f', 1001, 3, 1000,
                    'fade_time', 0.25, 'in_', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1000,
                    'amplitude', 1.0, 'frequency', 440, 'out', 16],
                ['/g_new', 1003, 0, 0],
                ['/s_new', '38a2c79fc9d58d06e361337163a4e80f', 1004, 3, 1003,
                    'fade_time', 0.25, 'in_', 18],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1005, 0, 1003,
                    'amplitude', 1.0, 'frequency', 222, 'out', 18]]],
            [0.75, [
                ['/n_set', 1005, 'amplitude', 1.0, 'frequency', 333]]],
            [1.0, [
                ['/n_set', 1001, 'gate', 0],
                ['/n_set', 1002, 'gate', 0]]],
            [1.25, [
                ['/n_free', 1000]]],
            [1.5, [
                ['/n_set', 1004, 'gate', 0],
                ['/n_set', 1005, 'gate', 0]]],
            [1.75, [
                ['/n_free', 1003],
                [0]]]]

        assert final_offset == 1.75

    def test_nonrealtime_05a(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            final_offset = session.inscribe(self.ppar_05)
        d_recv_commands = []
        for synthdef in sorted(
            [synthdefs.system_link_audio_2, synthdefs.default],
            key=lambda x: x.anonymous_name,
            ):
            compiled_synthdef = bytearray(synthdef.compile())
            d_recv_commands.append(['/d_recv', compiled_synthdef])
        assert session.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/g_new', 1000, 0, 0],
                ['/s_new', '38a2c79fc9d58d06e361337163a4e80f', 1001, 3, 1000,
                    'fade_time', 0.25, 'in_', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1000,
                    'amplitude', 1.0, 'frequency', 440, 'out', 16]]],
            [0.75, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 1000,
                    'amplitude', 1.0, 'frequency', 660, 'out', 16],
                ['/n_set', 1002, 'gate', 0]]],
            [1.5, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 1000,
                    'amplitude', 1.0, 'frequency', 880, 'out', 16],
                ['/n_set', 1003, 'gate', 0]]],
            [2.25, [
                ['/n_set', 1001, 'gate', 0],
                ['/n_set', 1004, 'gate', 0]]],
            [2.5, [
                ['/n_free', 1000],
                [0]]]]
        assert final_offset == 2.5

    def test_nonrealtime_05b(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            final_offset = session.inscribe(self.ppar_05, duration=1.75)
        d_recv_commands = []
        for synthdef in sorted(
            [synthdefs.system_link_audio_2, synthdefs.default],
            key=lambda x: x.anonymous_name,
            ):
            compiled_synthdef = bytearray(synthdef.compile())
            d_recv_commands.append(['/d_recv', compiled_synthdef])
        assert session.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/g_new', 1000, 0, 0],
                ['/s_new', '38a2c79fc9d58d06e361337163a4e80f', 1001, 3, 1000,
                    'fade_time', 0.25, 'in_', 16],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1000,
                    'amplitude', 1.0, 'frequency', 440, 'out', 16]]],
            [0.75, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 1000,
                    'amplitude', 1.0, 'frequency', 660, 'out', 16],
                ['/n_set', 1002, 'gate', 0]]],
            [1.5, [
                ['/n_set', 1001, 'gate', 0],
                ['/n_set', 1003, 'gate', 0]]],
            [1.75, [
                ['/n_free', 1000],
                [0]]]]
        assert final_offset == 1.75
