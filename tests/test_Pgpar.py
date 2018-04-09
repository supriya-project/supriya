from patterntools_testbase import TestCase
from supriya import synthdefs
from supriya.tools import nonrealtimetools
from supriya.tools import patterntools


class TestCase(TestCase):

    pattern = patterntools.Pgpar([
        patterntools.Pmono(
            amplitude=1.0,
            duration=1.0,
            frequency=patterntools.Pseq([440, 660, 880, 990], 1),
            ),
        patterntools.Pbind(
            amplitude=1.0,
            duration=0.75,
            frequency=patterntools.Pseq([222, 333, 444, 555], 1),
            ),
        ])

    def test___iter__(self):
        events = list(self.pattern)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('B'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=False,
                target_node=UUID('A'),
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=222,
                is_stop=True,
                target_node=UUID('B'),
                uuid=UUID('D'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=0.75,
                frequency=333,
                is_stop=True,
                target_node=UUID('B'),
                uuid=UUID('E'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=1.0,
                frequency=660,
                is_stop=False,
                target_node=UUID('A'),
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.5,
                duration=0.75,
                frequency=444,
                is_stop=True,
                target_node=UUID('B'),
                uuid=UUID('F'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.25,
                duration=1.0,
                frequency=880,
                is_stop=False,
                target_node=UUID('A'),
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=555,
                is_stop=True,
                target_node=UUID('B'),
                uuid=UUID('G'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=1.0,
                duration=1.0,
                frequency=990,
                is_stop=True,
                target_node=UUID('A'),
                uuid=UUID('C'),
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
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('B'),
                        ),
                    ),
                is_stop=True,
                )
            ''',
            replace_uuids=True,
            )

    def test_send_01(self):
        events = self.setup_send(self.pattern, iterations=1)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('B'),
                        ),
                    ),
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
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('B'),
                        ),
                    ),
                is_stop=True,
                )
            ''',
            replace_uuids=True,
            )

    def test_send_02(self):
        events = self.setup_send(self.pattern, iterations=2)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('B'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=False,
                target_node=UUID('A'),
                uuid=UUID('C'),
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
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('B'),
                        ),
                    ),
                is_stop=True,
                )
            ''',
            replace_uuids=True,
            )

    def test_send_03(self):
        events = self.setup_send(self.pattern, iterations=3)
        self.compare_objects_as_strings(
            events,
            '''
            supriya.tools.patterntools.CompositeEvent(
                delta=0.0,
                events=(
                    supriya.tools.patterntools.GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        add_action=AddAction.ADD_TO_TAIL,
                        delta=0.0,
                        uuid=UUID('B'),
                        ),
                    ),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.0,
                duration=1.0,
                frequency=440,
                is_stop=False,
                target_node=UUID('A'),
                uuid=UUID('C'),
                )
            supriya.tools.patterntools.NoteEvent(
                amplitude=1.0,
                delta=0.75,
                duration=0.75,
                frequency=222,
                is_stop=True,
                target_node=UUID('B'),
                uuid=UUID('D'),
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
                        uuid=UUID('A'),
                        ),
                    supriya.tools.patterntools.GroupEvent(
                        delta=0.0,
                        is_stop=True,
                        uuid=UUID('B'),
                        ),
                    ),
                is_stop=True,
                )
            ''',
            replace_uuids=True,
            )

    def test_manual_incommunicado(self):
        lists, deltas = self.manual_incommunicado(self.pattern, 10)
        assert lists == [
            [10, [
                ['/g_new', 1000, 1, 1],
                ['/g_new', 1001, 1, 1],
                ['/s_new', 'default', 1002, 0, 1000,
                    'amplitude', 1.0, 'frequency', 440],
                ['/s_new', 'default', 1003, 0, 1001,
                    'amplitude', 1.0, 'frequency', 222]]],
            [10.75, [
                ['/n_set', 1003, 'gate', 0],
                ['/s_new', 'default', 1004, 0, 1001,
                    'amplitude', 1.0, 'frequency', 333]]],
            [11.0, [['/n_set', 1002, 'amplitude', 1.0, 'frequency', 660]]],
            [11.5, [
                ['/n_set', 1004, 'gate', 0],
                ['/s_new', 'default', 1005, 0, 1001,
                    'amplitude', 1.0, 'frequency', 444]]],
            [12.0, [['/n_set', 1002, 'amplitude', 1.0, 'frequency', 880]]],
            [12.25, [
                ['/n_set', 1005, 'gate', 0],
                ['/s_new', 'default', 1006, 0, 1001,
                    'amplitude', 1.0, 'frequency', 555]]],
            [13.0, [
                ['/n_set', 1006, 'gate', 0],
                ['/n_set', 1002, 'amplitude', 1.0, 'frequency', 990]]],
            [14.0, [['/n_set', 1002, 'gate', 0]]],
            [14.25, [['/n_free', 1000, 1001]]]]
        assert deltas == [0.75, 0.25, 0.5, 0.5, 0.25, 0.75, 1.0, 0.25, None]

    def test_nonrealtime(self):
        session = nonrealtimetools.Session()
        with session.at(10):
            session.inscribe(self.pattern)
        d_recv_commands = self.build_d_recv_commands([synthdefs.default])
        assert session.to_lists() == [
            [10.0, [
                *d_recv_commands,
                ['/g_new', 1000, 1, 0],
                ['/g_new', 1001, 1, 0],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1002, 0, 1000,
                    'amplitude', 1.0, 'frequency', 440],
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1003, 0, 1001,
                    'amplitude', 1.0, 'frequency', 222]]],
            [10.75, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1004, 0, 1001,
                    'amplitude', 1.0, 'frequency', 333],
                ['/n_set', 1003, 'gate', 0]]],
            [11.0, [['/n_set', 1002, 'amplitude', 1.0, 'frequency', 660]]],
            [11.5, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1005, 0, 1001,
                    'amplitude', 1.0, 'frequency', 444],
                ['/n_set', 1004, 'gate', 0]]],
            [12.0, [['/n_set', 1002, 'amplitude', 1.0, 'frequency', 880]]],
            [12.25, [
                ['/s_new', 'da0982184cc8fa54cf9d288a0fe1f6ca', 1006, 0, 1001,
                    'amplitude', 1.0, 'frequency', 555],
                ['/n_set', 1005, 'gate', 0]]],
            [13.0, [
                ['/n_set', 1002, 'amplitude', 1.0, 'frequency', 990],
                ['/n_set', 1006, 'gate', 0]]],
            [14.0, [['/n_set', 1002, 'gate', 0]]],
            [14.25, [['/n_free', 1000, 1001], [0]]]]
