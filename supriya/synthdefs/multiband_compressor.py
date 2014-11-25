# -*- encoding: utf-8 -*-
from supriya import *


def _make_synthdef():
    with SynthDefBuilder(
        frequency_1=100,
        frequency_2=1000,
        frequency_3=3000,
        band_1_gain=1,
        band_2_gain=1,
        band_3_gain=1,
        band_4_gain=1,
        band_1_clamp_time=0.01,
        band_2_clamp_time=0.01,
        band_3_clamp_time=0.01,
        band_4_clamp_time=0.01,
        band_1_relax_time=0.1,
        band_2_relax_time=0.1,
        band_3_relax_time=0.1,
        band_4_relax_time=0.1,
        band_1_slope=0.5,
        band_2_slope=0.5,
        band_3_slope=0.5,
        band_4_slope=0.5,
        band_1_threshold=0.9,
        band_2_threshold=0.9,
        band_3_threshold=0.9,
        band_4_threshold=0.9,
        ) as builder:
        source = ugentools.In.ar(bus=0, channel_count=2)
        band_1 = ugentools.LPF.ar(
            frequency=builder['frequency_1'],
            source=source,
            )
        band_4 = ugentools.HPF.ar(
            frequency=builder['frequency_3'],
            source=source,
            )
        center = source - band_1 - band_4
        band_2 = ugentools.LPF.ar(
            frequency=builder['frequency_2'],
            source=center,
            )
        band_3 = ugentools.HPF.ar(
            frequency=builder['frequency_2'],
            source=center,
            )
        band_1 = ugentools.CompanderD.ar(
            clamp_time=builder['band_1_clamp_time'],
            relax_time=builder['band_1_relax_time'],
            slope_above=builder['band_1_slope'],
            source=band_1,
            threshold=builder['band_1_threshold'],
            )
        band_2 = ugentools.CompanderD.ar(
            clamp_time=builder['band_2_clamp_time'],
            relax_time=builder['band_2_relax_time'],
            slope_above=builder['band_2_slope'],
            source=band_2,
            threshold=builder['band_2_threshold'],
            )
        band_3 = ugentools.CompanderD.ar(
            clamp_time=builder['band_3_clamp_time'],
            relax_time=builder['band_3_relax_time'],
            slope_above=builder['band_3_slope'],
            source=band_3,
            threshold=builder['band_3_threshold'],
            )
        band_4 = ugentools.CompanderD.ar(
            clamp_time=builder['band_4_clamp_time'],
            relax_time=builder['band_4_relax_time'],
            slope_above=builder['band_4_slope'],
            source=band_4,
            threshold=builder['band_4_threshold'],
            )
        band_1 *= builder['band_1_gain']
        band_2 *= builder['band_2_gain']
        band_3 *= builder['band_3_gain']
        band_4 *= builder['band_4_gain']
        source = ugentools.Sum4.new(
            input_one=band_1,
            input_two=band_2,
            input_three=band_3,
            input_four=band_4,
            )
        ugentools.ReplaceOut.ar(bus=0, source=source)
    return builder.build()


multiband_compressor = _make_synthdef()

__all__ = (
    'multiband_compressor',
    )