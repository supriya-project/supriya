# -*- encoding: utf-8 -*-
from patterntools_testbase import TestCase
from supriya import synthdefs
from supriya.tools import nonrealtimetools
from supriya.tools import patterntools
from supriya.tools import synthdeftools
from supriya.tools import ugentools


class TestCase(TestCase):

    with synthdeftools.SynthDefBuilder(in_=0, out=0) as builder:
        source = ugentools.In.ar(bus=builder['in_'])
        source = ugentools.Limiter.ar(source=source)
        ugentools.Out.ar(bus=builder['out'], source=source)
    limiter_synthdef = builder.build()

    pattern = patterntools.Pbind(
        amplitude=1.0,
        duration=1.0,
        frequency=patterntools.Pseq([440, 660, 880], 1),
        synthdef=synthdefs.default,
        )
    pattern = pattern.with_group()
    pattern = pattern.with_effect(synthdef=limiter_synthdef)
    pattern = pattern.with_bus()

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test___iter__(self):
        events = list(self.pattern)
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
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        in_=UUID('A'),
                        out=UUID('A'),
                        synthdef=<supriya.tools.synthdeftools.SynthDef('38bda0aee6d0e2d4af72be83c09d9b77')>,
                        target_node=UUID('B'),
                        uuid=UUID('D'),
                        ),
                    ),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.GroupEvent(
                        add_action=supriya.tools.servertools.AddAction.ADD_TO_HEAD,
                        delta=0.0,
                        target_node=UUID('B'),
                        uuid=UUID('E'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=440,
                is_stop=True,
                out=UUID('A'),
                synthdef=<supriya.tools.synthdeftools.SynthDef('default')>,
                target_node=UUID('E'),
                uuid=UUID('F'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=660,
                is_stop=True,
                out=UUID('A'),
                synthdef=<supriya.tools.synthdeftools.SynthDef('default')>,
                target_node=UUID('E'),
                uuid=UUID('G'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                duration=1.0,
                frequency=880,
                is_stop=True,
                out=UUID('A'),
                synthdef=<supriya.tools.synthdeftools.SynthDef('default')>,
                target_node=UUID('E'),
                uuid=UUID('H'),
                )
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.GroupEvent(
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
                    supriya.tools.patterntools.NullEvent(
                        delta=0.25,
                        ),
                    supriya.tools.patterntools.SynthEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('D'),
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

    def test_nonrealtime(self):
        session = nonrealtimetools.Session()
        with session.at(0):
            final_offset = session.inscribe(self.pattern)
        d_recv_commands = []
        for synthdef in sorted(
            [
                synthdefs.system_link_audio_2,
                synthdefs.default,
                self.limiter_synthdef,
                ],
            key=lambda x: x.anonymous_name,
            ):
            compiled_synthdef = bytearray(synthdef.compile())
            d_recv_commands.append(['/d_recv', compiled_synthdef])
        assert session.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/g_new', 1000, 0, 0],
                ['/s_new', synthdefs.system_link_audio_2.anonymous_name, 1001, 3, 1000,
                    'fade_time', 0.25, 'in_', 16],
                ['/s_new', self.limiter_synthdef.anonymous_name, 1002, 1, 1000,
                    'in_', 16.0, 'out', 16.0],
                ['/g_new', 1003, 0, 1000],
                ['/s_new', synthdefs.default.anonymous_name, 1004, 0, 1003,
                    'amplitude', 1.0, 'frequency', 440, 'out', 16]]],
            [1.0, [
                ['/s_new', synthdefs.default.anonymous_name, 1005, 0, 1003,
                    'amplitude', 1.0, 'frequency', 660, 'out', 16],
                ['/n_set', 1004, 'gate', 0]]],
            [2.0, [
                ['/s_new', synthdefs.default.anonymous_name, 1006, 0, 1003,
                    'amplitude', 1.0, 'frequency', 880, 'out', 16],
                ['/n_set', 1005, 'gate', 0]]],
            [3.0, [
                ['/n_set', 1001, 'gate', 0],
                ['/n_set', 1006, 'gate', 0]]],
            [3.25, [
                ['/n_free', 1000, 1002, 1003],
                [0]]]]
        assert final_offset == 3.25
