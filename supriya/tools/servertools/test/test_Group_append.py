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


def test_Group_append_01(server):

    group_a = servertools.Group()
    group_a.allocate(target_node=server)

    group_b = servertools.Group()
    group_b.allocate(target_node=server)

    synthdef = synthdefs.test
    assert not synthdef.is_allocated

    synth_a = servertools.Synth(synthdef)
    assert not synthdef.is_allocated
    assert not synth_a.is_allocated

    group_a.append(synth_a)
    assert synthdef.is_allocated
    assert synth_a.is_allocated
    assert synth_a.parent is group_a
    assert synth_a in group_a
    assert synth_a not in group_b

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1002 test
        ''',
        ), server_state

    group_b.append(synth_a)
    assert synthdef.is_allocated
    assert synth_a.is_allocated
    assert synth_a.parent is group_b
    assert synth_a in group_b
    assert synth_a not in group_a

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                    1002 test
                1000 group
        ''',
        ), server_state

    synth_b = servertools.Synth(synthdef)
    assert not synth_b.is_allocated
    assert synth_b.parent is None

    group_b.append(synth_b)
    assert synth_b.is_allocated
    assert synth_b.parent is group_b

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                    1002 test
                    1003 test
                1000 group
        ''',
        ), server_state
