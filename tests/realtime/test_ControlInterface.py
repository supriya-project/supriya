from uqbar.strings import normalize

import supriya.assets.synthdefs
import supriya.realtime


def test_01(server):
    group = supriya.realtime.Group()
    synth_a = supriya.realtime.Synth(supriya.assets.synthdefs.test)
    synth_b = supriya.realtime.Synth(supriya.assets.synthdefs.test, amplitude=0.0)
    group.extend([synth_a, synth_b])
    group.allocate(server)
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 0.0, frequency: 440.0
        """
    )
    local_state = str(server.root_node)
    assert local_state == remote_state
    bus_a = supriya.realtime.Bus(calculation_rate="control").allocate(server)
    bus_a.set(0.25)
    group.controls["amplitude"] = bus_a
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: c0, frequency: 440.0
                    1002 test
                        amplitude: c0, frequency: 440.0
        """
    )
    local_state = str(server.root_node)
    assert local_state == remote_state
    bus_b = supriya.realtime.Bus(calculation_rate="control").allocate(server)
    bus_b.set(0.75)
    group.controls["amplitude"] = bus_b
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: c1, frequency: 440.0
                    1002 test
                        amplitude: c1, frequency: 440.0
        """
    )
    local_state = str(server.root_node)
    assert local_state == remote_state
    bus_b.set(0.675)
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: c1, frequency: 440.0
                    1002 test
                        amplitude: c1, frequency: 440.0
        """
    )
    local_state = str(server.root_node)
    assert local_state == remote_state
    group.controls["amplitude"] = None
    remote_state = str(server.query())
    assert remote_state == normalize(
        """
        NODE TREE 0 group
            1 group
                1000 group
                    1001 test
                        amplitude: 1.0, frequency: 440.0
                    1002 test
                        amplitude: 0.0, frequency: 440.0
        """
    )
    local_state = str(server.root_node)
    assert local_state == remote_state
