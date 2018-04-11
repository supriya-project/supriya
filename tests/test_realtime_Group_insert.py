import supriya.realtime
from supriya import synthdefs
from supriya import systemtools


class Test(systemtools.TestCase):

    def setUp(self):
        super(systemtools.TestCase, self).setUp()
        self.server = supriya.realtime.Server().boot()

    def tearDown(self):
        self.server.quit()
        super(systemtools.TestCase, self).tearDown()

    def test_01(self):

        group = supriya.realtime.Group().allocate()

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
            ''',
            )

        synth_a = supriya.realtime.Synth(synthdefs.test)
        group.insert(0, synth_a)

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1001 test
            ''',
            )

        synth_b = supriya.realtime.Synth(synthdefs.test)
        group.insert(0, synth_b)

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1002 test
                        1001 test
            ''',
            )

        synth_c = supriya.realtime.Synth(synthdefs.test)
        group.insert(1, synth_c)

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1002 test
                        1003 test
                        1001 test
            ''',
            )

        synth_d = supriya.realtime.Synth(synthdefs.test)
        group.insert(3, synth_d)

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1002 test
                        1003 test
                        1001 test
                        1004 test
            ''',
            )
