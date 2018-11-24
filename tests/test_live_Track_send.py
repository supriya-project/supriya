import time

import pytest

import supriya.live
import supriya.realtime
import supriya.synthdefs
import supriya.ugens

with supriya.synthdefs.SynthDefBuilder(out=0, value=1) as builder:
    source = supriya.ugens.DC.ar(source=builder["value"])
    supriya.ugens.Out.ar(bus=builder["out"], source=source)
dc_synthdef = builder.build("dc")


@pytest.fixture(scope="function")
def mixer(server):
    mixer = supriya.live.Mixer(channel_count=1, cue_channel_count=1)
    mixer.add_track("foo")
    mixer.add_track("bar")
    mixer.add_track("baz")
    mixer.allocate()
    synth_a = supriya.realtime.Synth(synthdef=dc_synthdef, value=1.0)
    synth_b = supriya.realtime.Synth(synthdef=dc_synthdef, value=0.5)
    synth_c = supriya.realtime.Synth(synthdef=dc_synthdef, value=0.25)
    synth_a.allocate(target_node=mixer["foo"], out=int(mixer["foo"].output_bus_group))
    synth_b.allocate(target_node=mixer["bar"], out=int(mixer["bar"].output_bus_group))
    synth_c.allocate(target_node=mixer["baz"], out=int(mixer["baz"].output_bus_group))
    mixer["foo"].set_gain(0)
    mixer["bar"].set_gain(0)
    mixer["baz"].set_gain(0)
    mixer["foo"].send["master"] = -96
    mixer["bar"].send["master"] = -96
    mixer["baz"].send["master"] = 0
    time.sleep(0.25)
    return mixer


def test_01(mixer):
    levels = mixer["master"].input_levels
    assert round(levels["rms"][0], 2) == 0.25
    # chain bar into baz
    mixer["bar"].send["baz"] = 0
    time.sleep(0.25)
    levels = mixer["master"].input_levels
    assert round(levels["rms"][0], 2) == 0.75
    # chain foo into bar
    mixer["foo"].send["bar"] = 0
    time.sleep(0.25)
    levels = mixer["master"].input_levels
    assert round(levels["rms"][0], 2) == 1.75
    # mute bar
    mixer["bar"].set_mute(True)
    time.sleep(0.25)
    levels = mixer["master"].input_levels
    assert round(levels["rms"][0], 2) == 0.25
