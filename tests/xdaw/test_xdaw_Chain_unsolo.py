import time

from supriya.xdaw import Application, AudioEffect, RackDevice


def test_repeat(dc_index_synthdef_factory):
    """
    Unsoloing more than once is a no-op
    """
    application = Application(channel_count=2)
    context = application.add_context()
    track = context.add_track()
    rack = track.add_device(RackDevice)
    rack.add_chain(name="a")
    rack.add_chain(name="b")
    rack["a"].add_device(
        AudioEffect, synthdef=dc_index_synthdef_factory, synthdef_kwargs=dict(index=0)
    )
    rack["b"].add_device(
        AudioEffect, synthdef=dc_index_synthdef_factory, synthdef_kwargs=dict(index=1)
    )
    application.boot()
    rack["a"].solo()
    time.sleep(0.2)
    assert [int(_) for _ in context.master_track.rms_levels["input"]] == [1, 0]
    rack["a"].unsolo()
    time.sleep(0.2)
    assert [int(_) for _ in context.master_track.rms_levels["input"]] == [1, 1]
    with rack.provider.server.osc_io.capture() as transcript:
        rack["a"].unsolo()
    assert not len(transcript.sent_messages)


def test_exclusivity():
    application = Application()
    context = application.add_context()
    track = context.add_track()
    rack = track.add_device(RackDevice)
    chain_a = rack.add_chain(name="a")
    chain_b = rack.add_chain(name="b")
    chain_c = rack.add_chain(name="c")
    chain_d = rack.add_chain(name="d")
    chain_a.solo()
    chain_b.solo(exclusive=False)
    chain_c.solo(exclusive=False)
    assert [chain.is_active for chain in rack.chains] == [True, True, True, False]
    chain_a.unsolo(exclusive=True)
    assert [chain.is_active for chain in rack.chains] == [False, True, True, False]
    chain_d.solo(exclusive=False)
    assert [chain.is_active for chain in rack.chains] == [False, True, True, True]
    chain_b.unsolo()
    assert [chain.is_active for chain in rack.chains] == [True, True, True, True]
