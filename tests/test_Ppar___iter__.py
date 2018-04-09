import uqbar.strings
from supriya.tools import patterntools
from patterntools_testbase import TestCase


class TestCase(TestCase):

    pattern_01 = patterntools.Ppar([
        patterntools.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=patterntools.Pseq([1001, 1002, 1003], 1),
            ),
        ])

    pattern_02 = patterntools.Ppar([
        patterntools.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=patterntools.Pseq([1001, 1002], 1),
            ),
        patterntools.Pmono(
            amplitude=1.0,
            duration=0.75,
            frequency=patterntools.Pseq([2001, 2002, 2003], 1),
            ),
        ])

    pattern_03 = patterntools.Ppar([
        patterntools.Pbind(
            amplitude=1.0,
            duration=1.0,
            frequency=patterntools.Pseq([1001, 1002, 1003], 1),
            ),
        patterntools.Pbind(
            amplitude=1.0,
            duration=0.75,
            frequency=patterntools.Pseq([], 1),
            ),
        ])

    pattern_04 = patterntools.Ppar([
        patterntools.Pbus(
            patterntools.Pbind(
                amplitude=1.0,
                duration=0.75,
                frequency=patterntools.Pseq([1001, 1002, 1003], 1),
                ),
            ),
        ])

    pattern_05 = patterntools.Ppar([
        patterntools.Pbus(
            patterntools.Pbind(
                amplitude=1.0,
                duration=1.0,
                frequency=patterntools.Pseq([1001, 1002], 1),
                ),
            ),
        patterntools.Pbus(
            patterntools.Pmono(
                amplitude=1.0,
                duration=0.75,
                frequency=patterntools.Pseq([2001, 2002, 2003], 1),
                ),
            ),
        ])

    pattern_06 = patterntools.Ppar([
        patterntools.Pgpar([
            [
                patterntools.Pbind(
                    delta=10,
                    duration=10,
                    frequency=patterntools.Pseq([1001, 1002, 1003]),
                    ),
                patterntools.Pbind(
                    delta=12,
                    duration=10,
                    frequency=patterntools.Pseq([2001, 2002, 2003]),
                    ),
                ],
            ]),
        patterntools.Pgpar([
            [
                patterntools.Pbind(
                    delta=10,
                    duration=10,
                    frequency=patterntools.Pseq([3001, 3002]),
                    ),
                patterntools.Pbind(
                    delta=12,
                    duration=10,
                    frequency=patterntools.Pseq([4001, 4002]),
                    ),
                ],
            ]),
        ])

    def test___iter___01(self):
        events = list(self.pattern_01)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1001,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1002,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1003,
                uuid=UUID('C'),
                )
            ''')

    def test___iter___02(self):
        events = list(self.pattern_02)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2001,
                is_stop=False,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=2002,
                is_stop=False,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=1.0,
                frequency=1002,
                uuid=UUID('C'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2003,
                uuid=UUID('B'),
                )
            ''')

    def test___iter___03(self):
        events = list(self.pattern_03)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1001,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1002,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=1003,
                uuid=UUID('C'),
                )
            ''')

    def test___iter___04(self):
        events = list(self.pattern_04)
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
            NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=1001,
                out=UUID('A'),
                target_node=UUID('B'),
                uuid=UUID('D'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=1002,
                out=UUID('A'),
                target_node=UUID('B'),
                uuid=UUID('E'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=1003,
                out=UUID('A'),
                target_node=UUID('B'),
                uuid=UUID('F'),
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

    def test___iter___05(self):
        events = list(self.pattern_05)
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
            NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=1001,
                out=UUID('A'),
                target_node=UUID('B'),
                uuid=UUID('D'),
                )
            CompositeEvent(
                events=(
                    BusEvent(
                        calculation_rate=CalculationRate.AUDIO,
                        channel_count=2,
                        uuid=UUID('E'),
                        ),
                    GroupEvent(
                        uuid=UUID('F'),
                        ),
                    SynthEvent(
                        add_action=AddAction.ADD_AFTER,
                        amplitude=1.0,
                        fade_time=0.25,
                        in_=UUID('E'),
                        synthdef=<SynthDef: system_link_audio_2>,
                        target_node=UUID('F'),
                        uuid=UUID('G'),
                        ),
                    ),
                )
            NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=2001,
                is_stop=False,
                out=UUID('E'),
                target_node=UUID('F'),
                uuid=UUID('H'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=2002,
                is_stop=False,
                out=UUID('E'),
                target_node=UUID('F'),
                uuid=UUID('H'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=1.0,
                frequency=1002,
                out=UUID('A'),
                target_node=UUID('B'),
                uuid=UUID('I'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=0.75,
                frequency=2003,
                out=UUID('E'),
                target_node=UUID('F'),
                uuid=UUID('H'),
                )
            CompositeEvent(
                delta=0.25,
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
            CompositeEvent(
                events=(
                    SynthEvent(
                        is_stop=True,
                        uuid=UUID('G'),
                        ),
                    NullEvent(
                        delta=0.25,
                        ),
                    GroupEvent(
                        is_stop=True,
                        uuid=UUID('F'),
                        ),
                    BusEvent(
                        calculation_rate=None,
                        channel_count=None,
                        is_stop=True,
                        uuid=UUID('E'),
                        ),
                    ),
                is_stop=True,
                )
            ''')

    def test___iter___06(self):
        events = list(self.pattern_06)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            CompositeEvent(
                events=(
                    GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        uuid=UUID('A'),
                        ),
                    ),
                )
            NoteEvent(
                delta=0.0,
                duration=10,
                frequency=1001,
                target_node=UUID('A'),
                uuid=UUID('B'),
                )
            NoteEvent(
                delta=0.0,
                duration=10,
                frequency=2001,
                target_node=UUID('A'),
                uuid=UUID('C'),
                )
            CompositeEvent(
                events=(
                    GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        uuid=UUID('D'),
                        ),
                    ),
                )
            NoteEvent(
                delta=0.0,
                duration=10,
                frequency=3001,
                target_node=UUID('D'),
                uuid=UUID('E'),
                )
            NoteEvent(
                delta=10.0,
                duration=10,
                frequency=4001,
                target_node=UUID('D'),
                uuid=UUID('F'),
                )
            NoteEvent(
                delta=0.0,
                duration=10,
                frequency=1002,
                target_node=UUID('A'),
                uuid=UUID('G'),
                )
            NoteEvent(
                delta=2.0,
                duration=10,
                frequency=3002,
                target_node=UUID('D'),
                uuid=UUID('H'),
                )
            NoteEvent(
                delta=0.0,
                duration=10,
                frequency=2002,
                target_node=UUID('A'),
                uuid=UUID('I'),
                )
            NoteEvent(
                delta=8.0,
                duration=10,
                frequency=4002,
                target_node=UUID('D'),
                uuid=UUID('J'),
                )
            NoteEvent(
                delta=4.0,
                duration=10,
                frequency=1003,
                target_node=UUID('A'),
                uuid=UUID('K'),
                )
            NoteEvent(
                delta=0.0,
                duration=10,
                frequency=2003,
                target_node=UUID('A'),
                uuid=UUID('L'),
                )
            CompositeEvent(
                delta=12.0,
                events=(
                    NullEvent(
                        delta=0.25,
                        ),
                    GroupEvent(
                        is_stop=True,
                        uuid=UUID('D'),
                        ),
                    ),
                is_stop=True,
                )
            CompositeEvent(
                events=(
                    NullEvent(
                        delta=0.25,
                        ),
                    GroupEvent(
                        is_stop=True,
                        uuid=UUID('A'),
                        ),
                    ),
                is_stop=True,
                )
            ''')
