import supriya.realtime
import supriya.assets.synthdefs
from supriya import systemtools


class Test(systemtools.TestCase):

    def setUp(self):
        super(systemtools.TestCase, self).setUp()
        self.server = supriya.realtime.Server().boot()

    def tearDown(self):
        self.server.quit()
        super(systemtools.TestCase, self).tearDown()

    def test_01(self):

        group_a = supriya.realtime.Group()
        group_a.allocate()

        assert len(group_a) == 0

        synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        group_a.append(synth_a)

        assert len(group_a) == 1

        group_b = supriya.realtime.Group()
        group_a.append(group_b)

        assert len(group_a) == 2
        assert len(group_b) == 0

        synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        group_b.append(synth_b)

        assert len(group_a) == 2
        assert len(group_b) == 1

        synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        group_b.append(synth_c)

        assert len(group_a) == 2
        assert len(group_b) == 2

        synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        group_a.append(synth_d)

        assert len(group_a) == 3
        assert len(group_b) == 2

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 test
                        1002 group
                            1003 test
                            1004 test
                        1005 test
            ''',
            )

        assert len(group_a) == 3
        assert len(group_b) == 2

        group_a.pop()

        assert len(group_a) == 2

        group_b.pop()

        assert len(group_b) == 1

        group_a.pop()

        assert len(group_a) == 1
        assert len(group_b) == 1
        assert not group_b[0].is_allocated

        group_a.pop()

        assert len(group_a) == 0

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
            ''',
            )
