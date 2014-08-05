# -*- encoding: utf-8 -*-
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


def test_Node_replace_01(server):

    synth_a = servertools.Synth(synthdefs.test)
    synth_b = servertools.Synth(synthdefs.test)
    synth_c = servertools.Synth(synthdefs.test)
    synth_d = servertools.Synth(synthdefs.test)
    synth_e = servertools.Synth(synthdefs.test)

    synth_a.allocate()
    synth_b.allocate()

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 test
                1000 test
        ''',
        ), server_state

    synth_a.replace(synth_c) 

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 test
                1002 test
        ''',
        ), server_state

    synth_b.replace([synth_d, synth_e])

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1003 test
                1004 test
                1002 test
        ''',
        ), server_state

    synth_c.replace([synth_a, synth_e])

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1003 test
                1005 test
                1004 test
        ''',
        ), server_state
