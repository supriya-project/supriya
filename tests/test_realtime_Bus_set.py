import supriya.realtime


def test_01(server):

    control_bus = supriya.realtime.Bus.control()
    control_bus.allocate()

    assert control_bus.is_allocated

    result = control_bus.get()
    assert result == 0.0
    assert control_bus.value == result

    control_bus.set(0.5)
    result = control_bus.get()
    assert result == 0.5
    assert control_bus.value == result

    control_bus.set(0.25)
    result = control_bus.get()
    assert result == 0.25
    assert control_bus.value == result
