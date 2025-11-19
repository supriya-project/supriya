from ..enums import CalculationRate
from ..ugens import (
    Compander,
    DelayN,
    In,
    Linen,
    Mix,
    Out,
    SynthDef,
    SynthDefBuilder,
    XOut,
    system,
)
from . import (
    BoolField,
    DeviceConfig,
    FloatField,
    ParameterConfig,
    SidechainConfig,
    SynthConfig,
)
from .constants import Names


def _build_compressor_sidechain_synthdef(
    channel_count: int,
    options: dict[str, float],
    sidechains: dict[str, tuple[int, bool]],
) -> SynthDef | None:
    print("???", channel_count, options, sidechains)
    sidechain_channel_count, sidechain_active = sidechains[Names.SIDECHAIN]
    if sidechain_active:
        return None
    with SynthDefBuilder(
        clamp_time=0.01,
        gate=1,
        in_=0,
        out=0,
    ) as builder:
        source = In.ar(
            bus=builder["in_"],
            channel_count=sidechain_channel_count,
        )
        if sidechain_channel_count == 1:
            source = Mix.new(source) / channel_count
        source = DelayN.ar(
            delay_time=builder["clamp_time"],
            maximum_delay_time=builder["clamp_time"],
            source=source,
        )
        gate = Linen.kr(
            attack_time=system.LAG_TIME,
            gate=builder["gate"],
            release_time=system.LAG_TIME,
        )
        Out.ar(
            bus=builder["out"],
            source=source * gate,
        )
    return builder.build(name=f"supriya:compressor:sidechain:{sidechain_channel_count}")


def _build_compressor_compressor_synthdef(
    channel_count: int,
    options: dict[str, float],
    sidechains: dict[str, tuple[int, bool]],
) -> SynthDef:
    sidechain_channel_count, _ = sidechains[Names.SIDECHAIN]
    with SynthDefBuilder(
        bus=0,
        clamp_time=0.01,
        gate=1,
        ratio=1 / 4,
        relax_time=0.1,
        sidechain=0,
        threshold=-6.0,
    ) as builder:
        source = In.ar(bus=builder["bus"], channel_count=channel_count)
        control = In.ar(bus=builder["sidechain"], channel_count=sidechain_channel_count)
        compressor = Compander.ar(
            source=source,
            control=control,
            threshold=builder["threshold"].amplitude_to_db(),
            clamp_time=builder["clamp_time"],
            relax_time=builder["relax_time"],
            slope_below=1.0,
            slope_above=builder["ratio"],
        )
        gate = Linen.kr(
            attack_time=system.LAG_TIME,
            gate=builder["gate"],
            release_time=system.LAG_TIME,
        )
        XOut.ar(
            crossfade=gate,
            source=compressor,
        )

    return builder.build(
        name=f"supriya:compressor:compressor:{channel_count}x{sidechain_channel_count}"
    )


COMPRESSOR_CONFIG = DeviceConfig(
    name="Compressor",
    parameter_configs={
        "clamp_time": FloatField(default=0.01, minimum=0.0, maximum=1.0),
        "ratio": FloatField(default=1 / 4, minimum=0.0, maximum=1.0),
        "relax_time": FloatField(default=0.1, minimum=0.0, maximum=10.0),
        "threshold": FloatField(default=-6.0),
        "mono_sidechain": ParameterConfig(
            field=BoolField(default=False), has_bus=False
        ),
    },
    sidechain_configs={
        Names.SIDECHAIN: SidechainConfig(
            channel_count=lambda channel_count, options: 1
            if options.get("mono_sidechain")
            else channel_count,
        ),
    },
    synth_configs=[
        SynthConfig(
            # should be able to pass sidechain info (channel_count, non-null) as a dict
            # and use that to control the presence of the synthdef
            controls={
                "clamp_time": (CalculationRate.CONTROL, "clamp_time"),
                "out": (CalculationRate.AUDIO, "sidechain"),
            },
            synthdef=_build_compressor_sidechain_synthdef,
        ),
        SynthConfig(
            controls={
                "clamp_time": (CalculationRate.CONTROL, "clamp_time"),
                "relax_time": (CalculationRate.CONTROL, "relax_time"),
                "ratio": (CalculationRate.CONTROL, "ratio"),
                "sidechain": (CalculationRate.AUDIO, "sidechain"),
                "threshold": (CalculationRate.CONTROL, "threshold"),
            },
            synthdef=_build_compressor_compressor_synthdef,
        ),
    ],
)
