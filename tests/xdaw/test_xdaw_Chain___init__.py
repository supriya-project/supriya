from uuid import UUID

from supriya.xdaw import Chain, Target


def test_1():
    chain = Chain()
    assert chain.application is None
    assert chain.channel_count is None
    assert chain.effective_channel_count == 2
    assert chain.context is None
    assert chain.graph_order == ()
    assert chain.is_active
    assert chain.name is None
    assert chain.parent is None
    assert chain.provider is None
    assert isinstance(chain.receive_target, Target)
    assert isinstance(chain.send_target, Target)
    assert isinstance(chain.uuid, UUID)
    assert len(chain.devices) == 0
    assert len(chain.postfader_sends) == 1
    assert len(chain.prefader_sends) == 0
    assert not chain.is_cued
    assert not chain.is_muted
    assert not chain.is_soloed
