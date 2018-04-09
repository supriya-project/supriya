import uqbar.strings
from patterntools_testbase import TestCase
from supriya.tools import patterntools


class TestCase(TestCase):

    pseq_01 = patterntools.Pseq(['A', 'B', 'C', 'D'])

    pseq_02 = patterntools.Pseq([
        patterntools.Pseq(['A', 'B', 'C']),
        patterntools.Pseq(['D', 'E', 'F']),
        ])

    pseq_03 = patterntools.Pseq([
        patterntools.Pbind(
            amplitude=1.0,
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            frequency=patterntools.Pseq([440, 660, 880], 1),
            ),
        patterntools.Pbind(
            amplitude=1.0,
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            frequency=patterntools.Pseq([550, 770, 990], 1),
            ),
        ])

    pseq_04 = patterntools.Pseq([
        patterntools.Pbind(
            amplitude=1.0,
            duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
            frequency=patterntools.Pseq([440, 660, 880], 1),
            ),
        patterntools.Pbus(
            patterntools.Pbind(
                amplitude=1.0,
                duration=patterntools.Pseq([1.0, 2.0, 3.0], 1),
                frequency=patterntools.Pseq([550, 770, 990], 1),
                ),
            ),
        ])

    def test___iter___01(self):
        events = list(self.pseq_01)
        assert events == ['A', 'B', 'C', 'D']

    def test___iter___02(self):
        events = list(self.pseq_02)
        assert events == ['A', 'B', 'C', 'D', 'E', 'F']

    def test___iter___03(self):
        events = list(self.pseq_03)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=440,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=2.0,
                duration=2.0,
                frequency=660,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=3.0,
                duration=3.0,
                frequency=880,
                uuid=UUID('C'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=550,
                uuid=UUID('D'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=2.0,
                duration=2.0,
                frequency=770,
                uuid=UUID('E'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=3.0,
                duration=3.0,
                frequency=990,
                uuid=UUID('F'),
                )
            ''')

    def test___iter___04(self):
        events = list(self.pseq_04)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=440,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=2.0,
                duration=2.0,
                frequency=660,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=3.0,
                duration=3.0,
                frequency=880,
                uuid=UUID('C'),
                )
            CompositeEvent(
                events=(
                    BusEvent(
                        calculation_rate=CalculationRate.AUDIO,
                        channel_count=2,
                        uuid=UUID('D'),
                        ),
                    GroupEvent(
                        uuid=UUID('E'),
                        ),
                    SynthEvent(
                        add_action=AddAction.ADD_AFTER,
                        amplitude=1.0,
                        fade_time=0.25,
                        in_=UUID('D'),
                        synthdef=<SynthDef: system_link_audio_2>,
                        target_node=UUID('E'),
                        uuid=UUID('F'),
                        ),
                    ),
                )
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=550,
                out=UUID('D'),
                target_node=UUID('E'),
                uuid=UUID('G'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=2.0,
                duration=2.0,
                frequency=770,
                out=UUID('D'),
                target_node=UUID('E'),
                uuid=UUID('H'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=3.0,
                duration=3.0,
                frequency=990,
                out=UUID('D'),
                target_node=UUID('E'),
                uuid=UUID('I'),
                )
            CompositeEvent(
                events=(
                    SynthEvent(
                        is_stop=True,
                        uuid=UUID('F'),
                        ),
                    NullEvent(
                        delta=0.25,
                        ),
                    GroupEvent(
                        is_stop=True,
                        uuid=UUID('E'),
                        ),
                    BusEvent(
                        calculation_rate=None,
                        channel_count=None,
                        is_stop=True,
                        uuid=UUID('D'),
                        ),
                    ),
                is_stop=True,
                )
            ''')

    def test_send_01(self):
        events = self.setup_send(self.pseq_01, iterations=2)
        assert events == ['A', 'B']

    def test_send_02a(self):
        events = self.setup_send(self.pseq_02, iterations=2)
        assert events == ['A', 'B']

    def test_send_02b(self):
        events = self.setup_send(self.pseq_02, iterations=3)
        assert events == ['A', 'B', 'C']

    def test_send_02c(self):
        events = self.setup_send(self.pseq_02, iterations=4)
        assert events == ['A', 'B', 'C', 'D']

    def test_send_03a(self):
        events = self.setup_send(self.pseq_03, iterations=2)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=440,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=2.0,
                duration=2.0,
                frequency=660,
                uuid=UUID('B'),
                )
            ''')

    def test_send_03b(self):
        events = self.setup_send(self.pseq_03, iterations=3)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=440,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=2.0,
                duration=2.0,
                frequency=660,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=3.0,
                duration=3.0,
                frequency=880,
                uuid=UUID('C'),
                )
            ''')

    def test_send_03c(self):
        events = self.setup_send(self.pseq_03, iterations=4)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=440,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=2.0,
                duration=2.0,
                frequency=660,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=3.0,
                duration=3.0,
                frequency=880,
                uuid=UUID('C'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=550,
                uuid=UUID('D'),
                )
            ''')

    def test_send_04a(self):
        events = self.setup_send(self.pseq_04, iterations=4)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=440,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=2.0,
                duration=2.0,
                frequency=660,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=3.0,
                duration=3.0,
                frequency=880,
                uuid=UUID('C'),
                )
            CompositeEvent(
                events=(
                    BusEvent(
                        calculation_rate=CalculationRate.AUDIO,
                        channel_count=2,
                        uuid=UUID('D'),
                        ),
                    GroupEvent(
                        uuid=UUID('E'),
                        ),
                    SynthEvent(
                        add_action=AddAction.ADD_AFTER,
                        amplitude=1.0,
                        fade_time=0.25,
                        in_=UUID('D'),
                        synthdef=<SynthDef: system_link_audio_2>,
                        target_node=UUID('E'),
                        uuid=UUID('F'),
                        ),
                    ),
                )
            CompositeEvent(
                events=(
                    SynthEvent(
                        is_stop=True,
                        uuid=UUID('F'),
                        ),
                    NullEvent(
                        delta=0.25,
                        ),
                    GroupEvent(
                        is_stop=True,
                        uuid=UUID('E'),
                        ),
                    BusEvent(
                        calculation_rate=None,
                        channel_count=None,
                        is_stop=True,
                        uuid=UUID('D'),
                        ),
                    ),
                is_stop=True,
                )
            ''')

    def test_send_04b(self):
        events = self.setup_send(self.pseq_04, iterations=5)
        assert self.get_objects_as_string(
            events,
            replace_uuids=True,
        ) == uqbar.strings.normalize('''
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=440,
                uuid=UUID('A'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=2.0,
                duration=2.0,
                frequency=660,
                uuid=UUID('B'),
                )
            NoteEvent(
                amplitude=1.0,
                delta=3.0,
                duration=3.0,
                frequency=880,
                uuid=UUID('C'),
                )
            CompositeEvent(
                events=(
                    BusEvent(
                        calculation_rate=CalculationRate.AUDIO,
                        channel_count=2,
                        uuid=UUID('D'),
                        ),
                    GroupEvent(
                        uuid=UUID('E'),
                        ),
                    SynthEvent(
                        add_action=AddAction.ADD_AFTER,
                        amplitude=1.0,
                        fade_time=0.25,
                        in_=UUID('D'),
                        synthdef=<SynthDef: system_link_audio_2>,
                        target_node=UUID('E'),
                        uuid=UUID('F'),
                        ),
                    ),
                )
            NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=550,
                out=UUID('D'),
                target_node=UUID('E'),
                uuid=UUID('G'),
                )
            CompositeEvent(
                events=(
                    SynthEvent(
                        is_stop=True,
                        uuid=UUID('F'),
                        ),
                    NullEvent(
                        delta=0.25,
                        ),
                    GroupEvent(
                        is_stop=True,
                        uuid=UUID('E'),
                        ),
                    BusEvent(
                        calculation_rate=None,
                        channel_count=None,
                        is_stop=True,
                        uuid=UUID('D'),
                        ),
                    ),
                is_stop=True,
                )
            ''')
