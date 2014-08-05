# -*- encoding: utf-8 -*- import pytest
import pytest
from abjad.tools import systemtools
from supriya import synthdefs
from supriya.tools import servertools


@pytest.fixture(scope='function')
def server(request):
    def server_teardown():
        server.quit()
    server = servertools.Server().boot()
    request.addfinalizer(server_teardown)
    return server


def test_Group___setitem___01(server):

    group_a = servertools.Group().allocate()
    group_b = servertools.Group().allocate()

    synth_a = servertools.Synth(synthdefs.test)
    synth_b = servertools.Synth(synthdefs.test)
    synth_c = servertools.Synth(synthdefs.test)
    synth_d = servertools.Synth(synthdefs.test)
    synth_e = servertools.Synth(synthdefs.test)
    synth_f = servertools.Synth(synthdefs.test)

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
        ''',
        ), server_state

    group_a[:] = [synth_a, synth_b]

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1002 test
                    1003 test
        ''',
        ), server_state

    group_a[:] = [synth_b, synth_a]

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1003 test
                    1002 test
        ''',
        ), server_state

    group_a[:] = [synth_c, synth_d, synth_b, synth_a]

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1004 test
                    1005 test
                    1003 test
                    1002 test
        ''',
        ), server_state

    group_b[1:-1] = [synth_c, synth_b]

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                    1004 test
                    1003 test
                1000 group
                    1005 test
                    1002 test
        ''',
        ), server_state

    group_b[1:-1] = [synth_b, synth_c, synth_e]

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                    1004 test
                    1006 test
                1000 group
                    1005 test
                    1002 test
        ''',
        ), server_state

    group_a[:] = [synth_c, synth_f]

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                    1006 test
                1000 group
                    1004 test
                    1007 test
        ''',
        ), server_state

    group_a[:-1] = [synth_f]

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                    1006 test
                1000 group
                    1007 test
        ''',
        ), server_state

    group_b[len(group_b):] = [group_a]

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                    1006 test
                    1000 group
                        1007 test
        ''',
        ), server_state
