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
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
        ''',
        ), remote_state

    synth = servertools.Synth(synthdefs.test)
    assert synth.parent is None
    assert not synth.is_allocated

    group[:] = [synth]
    assert len(group) == 1
    assert synth.parent is group
    assert synth in group
    assert synth.is_allocated
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
        ''',
        ), remote_state

    group[:] = []
    assert len(group) == 0
    assert synth.parent is None
    assert synth not in group
    assert not synth.is_allocated
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
        ''',
        ), remote_state


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
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 test
        ''',
        ), remote_state

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
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                    1001 test
        ''',
        ), remote_state

    group[:] = []
    assert len(group) == 0
    assert synth_a.parent is None
    assert synth_b.parent is None
    assert synth_a not in group
    assert synth_b not in group
    assert not synth_a.is_allocated
    assert not synth_b.is_allocated
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
        ''',
        ), remote_state


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

    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
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
        ), remote_state

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

    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
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
        ), remote_state

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

    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                    1002 group
                        1003 test
                        1005 group
        ''',
        ), remote_state

    assert len(group_a) == 2
    assert len(group_b) == 2
    assert len(group_c) == 0

    assert synth_a.parent is group_a
    assert synth_b.parent is group_b
    assert synth_c.parent is None
    assert synth_d.parent is None
    assert group_b.parent is group_a
    assert group_c.parent is group_b

    assert synth_a is group_a[0]
    assert synth_b is group_b[0]
    assert synth_c not in group_b
    assert synth_d not in group_a
    assert group_b is group_a[1]
    assert group_c is group_b[1]

    del(group_a[0])

    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1003 test
                        1005 group
        ''',
        ), remote_state

    assert len(group_a) == 1
    assert len(group_b) == 2
    assert len(group_c) == 0

    assert synth_a.parent is None
    assert synth_b.parent is group_b
    assert synth_c.parent is None
    assert synth_d.parent is None
    assert group_b.parent is group_a
    assert group_c.parent is group_b

    assert synth_a not in group_a
    assert synth_b is group_b[0]
    assert synth_c not in group_b
    assert synth_d not in group_a
    assert group_b is group_a[0]
    assert group_c is group_b[1]

    del(group_b[1])

    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 group
                        1003 test
        ''',
        ), remote_state

    assert len(group_a) == 1
    assert len(group_b) == 1
    assert len(group_c) == 0

    assert synth_a.parent is None
    assert synth_b.parent is group_b
    assert synth_c.parent is None
    assert synth_d.parent is None
    assert group_b.parent is group_a
    assert group_c.parent is None

    assert synth_a not in group_a
    assert synth_b is group_b[0]
    assert synth_c not in group_b
    assert synth_d not in group_a
    assert group_b is group_a[0]
    assert group_c not in group_b

    del(group_a[0])

    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1000 group
        ''',
        ), remote_state

    assert len(group_a) == 0
    assert len(group_b) == 1
    assert len(group_c) == 0

    assert synth_a.parent is None
    assert synth_b.parent is group_b
    assert synth_c.parent is None
    assert synth_d.parent is None
    assert group_b.parent is None
    assert group_c.parent is None

    assert synth_a not in group_a
    assert synth_b is group_b[0]
    assert synth_c not in group_b
    assert synth_d not in group_a
    assert group_b not in group_a
    assert group_c not in group_b

    assert not synth_b.is_allocated


def test_Group___setitem___04(server):

    group_a = servertools.Group().allocate()
    group_b = servertools.Group().allocate()

    synth_a = servertools.Synth(synthdefs.test)
    synth_b = servertools.Synth(synthdefs.test)
    synth_c = servertools.Synth(synthdefs.test)
    synth_d = servertools.Synth(synthdefs.test)
    synth_e = servertools.Synth(synthdefs.test)
    synth_f = servertools.Synth(synthdefs.test)

    local_state = str(server.query_local_nodes())
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
        ''',
        ), remote_state
    assert local_state == remote_state
    assert len(group_a) == 0
    assert len(group_b) == 0

    group_a[:] = [synth_a, synth_b]

    local_state = str(server.query_local_nodes())
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
    assert local_state == remote_state
    assert len(group_a) == 2
    assert len(group_b) == 0

    group_a[:] = [synth_b, synth_a]

    local_state = str(server.query_local_nodes())
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                1000 group
                    1003 test
                    1002 test
        ''',
        ), remote_state
    assert local_state == remote_state
    assert len(group_a) == 2
    assert len(group_b) == 0

    group_a[:] = [synth_c, synth_d, synth_b, synth_a]

    local_state = str(server.query_local_nodes())
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
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
        ), remote_state
    assert local_state == remote_state
    assert len(group_a) == 4
    assert len(group_b) == 0

    group_b[1:-1] = [synth_c, synth_b]

    local_state = str(server.query_local_nodes())
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
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
        ), remote_state
    assert local_state == remote_state
    assert len(group_a) == 2
    assert len(group_b) == 2

    group_b[1:-1] = [synth_b, synth_c, synth_e]

    local_state = str(server.query_local_nodes())
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
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
        ), remote_state
    assert local_state == remote_state
    assert len(group_a) == 2
    assert len(group_b) == 3

    group_a[:] = [synth_c, synth_f]

    local_state = str(server.query_local_nodes())
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
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
        ), remote_state
    assert local_state == remote_state
    assert len(group_a) == 2
    assert len(group_b) == 2

    group_a[:-1] = [synth_f]

    local_state = str(server.query_local_nodes())
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                    1006 test
                1000 group
                    1007 test
        ''',
        ), remote_state
    assert local_state == remote_state
    assert len(group_a) == 1
    assert len(group_b) == 2

    group_b[len(group_b):] = [group_a]

    local_state = str(server.query_local_nodes())
    remote_state = str(server.query_remote_nodes())
    assert systemtools.TestManager.compare(
        remote_state,
        '''
        NODE TREE 0 group
            1 group
                1001 group
                    1003 test
                    1006 test
                    1000 group
                        1007 test
        ''',
        ), remote_state
    assert local_state == remote_state
    assert len(group_a) == 1
    assert len(group_b) == 3