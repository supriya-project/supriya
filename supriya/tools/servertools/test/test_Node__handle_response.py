# -*- encoding: utf-8 -*- import pytest
import pytest
from abjad.tools import systemtools
from supriya import synthdefs
from supriya.tools import osctools
from supriya.tools import servertools


@pytest.fixture(scope='function')
def server(request):
    def server_teardown():
        server.quit()
    server = servertools.Server().boot()
    server.debug_osc = True
    request.addfinalizer(server_teardown)
    return server


def test_Node__handle_response(server):

    group_a = servertools.Group().allocate()
    group_b = servertools.Group().allocate()

    synth_a = servertools.Synth(synthdefs.test)
    synth_b = servertools.Synth(synthdefs.test)

    group_a.append(synth_a)
    group_b.append(synth_b)

    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                1000 group
                    1002 test
        ''',
        ), remote_state
    local_state = str(server.query_local_nodes())
    assert local_state == remote_state

    osc_message = osctools.OscMessage(
        '/n_after',
        synth_b.node_id,
        synth_a.node_id,
        )
    server.send_message(osc_message)

    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1002 test
                    1003 test
        ''',
        ), remote_state
    local_state = str(server.query_local_nodes())
    assert local_state == remote_state

    osc_message = osctools.OscMessage(
        '/n_order',
        0,
        group_b.node_id,
        synth_b.node_id,
        synth_a.node_id,
        )
    server.send_message(osc_message)

    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                    1002 test
                1000 group
        ''',
        ), remote_state
    local_state = str(server.query_local_nodes())
    assert local_state == remote_state