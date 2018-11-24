import pytest
import supriya.live
import supriya.realtime
import supriya.synthdefs
import supriya.ugens
import time


with supriya.synthdefs.SynthDefBuilder(out=0, value=1) as builder:
    source = supriya.ugens.DC.ar(source=builder['value'])
    supriya.ugens.Out.ar(bus=builder['out'], source=source)
dc_synthdef = builder.build('dc')


@pytest.fixture(scope='function')
def mixer(server):
    mixer = supriya.live.Mixer(channel_count=1, cue_channel_count=1)
    mixer.add_track('foo')
    mixer.add_track('bar')
    mixer.add_track('baz')
    mixer.allocate()
    synth_a = supriya.realtime.Synth(synthdef=dc_synthdef, value=1.0)
    synth_b = supriya.realtime.Synth(synthdef=dc_synthdef, value=0.5)
    synth_c = supriya.realtime.Synth(synthdef=dc_synthdef, value=0.25)
    synth_a.allocate(target_node=mixer['foo'], out=int(mixer['foo'].output_bus_group))
    synth_b.allocate(target_node=mixer['bar'], out=int(mixer['bar'].output_bus_group))
    synth_c.allocate(target_node=mixer['baz'], out=int(mixer['baz'].output_bus_group))
    time.sleep(0.25)
    return mixer


def test_01(mixer):
    """
    Tracks are initially uncued.
    """
    assert not mixer['foo'].is_cued
    assert not mixer['bar'].is_cued
    assert not mixer['baz'].is_cued
    assert not mixer['foo'].cue_synth['active']
    assert not mixer['bar'].cue_synth['active']
    assert not mixer['baz'].cue_synth['active']
    time.sleep(0.1)
    levels = mixer['cue'].input_levels
    assert round(levels['rms'][0], 2) == 0.0


def test_02(mixer):
    """
    Tracks can be cued.
    """
    mixer['bar'].set_cue(True)
    time.sleep(0.25)
    assert not mixer['foo'].is_cued
    assert mixer['bar'].is_cued
    assert not mixer['baz'].is_cued
    assert not mixer['foo'].cue_synth['active']
    assert mixer['bar'].cue_synth['active']
    assert not mixer['baz'].cue_synth['active']
    levels = mixer['cue'].input_levels
    assert round(levels['rms'][0], 2) == 0.5


def test_03(mixer):
    """
    Cued tracks can be uncued.
    """
    mixer['bar'].set_cue(True)
    mixer['bar'].set_cue(False)
    time.sleep(0.25)
    assert not mixer['foo'].is_cued
    assert not mixer['bar'].is_cued
    assert not mixer['baz'].is_cued
    assert not mixer['foo'].cue_synth['active']
    assert not mixer['bar'].cue_synth['active']
    assert not mixer['baz'].cue_synth['active']
    levels = mixer['cue'].input_levels
    assert round(levels['rms'][0], 2) == 0.0


def test_04(mixer):
    """
    Mutually-exclusive, by default.
    """
    mixer['bar'].set_cue(True)
    mixer['baz'].set_cue(True)
    time.sleep(0.25)
    assert not mixer['foo'].is_cued
    assert not mixer['bar'].is_cued
    assert mixer['baz'].is_cued
    assert not mixer['foo'].cue_synth['active']
    assert not mixer['bar'].cue_synth['active']
    assert mixer['baz'].cue_synth['active']
    levels = mixer['cue'].input_levels
    assert round(levels['rms'][0], 2) == 0.25


def test_05(mixer):
    """
    Not mutually-exclusive, when Mixer.is_allowing_multiple.
    """
    mixer['bar'].set_cue(True)
    mixer.allow_multiple(True)
    mixer['baz'].set_cue(True)
    time.sleep(0.25)
    assert not mixer['foo'].is_cued
    assert mixer['bar'].is_cued
    assert mixer['baz'].is_cued
    assert not mixer['foo'].cue_synth['active']
    assert mixer['bar'].cue_synth['active']
    assert mixer['baz'].cue_synth['active']
    levels = mixer['cue'].input_levels
    assert round(levels['rms'][0], 2) == 0.75


def test_06(mixer):
    """
    Mutually-exclusive again, when not Mixer.is_allowing_multiple.
    """
    mixer['bar'].set_cue(True)
    mixer.allow_multiple(True)
    mixer['baz'].set_cue(True)
    mixer.allow_multiple(False)
    mixer['foo'].set_cue(True)
    time.sleep(0.25)
    assert mixer['foo'].is_cued
    assert not mixer['bar'].is_cued
    assert not mixer['baz'].is_cued
    assert mixer['foo'].cue_synth['active']
    assert not mixer['bar'].cue_synth['active']
    assert not mixer['baz'].cue_synth['active']
    levels = mixer['cue'].input_levels
    assert round(levels['rms'][0], 2) == 1.0
