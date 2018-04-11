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

        group_a = supriya.realtime.Group()
        group_a.allocate()
        synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        group_a.append(synth_a)
        group_b = supriya.realtime.Group()
        group_a.append(group_b)
        synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        group_b.append(synth_b)
        synth_c = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        group_b.append(synth_c)
        group_c = supriya.realtime.Group()
        group_b.append(group_c)
        synth_d = supriya.realtime.Synth(supriya.assets.synthdefs.test)
        group_a.append(synth_d)

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
                            1005 group
                        1006 test
            ''',
            )

        group_a.pop()

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
                            1005 group
            ''',
            )

        group_b.pop(1)

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
                            1005 group
            ''',
            )

        group_a.pop(0)

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1002 group
                            1003 test
                            1005 group
            ''',
            )

        group_b.pop()

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
                        1002 group
                            1003 test
            ''',
            )

        group_a.pop()

        server_state = str(self.server.query_remote_nodes())
        self.compare_strings(
            server_state,
            '''
            NODE TREE 0 group
                1 group
                    1000 group
            ''',
            )

        assert not group_b.is_allocated
        assert not group_c.is_allocated
        assert not synth_a.is_allocated
        assert not synth_b.is_allocated
        assert not synth_c.is_allocated
        assert not synth_d.is_allocated
