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


def test_Group___getitem___01(server):

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

    assert group_a[0] is synth_a
    assert group_a[1] is group_b
    assert group_a[2] is synth_d

    assert group_b[0] is synth_b
    assert group_b[1] is synth_c
    assert group_b[2] is group_c

    assert group_a[-1] is synth_d
    assert group_a[-2] is group_b
    assert group_a[-3] is synth_a

    assert group_b[-1] is group_c
    assert group_b[-2] is synth_c
    assert group_b[-3] is synth_b

    assert group_a[:] == [synth_a, group_b, synth_d]
    assert group_a[1:] == [group_b, synth_d]
    assert group_a[1:-1] == [group_b]
    assert group_a[2:] == [synth_d]
    assert group_a[:-1] == [synth_a, group_b]
    assert group_a[:-2] == [synth_a]

    assert group_b[:] == [synth_b, synth_c, group_c]
    assert group_b[1:] == [synth_c, group_c]
    assert group_b[1:-1] == [synth_c]
    assert group_b[2:] == [group_c]
    assert group_b[:-1] == [synth_b, synth_c]
    assert group_b[:-2] == [synth_b]