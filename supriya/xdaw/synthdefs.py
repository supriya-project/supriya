import bisect
import math

from supriya.enums import CalculationRate, DoneAction
from supriya.synthdefs.SynthDefFactory import SynthDefFactory
from supriya.synthdefs.UGenArray import UGenArray
from supriya.ugens import (
    In,
    InFeedback,
    Linen,
    Mix,
    Out,
    PanAz,
    ReplaceOut,
    Sanitize,
    SendPeakRMS,
    XOut,
)


def gain_block(builder, source, state):
    amplitude = (builder["gain"].db_to_amplitude() * (builder["gain"] > -96.0)).lag(
        builder["lag"]
    )
    return source * amplitude


def gate_block(builder, source, state):
    active = Linen.kr(
        attack_time=builder["lag"],
        done_action=DoneAction.NOTHING,
        gate=builder["active"],
        release_time=builder["lag"],
    )
    gate = Linen.kr(
        attack_time=builder["lag"],
        done_action=DoneAction.FREE_SYNTH,
        gate=builder["gate"],
        release_time=builder["lag"],
    )
    return source * gate * active


def hard_gate_block(builder, source, state):
    active = Linen.kr(
        attack_time=builder["lag"],
        done_action=DoneAction.NOTHING,
        gate=builder["active"],
        release_time=builder["lag"],
    )
    gate = Linen.kr(
        attack_time=builder["lag"],
        done_action=DoneAction.FREE_SYNTH,
        gate=builder["gate"],
        release_time=builder["lag"],
    )
    hard_gate = Linen.kr(
        attack_time=builder["lag"],
        done_action=DoneAction.FREE_SYNTH_AND_ENCLOSING_GROUP,
        gate=builder["hard_gate"],
        release_time=builder["lag"],
    )
    return source * gate * hard_gate * active


def in_block(builder, source, state):
    rate = state.get("calculation_rate", CalculationRate.AUDIO)
    if rate == CalculationRate.CONTROL:
        ugen = In
    else:
        ugen = InFeedback if state["feedback"] else In
    source = ugen._get_method_for_rate(ugen, rate)(
        bus=builder["in_"], channel_count=state["source_channel_count"]
    )
    source = Sanitize._get_method_for_rate(Sanitize, rate)(source=source)
    return source


def mix_block(builder, source, state):
    source_channel_count = state["source_channel_count"]
    target_channel_count = state["target_channel_count"]
    mix_factor = source_channel_count / target_channel_count
    if source_channel_count == target_channel_count:
        pass
    elif target_channel_count == 1:
        source = Mix.new(source) / mix_factor
    elif source_channel_count == 1:
        source = UGenArray([source] * target_channel_count)
    else:
        source = list(source)
        # Duplicate channels until source is equal or larger than the target
        while (source_channel_count / target_channel_count) < 1:
            source = [x for x in source for _ in range(2)]
            source_channel_count *= 2
        source_positions = [
            2 / source_channel_count * i for i in range(source_channel_count)
        ]
        target_positions = [
            2 / target_channel_count * i for i in range(target_channel_count)
        ]
        # Manually calculate expected maximum target amplitudes
        target_amplitudes = [0.0] * target_channel_count
        for source_position in source_positions:
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
                target_amplitudes[index_one] += math.sin(math.pi * distance_to_one / 2)
                target_amplitudes[index_two] += math.sin(math.pi * distance_to_two / 2)
        amplitude = 1 / max(target_amplitudes)  # Use calculation to determine level
        width = 1.999  # Prevent denorm bleeding into adjacent speakers
        panners = []
        for position, channel in zip(source_positions, source):
            panner = PanAz._get_method_for_rate(PanAz, state["calculation_rate"])(
                channel_count=target_channel_count,
                source=channel,
                position=position,
                amplitude=amplitude,
                width=width,
                orientation=0,
            )
            panners.extend(panner)
        source = Mix.multichannel(panners, target_channel_count)
    return source


def out_block(builder, source, state):
    rate = state.get("calculation_rate", CalculationRate.AUDIO)
    kwargs = dict(bus=builder["out"], source=source)
    if state["replace_out"]:
        ugen = ReplaceOut
    elif state["mix_out"]:
        ugen = XOut
        kwargs["crossfade"] = builder["mix"]
    else:
        ugen = Out
    return ugen._get_method_for_rate(ugen, rate)(**kwargs)


def sanitize_block(builder, source, state):
    return Sanitize.ar(source=source)


def build_patch_synthdef(
    source_channel_count,
    target_channel_count,
    *,
    calculation_rate=CalculationRate.AUDIO,
    feedback=False,
    gain=False,
    hard_gate=False,
    mix_out=False,
    replace_out=False,
):
    if mix_out and replace_out:
        raise ValueError
    initial_state = dict(
        calculation_rate=CalculationRate.from_expr(calculation_rate),
        feedback=feedback,
        mix_out=mix_out,
        replace_out=replace_out,
        source_channel_count=source_channel_count,
        target_channel_count=target_channel_count,
    )
    kwargs = dict(active=1, gate=1, in_=0, lag=0.01, out=0)
    if gain:
        kwargs["gain"] = 0
    if hard_gate:
        kwargs["hard_gate"] = 1
    if mix_out:
        kwargs["mix"] = 1
    local_gate_block = gate_block
    if hard_gate:
        local_gate_block = hard_gate_block
    factory = SynthDefFactory(**kwargs).with_initial_state(**initial_state)
    factory = factory.with_signal_block(in_block)
    if source_channel_count <= target_channel_count:
        if gain:
            factory = factory.with_signal_block(gain_block)
        factory = factory.with_signal_block(local_gate_block)
    factory = factory.with_signal_block(mix_block)
    if source_channel_count > target_channel_count:
        if gain:
            factory = factory.with_signal_block(gain_block)
        factory = factory.with_signal_block(local_gate_block)
    factory = factory.with_signal_block(out_block)
    flavor_parts = []
    if feedback:
        flavor_parts.append("fb")
    if gain:
        flavor_parts.append("gain")
    if hard_gate:
        flavor_parts.append("hard")
    if mix_out:
        flavor_parts.append("mix")
    if replace_out:
        flavor_parts.append("replace")
    flavor = "[" + ",".join(flavor_parts) + "]" if flavor_parts else ""
    name = f"mixer/patch{flavor}/{source_channel_count}x{target_channel_count}"
    return factory.build(name=name)


def build_peak_rms_synthdef(channel_count):
    """
    Build Peak/RMS SynthDef.

    ::

        >>> from supriya.xdaw import synthdefs
        >>> synthdef = synthdefs.build_peak_rms_synthdef(channel_count=2)
        >>> print(synthdef)
        synthdef:
            name: mixer/levels/2
            ugens:
            -   Control.ir: null
            -   In.ar:
                    bus: Control.ir[0:out]
            -   SendPeakRMS.ar:
                    peak_lag: 3.0
                    reply_id: 115.0
                    reply_rate: 20.0
            -   Control.kr: null
            -   Linen.kr:
                    attack_time: Control.kr[1:lag]
                    done_action: 2.0
                    gate: Control.kr[0:gate]
                    release_time: Control.kr[1:lag]
                    sustain_level: 1.0

    """

    def gate_block(builder, source, state):
        Linen.kr(
            attack_time=builder["lag"],
            done_action=DoneAction.FREE_SYNTH,
            gate=builder["gate"],
            release_time=builder["lag"],
        )
        return source

    def peak_rms_block(builder, source, state):
        SendPeakRMS.ar(command_name="/levels", source=source)
        return source

    factory = (
        SynthDefFactory(gate=1, lag=0.01)
        .with_channel_count(channel_count)
        .with_input()
        .with_signal_block(gate_block)
        .with_signal_block(peak_rms_block)
    )
    return factory.build(f"mixer/levels/{channel_count}")
