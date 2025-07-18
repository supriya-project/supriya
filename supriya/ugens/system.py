import bisect
import math
from functools import lru_cache
from typing import Literal

from ..enums import CalculationRate, DoneAction, EnvelopeShape, ParameterRate
from . import (
    DC,
    FFT,
    K2A,
    LPF,
    Amplitude,
    BufDur,
    BufRd,
    BufSamples,
    Envelope,
    EnvGen,
    In,
    InFeedback,
    LFSaw,
    Linen,
    LocalBuf,
    Mix,
    MulAdd,
    OffsetOut,
    Out,
    Pan2,
    PanAz,
    Parameter,
    PV_Div,
    PV_MagSmear,
    Rand,
    ReplaceOut,
    ScopeOut,
    ScopeOut2,
    SynthDef,
    SynthDefBuilder,
    UGenOperable,
    UGenVector,
    VarSaw,
    XLine,
)

LAG_TIME = 0.05


@lru_cache(maxsize=32)
def build_dc_tester_synthdef(channel_count: int) -> SynthDef:
    with SynthDefBuilder(
        out=Parameter(rate=ParameterRate.SCALAR, value=0),
        dc=[0] * channel_count,
    ) as builder:
        Out.ar(
            bus=builder["out"],
            source=DC.ar(source=builder["dc"]),
        )
    return builder.build(f"supriya:dc-tester:{channel_count}")


@lru_cache(maxsize=1)
def build_default_synthdef() -> SynthDef:
    with SynthDefBuilder(
        amplitude=0.1,
        frequency=440,
        gate=1,
        out=Parameter(rate=ParameterRate.SCALAR, value=0),
        pan=0.5,
    ) as builder:
        low_pass = LPF.ar(
            source=Mix.new(
                VarSaw.ar(
                    frequency=builder["frequency"]
                    + (
                        0,
                        Rand.ir(minimum=-0.4, maximum=0.0),
                        Rand.ir(minimum=0.0, maximum=0.4),
                    ),
                    width=0.3,
                )
            )
            * 0.3,
            frequency=XLine.kr(
                start=Rand.ir(minimum=4000, maximum=5000),
                stop=Rand.ir(minimum=2500, maximum=3200),
            ),
        )
        linen = Linen.kr(
            attack_time=0.01,
            done_action=DoneAction.FREE_SYNTH,
            gate=builder["gate"],
            release_time=0.3,
            sustain_level=0.7,
        )
        pan = Pan2.ar(
            source=low_pass * linen * builder["amplitude"], position=builder["pan"]
        )
        OffsetOut.ar(bus=builder["out"], source=pan)
    return builder.build(name="supriya:default")


@lru_cache(maxsize=32)
def build_link_audio_synthdef(channel_count: int) -> SynthDef:
    with SynthDefBuilder(
        out=0, in_=16, gate=1, fade_time=0.02, done_action=2
    ) as builder:
        start_value = builder["fade_time"] <= 0
        envelope = Envelope(
            amplitudes=[start_value, 1.0, 0.0],
            durations=[1.0, 1.0],
            curves=[EnvelopeShape.SINE],
            release_node=1,
        )
        envgen = EnvGen.kr(
            done_action=builder["done_action"],
            envelope=envelope,
            gate=builder["gate"],
            time_scale=builder["fade_time"],
        )
        source = InFeedback.ar(bus=builder["in_"], channel_count=channel_count)
        Out.ar(bus=builder["out"], source=source * envgen)
    return builder.build(name=f"supriya:link-ar:{channel_count}")


@lru_cache(maxsize=32)
def build_link_control_synthdef(channel_count: int) -> SynthDef:
    with SynthDefBuilder(
        out=0, in_=16, gate=1, fade_time=0.02, done_action=2
    ) as builder:
        start_value = builder["fade_time"] <= 0
        envelope = EnvGen.kr(
            done_action=builder["done_action"],
            envelope=Envelope(
                amplitudes=[start_value, 1.0, 0.0],
                durations=[1.0, 1.0],
                curves=[EnvelopeShape.LINEAR],
                release_node=1,
            ),
            gate=builder["gate"],
            time_scale=builder["fade_time"],
        )
        input_ = In.kr(bus=builder["in_"], channel_count=channel_count)
        Out.kr(bus=builder["out"], source=input_ * envelope)
    return builder.build(name=f"supriya:link-kr:{channel_count}")


@lru_cache(maxsize=32)
def build_amplitude_scope_synthdef(
    channel_count: int, rate: CalculationRate
) -> SynthDef:
    with SynthDefBuilder(
        in_=0,
        max_frames=4096,
        scope_frames=4096,
        scope_id=0,
    ) as builder:
        if rate is CalculationRate.AUDIO:
            source = In.ar(
                bus=builder["in_"],
                channel_count=channel_count,
            )
        elif rate is CalculationRate.CONTROL:
            source = K2A.ar(
                source=In.kr(
                    bus=builder["in_"],
                    channel_count=channel_count,
                ),
            )
        else:
            raise ValueError(rate)
        ScopeOut2.ar(
            max_frames=builder["max_frames"],
            scope_frames=builder["scope_frames"],
            scope_id=builder["scope_id"],
            source=source,
        )
    return builder.build(name=f"supriya:amp-scope-{rate.token}:{channel_count}")


@lru_cache(maxsize=32)
def build_frequency_scope_synthdef(
    channel_mode: Literal["mono", "stereo"] = "mono",
    frequency_mode: Literal["linear", "logarithmic"] = "linear",
    use_shared_memory: bool = True,
) -> SynthDef:
    with SynthDefBuilder(
        in_=0,
        fft_buffer_size=Parameter(value=2048, rate="SCALAR"),
        scope_id=Parameter(value=0, rate="SCALAR"),
        rate=Parameter(value=4, rate="SCALAR"),
    ) as builder:
        phase = 1 - (builder["rate"] * builder["fft_buffer_size"].reciprocal())

        fft_buffer_id = LocalBuf.ir(frame_count=builder["fft_buffer_size"])

        sample_count = BufSamples.ir(buffer_id=fft_buffer_id) * 0.5

        source = In.ar(channel_count=1, bus=builder["in_"])

        pv_chain = FFT.kr(
            buffer_id=fft_buffer_id,
            hop=0.75,
            source=source,
            window_type=1,
        )

        if frequency_mode == "stereo":
            source_2 = In.ar(
                bus=builder.add_parameter(name="in2", value=0),
                channel_count=1,
            )
            fft_buffer_id_2 = LocalBuf.ir(frame_count=builder["fft_buffer_size"])
            pv_chain_2 = FFT.kr(
                buffer_id=fft_buffer_id_2,
                hop=0.75,
                source=source_2,
                window_type=1,
            )
            pv_chain = PV_Div(pv_chain_a=pv_chain_2, pv_chain_b=pv_chain)

        pv_chain = PV_MagSmear.kr(bins=1, pv_chain=pv_chain)

        if frequency_mode == "linear":
            phasor = MulAdd.new(
                source=LFSaw.ar(
                    frequency=builder["rate"] / BufDur.ir(buffer_id=fft_buffer_id),
                    initial_phase=phase,
                ),
                multiplier=sample_count,
                addend=sample_count,
            )
        else:
            phasor = (
                sample_count
                ** (
                    MulAdd.new(
                        source=LFSaw.ar(
                            frequency=builder["rate"]
                            / BufDur.ir(buffer_id=fft_buffer_id),
                            initial_phase=phase,
                        ),
                        multiplier=0.5,
                        addend=0.5,
                    )
                )
            ) * 2
        phasor = phasor.round(2)

        scope_source = (
            BufRd.ar(
                buffer_id=fft_buffer_id,
                channel_count=1,
                interpolation=1,
                loop=1,
                phase=phasor,
            )
            / builder["fft_buffer_size"]
        ).amplitude_to_db()

        if not use_shared_memory:
            ScopeOut.ar(
                buffer_id=builder["scope_id"],
                source=scope_source,
            )
        else:
            ScopeOut2.ar(
                scope_id=builder["scope_id"],
                source=scope_source,
                max_frames=builder["fft_buffer_size"] / builder["rate"],
            )
    name = "supriya:freq-scope"
    name += "-lin" if frequency_mode == "linear" else "-log"
    name += "-shm" if use_shared_memory else ""
    name += ":2" if channel_mode == "stereo" else ":1"
    return builder.build(name=name)


@lru_cache(maxsize=32)
def build_channel_strip_synthdef(channel_count: int = 2) -> SynthDef:
    with SynthDefBuilder(
        active=1,
        out=0,
        done_action=DoneAction.FREE_SYNTH,
        gain=Parameter(value=0, lag=LAG_TIME),
        gate=1,
    ) as builder:
        source = In.ar(
            channel_count=channel_count,
            bus=builder["out"],
        )
        active_gate = Linen.kr(
            attack_time=LAG_TIME,
            gate=builder["active"],
            release_time=LAG_TIME,
        )
        free_gate = Linen.kr(
            attack_time=LAG_TIME,
            done_action=builder["done_action"],
            gate=builder["gate"],
            release_time=LAG_TIME,
        )
        source *= builder["gain"].db_to_amplitude()
        source *= active_gate
        source *= free_gate
        ReplaceOut.ar(bus=builder["out"], source=source)
    return builder.build(f"supriya:channel-strip:{channel_count}")


@lru_cache(maxsize=32)
def build_meters_synthdef(channel_count: int = 2) -> SynthDef:
    with SynthDefBuilder(in_=0, out=0) as builder:
        Out.kr(
            bus=builder["out"],
            source=Amplitude.kr(
                source=In.ar(bus=builder["in_"], channel_count=channel_count)
            ),
        )
    return builder.build(f"supriya:meters:{channel_count}")


@lru_cache(maxsize=32)
def build_patch_cable_synthdef(
    source_channel_count: int = 2,
    target_channel_count: int = 2,
    feedback: bool = False,
) -> SynthDef:
    # TODO: Implement up/down channel mixing
    builder = SynthDefBuilder(
        active=1,
        done_action=DoneAction.FREE_SYNTH,
        gain=0,
        gate=1,
        in_=0,
        out=0,
    )
    with builder:
        if feedback:
            source = InFeedback.ar(
                channel_count=source_channel_count,
                bus=builder["in_"],
            )
        else:
            source = In.ar(
                channel_count=source_channel_count,
                bus=builder["in_"],
            )
        active_gate = Linen.kr(
            attack_time=LAG_TIME,
            gate=builder["active"],
            release_time=LAG_TIME,
        )
        free_gate = Linen.kr(
            attack_time=LAG_TIME,
            done_action=builder["done_action"],
            gate=builder["gate"],
            release_time=LAG_TIME,
        )
        gain = builder["gain"].db_to_amplitude() * free_gate * active_gate
        # gain stage with the smallest number of binops
        if source_channel_count < target_channel_count:
            source *= gain
        # TODO: up/down mixing goes here
        mix_factor = source_channel_count / target_channel_count

        # equal channel counts
        if source_channel_count == target_channel_count:
            pass
        # mix down to mono
        elif target_channel_count == 1:
            source = Mix.new(source) / mix_factor
        # mix up from mono
        elif source_channel_count == 1:
            source = UGenVector(*([source] * target_channel_count))
        # different channel counts
        else:
            # duplicate channels until source is equal or larger than the target
            if not isinstance(source, UGenVector):
                source = UGenVector(*source)
            while (len(source) / target_channel_count) < 1:
                source = UGenVector(*(x for x in source for _ in range(2)))
            source_positions = [2 / len(source) * i for i in range(len(source))]
            target_positions = [
                2 / target_channel_count * i for i in range(target_channel_count)
            ]
            print(f"{source_positions=}")
            print(f"{target_positions=}")
            # Manually calculate expected maximum target amplitudes
            target_amplitudes = [0.0] * target_channel_count
            for source_position in source_positions:
                print(f"{source_position=}")
                index = bisect.bisect(target_positions, source_position)
                if index == target_channel_count:
                    index_one, index_two = index - 1, 0
                else:
                    index_one, index_two = index - 1, index
                if source_position == target_positions[index_one]:
                    target_amplitudes[index_one] += 1.0
                else:
                    target_position_one = target_positions[index_one]
                    if index_two:
                        target_position_two = target_positions[index_two]
                    else:
                        target_position_two = 2.0
                    distance_to_one = abs(
                        (source_position - target_position_one)
                        / (target_position_one - target_position_two)
                    )
                    distance_to_two = abs(
                        (source_position - target_position_two)
                        / (target_position_one - target_position_two)
                    )
                    target_amplitudes[index_one] += (
                        amplitude_one := math.sin(math.pi * distance_to_one / 2)
                    )
                    target_amplitudes[index_two] += (
                        amplitude_two := math.sin(math.pi * distance_to_two / 2)
                    )
                    print(f"    {target_position_one=}")
                    print(f"    {target_position_two=}")
                    print(f"    {distance_to_one=}")
                    print(f"    {distance_to_two=}")
                    print(f"    {amplitude_one=}")
                    print(f"    {amplitude_two=}")
            print(f"{target_amplitudes=}")
            amplitude = 1 / max(target_amplitudes)  # Use calculation to determine level
            width = 1.999
            panners: list[UGenOperable] = []
            for position, channel in zip(source_positions, source):
                panner = PanAz.ar(
                    channel_count=target_channel_count,
                    source=channel,
                    position=position,
                    amplitude=amplitude,
                    width=width,
                    orientation=0,
                )
                panners.extend(panner)
            source = Mix.multichannel(panners, target_channel_count)
        # gain stage with the smallest number of binops
        if target_channel_count <= source_channel_count:
            source *= gain
        Out.ar(bus=builder["out"], source=source)

    name = (
        f"supriya:{'fb-' if feedback else ''}"
        f"patch-cable:{source_channel_count}x{target_channel_count}"
    )
    return builder.build(name)


# default synthdef
default = build_default_synthdef()

# audio-rate link synthdefs
system_link_audio_1 = build_link_audio_synthdef(1)
system_link_audio_2 = build_link_audio_synthdef(2)
system_link_audio_3 = build_link_audio_synthdef(3)
system_link_audio_4 = build_link_audio_synthdef(4)
system_link_audio_5 = build_link_audio_synthdef(5)
system_link_audio_6 = build_link_audio_synthdef(6)
system_link_audio_7 = build_link_audio_synthdef(7)
system_link_audio_8 = build_link_audio_synthdef(8)
system_link_audio_9 = build_link_audio_synthdef(9)
system_link_audio_10 = build_link_audio_synthdef(10)
system_link_audio_11 = build_link_audio_synthdef(11)
system_link_audio_12 = build_link_audio_synthdef(12)
system_link_audio_13 = build_link_audio_synthdef(13)
system_link_audio_14 = build_link_audio_synthdef(14)
system_link_audio_15 = build_link_audio_synthdef(15)
system_link_audio_16 = build_link_audio_synthdef(16)

# control-rate link synthdefs
system_link_control_1 = build_link_control_synthdef(1)
system_link_control_2 = build_link_control_synthdef(2)
system_link_control_3 = build_link_control_synthdef(3)
system_link_control_4 = build_link_control_synthdef(4)
system_link_control_5 = build_link_control_synthdef(5)
system_link_control_6 = build_link_control_synthdef(6)
system_link_control_7 = build_link_control_synthdef(7)
system_link_control_8 = build_link_control_synthdef(8)
system_link_control_9 = build_link_control_synthdef(9)
system_link_control_10 = build_link_control_synthdef(10)
system_link_control_11 = build_link_control_synthdef(11)
system_link_control_12 = build_link_control_synthdef(12)
system_link_control_13 = build_link_control_synthdef(13)
system_link_control_14 = build_link_control_synthdef(14)
system_link_control_15 = build_link_control_synthdef(15)
system_link_control_16 = build_link_control_synthdef(16)

# audio-rate stethoscope synthdefs
amplitude_scope_audio_1 = build_amplitude_scope_synthdef(1, CalculationRate.AUDIO)
amplitude_scope_audio_2 = build_amplitude_scope_synthdef(2, CalculationRate.AUDIO)
amplitude_scope_audio_3 = build_amplitude_scope_synthdef(3, CalculationRate.AUDIO)
amplitude_scope_audio_4 = build_amplitude_scope_synthdef(4, CalculationRate.AUDIO)
amplitude_scope_audio_5 = build_amplitude_scope_synthdef(5, CalculationRate.AUDIO)
amplitude_scope_audio_6 = build_amplitude_scope_synthdef(6, CalculationRate.AUDIO)
amplitude_scope_audio_7 = build_amplitude_scope_synthdef(7, CalculationRate.AUDIO)
amplitude_scope_audio_8 = build_amplitude_scope_synthdef(8, CalculationRate.AUDIO)
amplitude_scope_audio_9 = build_amplitude_scope_synthdef(9, CalculationRate.AUDIO)
amplitude_scope_audio_10 = build_amplitude_scope_synthdef(10, CalculationRate.AUDIO)
amplitude_scope_audio_11 = build_amplitude_scope_synthdef(11, CalculationRate.AUDIO)
amplitude_scope_audio_12 = build_amplitude_scope_synthdef(12, CalculationRate.AUDIO)
amplitude_scope_audio_13 = build_amplitude_scope_synthdef(13, CalculationRate.AUDIO)
amplitude_scope_audio_14 = build_amplitude_scope_synthdef(14, CalculationRate.AUDIO)
amplitude_scope_audio_15 = build_amplitude_scope_synthdef(15, CalculationRate.AUDIO)
amplitude_scope_audio_15 = build_amplitude_scope_synthdef(16, CalculationRate.AUDIO)

# control-rate amplitude_scope synthdefs
amplitude_scope_control_1 = build_amplitude_scope_synthdef(1, CalculationRate.CONTROL)
amplitude_scope_control_2 = build_amplitude_scope_synthdef(2, CalculationRate.CONTROL)
amplitude_scope_control_3 = build_amplitude_scope_synthdef(3, CalculationRate.CONTROL)
amplitude_scope_control_4 = build_amplitude_scope_synthdef(4, CalculationRate.CONTROL)
amplitude_scope_control_5 = build_amplitude_scope_synthdef(5, CalculationRate.CONTROL)
amplitude_scope_control_6 = build_amplitude_scope_synthdef(6, CalculationRate.CONTROL)
amplitude_scope_control_7 = build_amplitude_scope_synthdef(7, CalculationRate.CONTROL)
amplitude_scope_control_8 = build_amplitude_scope_synthdef(8, CalculationRate.CONTROL)
amplitude_scope_control_9 = build_amplitude_scope_synthdef(9, CalculationRate.CONTROL)
amplitude_scope_control_10 = build_amplitude_scope_synthdef(10, CalculationRate.CONTROL)
amplitude_scope_control_11 = build_amplitude_scope_synthdef(11, CalculationRate.CONTROL)
amplitude_scope_control_12 = build_amplitude_scope_synthdef(12, CalculationRate.CONTROL)
amplitude_scope_control_13 = build_amplitude_scope_synthdef(13, CalculationRate.CONTROL)
amplitude_scope_control_14 = build_amplitude_scope_synthdef(14, CalculationRate.CONTROL)
amplitude_scope_control_15 = build_amplitude_scope_synthdef(15, CalculationRate.CONTROL)
amplitude_scope_control_15 = build_amplitude_scope_synthdef(16, CalculationRate.CONTROL)

# frequency scope synthdefs
frequency_scope_lin_1 = build_frequency_scope_synthdef(
    channel_mode="mono", frequency_mode="linear", use_shared_memory=False
)
frequency_scope_lin_2 = build_frequency_scope_synthdef(
    channel_mode="stereo", frequency_mode="linear", use_shared_memory=False
)
frequency_scope_lin_shm_1 = build_frequency_scope_synthdef(
    channel_mode="mono", frequency_mode="linear", use_shared_memory=True
)
frequency_scope_lin_shm_2 = build_frequency_scope_synthdef(
    channel_mode="stereo", frequency_mode="linear", use_shared_memory=True
)
frequency_scope_log_1 = build_frequency_scope_synthdef(
    channel_mode="mono", frequency_mode="logarithmic", use_shared_memory=False
)
frequency_scope_log_2 = build_frequency_scope_synthdef(
    channel_mode="stereo", frequency_mode="logarithmic", use_shared_memory=False
)
frequency_scope_log_shm_1 = build_frequency_scope_synthdef(
    channel_mode="mono", frequency_mode="logarithmic", use_shared_memory=True
)
frequency_scope_log_shm_2 = build_frequency_scope_synthdef(
    channel_mode="stereo", frequency_mode="logarithmic", use_shared_memory=True
)

AMPLITUDE_SCOPE_SYNTHDEFS: dict[str, SynthDef] = {
    synthdef.effective_name: synthdef
    for synthdef in [
        amplitude_scope_audio_1,
        amplitude_scope_audio_2,
        amplitude_scope_audio_3,
        amplitude_scope_audio_4,
        amplitude_scope_audio_5,
        amplitude_scope_audio_6,
        amplitude_scope_audio_7,
        amplitude_scope_audio_8,
        amplitude_scope_audio_9,
        amplitude_scope_audio_10,
        amplitude_scope_audio_11,
        amplitude_scope_audio_12,
        amplitude_scope_audio_13,
        amplitude_scope_audio_14,
        amplitude_scope_audio_15,
        amplitude_scope_audio_15,
        amplitude_scope_control_1,
        amplitude_scope_control_2,
        amplitude_scope_control_3,
        amplitude_scope_control_4,
        amplitude_scope_control_5,
        amplitude_scope_control_6,
        amplitude_scope_control_7,
        amplitude_scope_control_8,
        amplitude_scope_control_9,
        amplitude_scope_control_10,
        amplitude_scope_control_11,
        amplitude_scope_control_12,
        amplitude_scope_control_13,
        amplitude_scope_control_14,
        amplitude_scope_control_15,
        amplitude_scope_control_15,
    ]
}

FREQUENCY_SCOPE_SYNTHDEFS: dict[str, SynthDef] = {
    synthdef.effective_name: synthdef
    for synthdef in [
        frequency_scope_lin_1,
        frequency_scope_lin_2,
        frequency_scope_log_1,
        frequency_scope_log_2,
        frequency_scope_lin_shm_1,
        frequency_scope_lin_shm_2,
        frequency_scope_log_shm_1,
        frequency_scope_log_shm_2,
    ]
}

SYSTEM_SYNTHDEFS: dict[str, SynthDef] = {
    synthdef.effective_name: synthdef
    for synthdef in [
        system_link_audio_1,
        system_link_audio_2,
        system_link_audio_3,
        system_link_audio_4,
        system_link_audio_5,
        system_link_audio_6,
        system_link_audio_7,
        system_link_audio_8,
        system_link_audio_9,
        system_link_audio_10,
        system_link_audio_11,
        system_link_audio_12,
        system_link_audio_13,
        system_link_audio_14,
        system_link_audio_15,
        system_link_audio_16,
        system_link_control_1,
        system_link_control_2,
        system_link_control_3,
        system_link_control_4,
        system_link_control_5,
        system_link_control_6,
        system_link_control_7,
        system_link_control_8,
        system_link_control_9,
        system_link_control_10,
        system_link_control_11,
        system_link_control_12,
        system_link_control_13,
        system_link_control_14,
        system_link_control_15,
        system_link_control_16,
    ]
}

__all__ = [
    "AMPLITUDE_SCOPE_SYNTHDEFS",
    "FREQUENCY_SCOPE_SYNTHDEFS",
    "SYSTEM_SYNTHDEFS",
    "build_amplitude_scope_synthdef",
    "build_channel_strip_synthdef",
    "build_dc_tester_synthdef",
    "build_default_synthdef",
    "build_frequency_scope_synthdef",
    "build_link_audio_synthdef",
    "build_link_control_synthdef",
    "default",
]
