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

        synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        synth_e = supriya.realtime.Synth(supriya.assets.synthdefs.test)

        synth_a.allocate()
        synth_b.allocate()

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1001 test
                    1000 test
            ''',
            )

        synth_a.replace_with(synth_c)

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1001 test
                    1002 test
            ''',
            )

        synth_b.replace_with([synth_d, synth_e])

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1003 test
                    1004 test
                    1002 test
            ''',
            )

        synth_c.replace_with([synth_a, synth_e])

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1003 test
                    1005 test
                    1004 test
            ''',
            )
