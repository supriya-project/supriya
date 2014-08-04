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


def test_Group_insert_01(server):

    group = servertools.Group().allocate()

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
        ''',
        ), server_state

    synth_a = servertools.Synth(synthdefs.test)
    group.insert(0, synth_a)

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
        ''',
        ), server_state

    synth_b = servertools.Synth(synthdefs.test)
    group.insert(0, synth_b)

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                    1001 test
        ''',
        ), server_state

    synth_c = servertools.Synth(synthdefs.test)
    group.insert(1, synth_c)

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                    1003 test
                    1001 test
        ''',
        ), server_state

    synth_d = servertools.Synth(synthdefs.test)
    group.insert(3, synth_d)

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
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
        ), server_state
