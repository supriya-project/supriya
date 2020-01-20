from supriya.xdaw import Application, RackDevice


def test_1():
    """
    Remove one chain
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack_device = track.add_device(RackDevice)
    chain = rack_device.add_chain()
    rack_device.remove_chains(chain)
    assert list(rack_device.chains) == []
    assert chain.application is None
    assert chain.graph_order == ()
    assert chain.parent is None
    assert chain.provider is None


def test_2():
    """
    Remove two chains
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack_device = track.add_device(RackDevice)
    chain_one = rack_device.add_chain()
    chain_two = rack_device.add_chain()
    rack_device.remove_chains(chain_one, chain_two)
    assert list(rack_device.chains) == []
    assert chain_one.application is None
    assert chain_one.graph_order == ()
    assert chain_one.parent is None
    assert chain_one.provider is None
    assert chain_two.application is None
    assert chain_two.graph_order == ()
    assert chain_two.parent is None
    assert chain_two.provider is None


def test_3():
    """
    Remove first chain, leaving second untouched
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack_device = track.add_device(RackDevice)
    chain_one = rack_device.add_chain()
    chain_two = rack_device.add_chain()
    rack_device.remove_chains(chain_one)
    assert list(rack_device.chains) == [chain_two]
    assert chain_one.application is None
    assert chain_one.graph_order == ()
    assert chain_one.parent is None
    assert chain_one.provider is None
    assert chain_two.application is context.application
    assert chain_two.graph_order == (3, 0, 0, 0, 5, 0, 0, 0)
    assert chain_two.parent is rack_device.chains
    assert chain_two.provider is None


def test_4():
    """
    Boot, remove first chain, leaving second untouched
    """
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack_device = track.add_device(RackDevice)
    chain_one = rack_device.add_chain()
    chain_two = rack_device.add_chain()
    application.boot()
    rack_device.remove_chains(chain_one)
    assert context.provider is not None
    assert list(rack_device.chains) == [chain_two]
    assert chain_one.application is None
    assert chain_one.graph_order == ()
    assert chain_one.parent is None
    assert chain_one.provider is None
    assert chain_two.application is context.application
    assert chain_two.graph_order == (3, 0, 0, 0, 5, 0, 0, 0)
    assert chain_two.parent is rack_device.chains
    assert chain_two.provider is context.provider
