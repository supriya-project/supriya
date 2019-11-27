from uuid import UUID

from supriya.xdaw import RackDevice


def test_1():
    rack_device = RackDevice()
    assert isinstance(rack_device.uuid, UUID)
    assert len(rack_device.chains) == 0
    assert rack_device.application is None
    assert rack_device.context is None
    assert rack_device.graph_order == ()
    assert rack_device.is_active
    assert rack_device.name is None
    assert rack_device.parent is None
    assert rack_device.provider is None
