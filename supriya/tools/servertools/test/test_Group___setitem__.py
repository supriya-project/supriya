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


def test_Group___setitem___03(server):

    group_a = servertools.Group()
    group_a.allocate()

    synth_a = servertools.Synth(synthdefs.test)
    group_a.append(synth_a)

    group_b = servertools.Group()
    group_a.append(group_b)

    synth_b = servertools.Synth(synthdefs.test)
    group_b.append(synth_b)

    synth_c = servertools.Synth(synthdefs.test)
    group_b.append(synth_c)

    group_c = servertools.Group()
    group_b.append(group_c)

    synth_d = servertools.Synth(synthdefs.test)
    group_a.append(synth_d)

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
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
        ), server_state

    assert len(group_a) == 3
    assert len(group_b) == 3
    assert len(group_c) == 0

    assert synth_a.parent is group_a
    assert synth_b.parent is group_b
    assert synth_c.parent is group_b
    assert synth_d.parent is group_a
    assert group_b.parent is group_a
    assert group_c.parent is group_b

    assert synth_a is group_a[0]
    assert synth_b is group_b[0]
    assert synth_c is group_b[1]
    assert synth_d is group_a[2]
    assert group_b is group_a[1]
    assert group_c is group_b[2]

    del(group_a[-1])

    server_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
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
        ), server_state

    assert len(group_a) == 2
    assert len(group_b) == 3
    assert len(group_c) == 0

    assert synth_a.parent is group_a
    assert synth_b.parent is group_b
    assert synth_c.parent is group_b
    assert synth_d.parent is None
    assert group_b.parent is group_a
    assert group_c.parent is group_b

    assert synth_a is group_a[0]
    assert synth_b is group_b[0]
    assert synth_c is group_b[1]
    assert synth_d not in group_a
    assert group_b is group_a[1]
    assert group_c is group_b[2]

    del(group_b[1])

    assert len(group_b) == 2

    del(group_a[0])

    assert len(group_a) == 1

    del(group_b[1])

    assert len(group_b) == 1

    del(group_a[0])

    assert len(group_a) == 0