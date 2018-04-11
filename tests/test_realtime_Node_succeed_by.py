import supriya.realtime
import supriya.assets.synthdefs
import supriya.system


class Test(supriya.system.TestCase):

    def setUp(self):
        super(supriya.system.TestCase, self).setUp()
        self.server = supriya.realtime.Server().boot()

    def tearDown(self):
        self.server.quit()
        super(supriya.system.TestCase, self).tearDown()

    def test_01(self):

        synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        synth_e = supriya.realtime.Synth(supriya.assets.synthdefs.test)

        synth_a.allocate()

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 test
            ''',
            )

        synth_a.succeed_by(synth_b)

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 test
                    1001 test
            ''',
            )

        synth_a.succeed_by([synth_c, synth_d])

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 test
                    1002 test
                    1003 test
                    1001 test
            ''',
            )

        synth_a.succeed_by([synth_e, synth_b])

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 test
                    1004 test
                    1001 test
                    1002 test
                    1003 test
            ''',
            )
