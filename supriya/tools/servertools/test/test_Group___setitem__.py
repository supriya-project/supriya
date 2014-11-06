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


def test_Group___setitem__01(server):

    group = servertools.Group().allocate()
    assert len(group) == 0
    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
        ''',
        ), server_state

    synth = servertools.Synth(synthdefs.test)
    assert synth.parent is None
    assert not synth.is_allocated

    group[:] = [synth]
    assert len(group) == 1
    assert synth.parent is group
    assert synth in group
    assert synth.is_allocated
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

    group[:] = []
    assert len(group) == 0
    assert synth.parent is None
    assert synth not in group
    assert not synth.is_allocated
    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
        ''',
        ), server_state


def test_Group___setitem__02(server):

    group = servertools.Group().allocate()
    synth_a = servertools.Synth(synthdefs.test)
    synth_b = servertools.Synth(synthdefs.test)

    group[:] = [synth_a, synth_b]
    assert len(group) == 2
    assert synth_a.parent is group
    assert synth_b.parent is group
    assert synth_a in group
    assert synth_b in group
    assert synth_a.is_allocated
    assert synth_b.is_allocated
    assert synth_a is group[0]
    assert synth_b is group[1]
    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 test
        ''',
        ), server_state

    group[:] = [synth_b, synth_a]
    assert len(group) == 2
    assert synth_a.parent is group
    assert synth_b.parent is group
    assert synth_a in group
    assert synth_b in group
    assert synth_a.is_allocated
    assert synth_b.is_allocated
    assert synth_a is group[1]
    assert synth_b is group[0]
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

    group[:] = []
    assert len(group) == 0
    assert synth_a.parent is None
    assert synth_b.parent is None
    assert synth_a not in group
    assert synth_b not in group
    assert not synth_a.is_allocated
    assert not synth_b.is_allocated
    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        server_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
        ''',
        ), server_state



#def test_Group___setitem___02(server):
#
#    group_a = servertools.Group().allocate()
#    group_b = servertools.Group().allocate()
#
#    synth_a = servertools.Synth(synthdefs.test)
#    synth_b = servertools.Synth(synthdefs.test)
#    synth_c = servertools.Synth(synthdefs.test)
#    synth_d = servertools.Synth(synthdefs.test)
#    synth_e = servertools.Synth(synthdefs.test)
#    synth_f = servertools.Synth(synthdefs.test)
#
#    server_state = str(server.query_remote_nodes())
#    assert systemtools.TestManager.compare(
#        server_state,
#        '''
#        NODE TREE 0 group
#            1 group
#                1001 group
#                1000 group
#        ''',
#        ), server_state
#
#    group_a[:] = [synth_a, synth_b]
#
#    server_state = str(server.query_remote_nodes())
#    assert systemtools.TestManager.compare(
#        server_state,
#        '''
#        NODE TREE 0 group
#            1 group
#                1001 group
#                1000 group
#                    1002 test
#                    1003 test
#        ''',
#        ), server_state
#
#    group_a[:] = [synth_b, synth_a]
#
#    server_state = str(server.query_remote_nodes())
#    assert systemtools.TestManager.compare(
#        server_state,
#        '''
#        NODE TREE 0 group
#            1 group
#                1001 group
#                1000 group
#                    1003 test
#                    1002 test
#        ''',
#        ), server_state
#
#    group_a[:] = [synth_c, synth_d, synth_b, synth_a]
#
#    server_state = str(server.query_remote_nodes())
#    assert systemtools.TestManager.compare(
#        server_state,
#        '''
#        NODE TREE 0 group
#            1 group
#                1001 group
#                1000 group
#                    1004 test
#                    1005 test
#                    1003 test
#                    1002 test
#        ''',
#        ), server_state
#
#    group_b[1:-1] = [synth_c, synth_b]
#
#    server_state = str(server.query_remote_nodes())
#    assert systemtools.TestManager.compare(
#        server_state,
#        '''
#        NODE TREE 0 group
#            1 group
#                1001 group
#                    1004 test
#                    1003 test
#                1000 group
#                    1005 test
#                    1002 test
#        ''',
#        ), server_state
#
#    group_b[1:-1] = [synth_b, synth_c, synth_e]
#
#    server_state = str(server.query_remote_nodes())
#    assert systemtools.TestManager.compare(
#        server_state,
#        '''
#        NODE TREE 0 group
#            1 group
#                1001 group
#                    1003 test
#                    1004 test
#                    1006 test
#                1000 group
#                    1005 test
#                    1002 test
#        ''',
#        ), server_state
#
#    group_a[:] = [synth_c, synth_f]
#
#    server_state = str(server.query_remote_nodes())
#    assert systemtools.TestManager.compare(
#        server_state,
#        '''
#        NODE TREE 0 group
#            1 group
#                1001 group
#                    1003 test
#                    1006 test
#                1000 group
#                    1004 test
#                    1007 test
#        ''',
#        ), server_state
#
#    group_a[:-1] = [synth_f]
#
#    server_state = str(server.query_remote_nodes())
#    assert systemtools.TestManager.compare(
#        server_state,
#        '''
#        NODE TREE 0 group
#            1 group
#                1001 group
#                    1003 test
#                    1006 test
#                1000 group
#                    1007 test
#        ''',
#        ), server_state
#
#    group_b[len(group_b):] = [group_a]
#
#    server_state = str(server.query_remote_nodes())
#    assert systemtools.TestManager.compare(
#        server_state,
#        '''
#        NODE TREE 0 group
#            1 group
#                1001 group
#                    1003 test
#                    1006 test
#                    1000 group
#                        1007 test
#        ''',
#        ), server_state