from supriya.xdaw import Application, Chain, RackDevice


def test_1():
    """
    Add one chain
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack_device = track.add_device(RackDevice)
    chain = rack_device.add_chain()
    assert chain.application is context.application
    assert chain.graph_order == (1, 0, 0, 0, 3, 0, 0, 0)
    assert chain.parent is rack_device.chains
    assert chain.postfader_sends[0].effective_target is rack_device
    assert chain.provider is context.provider
    assert isinstance(chain, Chain)
    assert len(chain.postfader_sends) == 1
    assert list(rack_device.chains) == [chain]


def test_2():
    """
    Add two chains
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack_device = track.add_device(RackDevice)
    chain_one = rack_device.add_chain()
    chain_two = rack_device.add_chain()
    assert chain_one.application is context.application
    assert chain_one.graph_order == (1, 0, 0, 0, 3, 0, 0, 0)
    assert chain_one.parent is rack_device.chains
    assert chain_one.provider is context.provider
    assert chain_two.application is context.application
    assert chain_two.graph_order == (1, 0, 0, 0, 3, 0, 0, 1)
    assert chain_two.parent is rack_device.chains
    assert chain_two.provider is context.provider
    assert list(rack_device.chains) == [chain_one, chain_two]


def test_3():
    """
    Add one chain, boot, add second chain
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack_device = track.add_device(RackDevice)
    chain_one = rack_device.add_chain()
    application.boot()
    chain_two = rack_device.add_chain()
    assert chain_one.application is context.application
    assert chain_one.graph_order == (1, 0, 0, 0, 3, 0, 0, 0)
    assert chain_one.parent is rack_device.chains
    assert chain_one.provider is context.provider
    assert chain_two.application is context.application
    assert chain_two.graph_order == (1, 0, 0, 0, 3, 0, 0, 1)
    assert chain_two.parent is rack_device.chains
    assert chain_two.provider is context.provider
    assert list(rack_device.chains) == [chain_one, chain_two]
