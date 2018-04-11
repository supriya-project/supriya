import uqbar.strings
import supriya.nonrealtime
import supriya.patterns
from patterns_testbase import TestCase
from supriya.tools import synthdeftools
from supriya.tools import ugentools


class TestCase(TestCase):

    with synthdeftools.SynthDefBuilder(in_=0, out=0) as builder:
        source = ugentools.In.ar(bus=builder['in_'])
        source = ugentools.Limiter.ar(source=source)
        ugentools.Out.ar(bus=builder['out'], source=source)
    limiter_synthdef = builder.build()

    pattern = supriya.patterns.Pbind(
        amplitude=1.0,
        duration=1.0,
        frequency=supriya.patterns.Pseq([440, 660, 880], 1),
        synthdef=supriya.assets.synthdefs.default,
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
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            CompositeEvent(
                events=(
                    BusEvent(
                        calculation_rate=CalculationRate.AUDIO,
                        channel_count=2,
                        uuid=UUID('A'),
                        ),
                    GroupEvent(
                        uuid=UUID('B'),
                        ),
                    SynthEvent(
                        add_action=AddAction.ADD_AFTER,
                        amplitude=1.0,
                        fade_time=0.25,
                        in_=UUID('A'),
                        synthdef=<SynthDef: system_link_audio_2>,
                        target_node=UUID('B'),
                        uuid=UUID('C'),
                        ),
                    ),
                )
            CompositeEvent(
                events=(
                    SynthEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        in_=UUID('A'),
                        out=UUID('A'),
                        synthdef=<SynthDef: 38bda0aee6d0e2d4af72be83c09d9b77>,
                        target_node=UUID('B'),
                        uuid=UUID('D'),
                        ),
                    ),
                )
            CompositeEvent(
                events=(
                    GroupEvent(
                        add_action=AddAction.ADD_TO_HEAD,
                        target_node=UUID('B'),
                        uuid=UUID('E'),
                        ),
                    ),
                )
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=440,
                out=UUID('A'),
                synthdef=<SynthDef: default>,
                target_node=UUID('E'),
                uuid=UUID('F'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=660,
                out=UUID('A'),
                synthdef=<SynthDef: default>,
                target_node=UUID('E'),
                uuid=UUID('G'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=880,
                out=UUID('A'),
                synthdef=<SynthDef: default>,
                target_node=UUID('E'),
                uuid=UUID('H'),
                )
            CompositeEvent(
                events=(
                    NullEvent(
                        delta=0.25,
                        ),
                    GroupEvent(
                        is_stop=True,
                        uuid=UUID('E'),
                        ),
                    ),
                is_stop=True,
                )
            CompositeEvent(
                events=(
                    NullEvent(
                        delta=0.25,
                        ),
                    SynthEvent(
                        is_stop=True,
                        uuid=UUID('D'),
                        ),
                    ),
                is_stop=True,
                )
            CompositeEvent(
                events=(
                    SynthEvent(
                        is_stop=True,
                        uuid=UUID('C'),
                        ),
                    NullEvent(
                        delta=0.25,
                        ),
                    GroupEvent(
                        is_stop=True,
                        uuid=UUID('B'),
                        ),
                    BusEvent(
                        calculation_rate=None,
                        channel_count=None,
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            ''')

    def test_nonrealtime(self):
        session = supriya.nonrealtime.Session()
        with session.at(0):
            final_offset = session.inscribe(self.pattern)
        d_recv_commands = self.build_d_recv_commands([
            supriya.assets.synthdefs.system_link_audio_2,
            supriya.assets.synthdefs.default,
            self.limiter_synthdef,
            ])
        assert session.to_lists() == [
            [0.0, [
                *d_recv_commands,
                ['/g_new', 1000, 0, 0],
                ['/s_new', supriya.assets.synthdefs.system_link_audio_2.anonymous_name, 1001, 3, 1000,
                    'fade_time', 0.25, 'in_', 16],
                ['/s_new', self.limiter_synthdef.anonymous_name, 1002, 1, 1000,
                    'in_', 16.0, 'out', 16.0],
                ['/g_new', 1003, 0, 1000],
                ['/s_new', supriya.assets.synthdefs.default.anonymous_name, 1004, 0, 1003,
                    'amplitude', 1.0, 'frequency', 440, 'out', 16]]],
            [1.0, [
                ['/s_new', supriya.assets.synthdefs.default.anonymous_name, 1005, 0, 1003,
                    'amplitude', 1.0, 'frequency', 660, 'out', 16],
                ['/n_set', 1004, 'gate', 0]]],
            [2.0, [
                ['/s_new', supriya.assets.synthdefs.default.anonymous_name, 1006, 0, 1003,
                    'amplitude', 1.0, 'frequency', 880, 'out', 16],
                ['/n_set', 1005, 'gate', 0]]],
            [3.0, [
                ['/n_set', 1001, 'gate', 0],
                ['/n_set', 1006, 'gate', 0]]],
            [3.25, [
                ['/n_free', 1000, 1002, 1003],
                [0]]]]
        assert final_offset == 3.25
