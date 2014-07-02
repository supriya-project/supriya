# -*- encoding: utf-8 -*-
import pytest
from supriya import servertools
from supriya import synthdeftools
from supriya import ugentools
from abjad.tools import systemtools


@pytest.fixture(scope='function')
def server(request):
    def server_teardown():
        server.quit()
    server = servertools.Server().boot()
    request.addfinalizer(server_teardown)
    return server


@pytest.fixture(scope='function')
def synthdef(request):
    builder = synthdeftools.SynthDefBuilder()
    builder.add_parameter('frequency', 440)
    builder.add_parameter('amplitude', 1.0, 'audio')
    sin_osc = ugentools.SinOsc.ar(frequency=builder['frequency'])
    enveloped_sin = sin_osc * builder['amplitude']
    out = ugentools.Out.ar(bus=0, source=enveloped_sin)
    builder.add_ugen(out)
    synthdef = builder.build(name='test')
    synthdef.allocate()
    return synthdef


def test_Synth_01(server, synthdef):

    group = servertools.Group().allocate() 

    server.sync()

    synth_a = servertools.Synth(synthdef)
    synth_a.allocate(target_node=group)
    synth_b = servertools.Synth(synthdef)
    synth_b.allocate(target_node=group)

    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert systemtools.TestManager.compare(
        server_state,
        r'''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                        amplitude: 1.0, frequency: 440.0
                    1001 test
                        amplitude: 1.0, frequency: 440.0
        '''
        ), server_state

    synth_a['frequency'] = 443
    synth_a['amplitude'] = 0.5

    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert systemtools.TestManager.compare(
        server_state,
        r'''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                        amplitude: 1.0, frequency: 440.0
                    1001 test
                        amplitude: 0.5, frequency: 443.0
        '''
        ), server_state

    synth_b['frequency', 'amplitude'] = 441, 0.25

    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert systemtools.TestManager.compare(
        server_state,
        r'''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                        amplitude: 0.25, frequency: 441.0
                    1001 test
                        amplitude: 0.5, frequency: 443.0
        '''
        ), server_state

    bus_a = servertools.Bus(rate='control')
    bus_a.allocate()
    bus_b = servertools.Bus(rate='audio')
    bus_b.allocate()
    synth_a['frequency'] = bus_a
    synth_b['amplitude'] = bus_b

    server.sync()
    server_state = str(server.query_remote_nodes(include_controls=True))
    assert systemtools.TestManager.compare(
        server_state,
        r'''
        NODE TREE 0 group
            1 group
                1000 group
                    1002 test
                        amplitude: a16, frequency: 441.0
                    1001 test
                        amplitude: 0.5, frequency: c0
        '''
        ), server_state
