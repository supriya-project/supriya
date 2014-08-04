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


def test_Group___contains___01(server):

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

    assert group_a not in group_a
    assert group_b in group_a
    assert group_c not in group_a
    assert synth_a in group_a
    assert synth_b not in group_a
    assert synth_c not in group_a
    assert synth_d in group_a

    assert group_a not in group_b
    assert group_b not in group_b
    assert group_c in group_b
    assert synth_a not in group_b
    assert synth_b in group_b
    assert synth_c in group_b
    assert synth_d not in group_b

    assert group_a not in group_c
    assert group_b not in group_c
    assert group_c not in group_c
    assert synth_a not in group_c
    assert synth_b not in group_c
    assert synth_c not in group_c
    assert synth_d not in group_c