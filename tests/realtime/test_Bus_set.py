def test_01(server):

    control_bus = server.add_bus()

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
