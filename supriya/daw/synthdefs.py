from supriya import DoneAction
from supriya.synthdefs.Parameter import Parameter
from supriya.synthdefs.SynthDefBuilder import SynthDefBuilder
from supriya.synthdefs.SynthDefFactory import SynthDefFactory
from supriya.synthdefs.UGenArray import UGenArray
from supriya.ugens import (
    DC,
    HPZ1,
    In,
    Linen,
    Mix,
    Out,
    PanAz,
    SendPeakRMS,
    SendTrig,
)

factory = SynthDefFactory(active=1, gate=1, lag=0.1).with_output().with_input()


def _peak_rms_block_builder(command_name):
    def _peak_rms_block(builder, source, state):
        SendPeakRMS.ar(command_name=command_name, source=source)
        return source

    return _peak_rms_block


def _gate_block(builder, source, state):
    gate = Linen.kr(
        attack_time=builder["lag"],
        done_action=DoneAction.FREE_SYNTH,
        gate=builder["gate"],
        release_time=builder["lag"],
    )
    active = Linen.kr(
        attack_time=builder["lag"],
        done_action=DoneAction.NOTHING,
        gate=builder["active"],
        release_time=builder["lag"],
    )
    is_active = active > 0
    trigger = abs(HPZ1.kr(source=is_active))
    SendTrig.kr(trigger=trigger, id_=0, value=is_active)
    return source * gate * active


def _gain_block(builder, source, state):
    amplitude = (builder["gain"].db_to_amplitude() * (builder["gain"] > -96.0)).lag(
        builder["lag"]
    )
    return source * amplitude


def with_gate(synthdef_builder):
    return Linen.kr(
        attack_time=synthdef_builder["lag"],
        done_action=DoneAction.FREE_SYNTH,
        gate=synthdef_builder["gate"],
        release_time=synthdef_builder["lag"],
    )


def with_active(synthdef_builder):
    return Linen.kr(
        attack_time=synthdef_builder["lag"],
        done_action=DoneAction.NOTHING,
        gate=synthdef_builder["active"],
        release_time=synthdef_builder["lag"],
    )


def with_gain(synthdef_builder):
    gate = with_gate(synthdef_builder)
    active = with_active(synthdef_builder)
    amplitude = (
        synthdef_builder["gain"].db_to_amplitude() * (synthdef_builder["gain"] > -96.0)
    ).lag(synthdef_builder["lag"])
    return gate * active * amplitude


def build_direct_synthdef(source_track_count, target_track_count, mapping):
    for in_, out in mapping:
        assert 0 <= in_ < source_track_count
        assert 0 <= out < target_track_count
    synthdef_builder = SynthDefBuilder(
        gate=1,
        lag=0.1,
        in_=Parameter(value=0, parameter_rate="scalar"),
        out=Parameter(value=0, parameter_rate="scalar"),
    )
    with synthdef_builder:
        source = In.ar(bus=synthdef_builder["in_"], channel_count=source_track_count)
        gate = with_gate(synthdef_builder)
        source *= gate
        zero = DC.ar(0)
        mapped = []
        for _ in range(target_track_count):
            mapped.append([])
        for in_, out in mapping:
            mapped[out].append(source[in_])
        for i, out in enumerate(mapped):
            if not out:
                out.append(zero)
            mapped[i] = Mix.new(out)
        Out.ar(bus=synthdef_builder["out"], source=mapped)
    name = "mixer/direct/{}".format(
        ",".join("{}:{}".format(in_, out) for in_, out in mapping)
    )
    return synthdef_builder.build(name=name)


def build_chain_input_synthdef(channel_count):
    """
    Build chain input synthdef.

    ::

        >>> from supriya.daw import synthdefs
        >>> synthdef = synthdefs.build_chain_input_synthdef(channel_count=1)
        >>> print(synthdef)
        synthdef:
            name: mixer/chain-input/1
            ugens:
            -   Control.ir: null
            -   In.ar:
                    bus: Control.ir[0:in_]
            -   SendPeakRMS.ar:
                    peak_lag: 3.0
                    reply_id: 116.0
                    reply_rate: 20.0
            -   Control.kr: null
            -   Linen.kr/0:
                    attack_time: Control.kr[2:lag]
                    done_action: 2.0
                    gate: Control.kr[1:gate]
                    release_time: Control.kr[2:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: In.ar[0]
                    right: Linen.kr/0[0]
            -   Linen.kr/1:
                    attack_time: Control.kr[2:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[2:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(GREATER_THAN).kr:
                    left: Linen.kr/1[0]
                    right: 0.0
            -   HPZ1.kr:
                    source: BinaryOpUGen(GREATER_THAN).kr[0]
            -   UnaryOpUGen(ABSOLUTE_VALUE).kr:
                    source: HPZ1.kr[0]
            -   SendTrig.kr:
                    id_: 0.0
                    trigger: UnaryOpUGen(ABSOLUTE_VALUE).kr[0]
                    value: BinaryOpUGen(GREATER_THAN).kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    right: Linen.kr/1[0]
            -   ReplaceOut.ar:
                    bus: Control.ir[1:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/1[0]

    """
    factory = (
        SynthDefFactory(active=1, gate=1, lag=0.1)
        .with_output(replacing=True)
        .with_input(private=True)
        .with_channel_count(channel_count)
        .with_signal_block(_peak_rms_block_builder("/levels/chain/input"))
        .with_signal_block(_gate_block)
    )
    return factory.build(name=f"mixer/chain-input/{channel_count}")


def build_chain_output_synthdef(channel_count):
    """
    Build chain output synthdef.

    ::

        >>> from supriya.daw import synthdefs
        >>> synthdef = synthdefs.build_chain_output_synthdef(channel_count=1)
        >>> print(synthdef)
        synthdef:
            name: mixer/chain-output/1
            ugens:
            -   Control.ir: null
            -   In.ar:
                    bus: Control.ir[0:in_]
            -   SendPeakRMS.ar/0:
                    peak_lag: 3.0
                    reply_id: 114.0
                    reply_rate: 20.0
            -   Control.kr: null
            -   Linen.kr/0:
                    attack_time: Control.kr[3:lag]
                    done_action: 2.0
                    gate: Control.kr[2:gate]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: In.ar[0]
                    right: Linen.kr/0[0]
            -   Linen.kr/1:
                    attack_time: Control.kr[3:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(GREATER_THAN).kr/0:
                    left: Linen.kr/1[0]
                    right: 0.0
            -   HPZ1.kr:
                    source: BinaryOpUGen(GREATER_THAN).kr/0[0]
            -   UnaryOpUGen(ABSOLUTE_VALUE).kr:
                    source: HPZ1.kr[0]
            -   SendTrig.kr:
                    id_: 0.0
                    trigger: UnaryOpUGen(ABSOLUTE_VALUE).kr[0]
                    value: BinaryOpUGen(GREATER_THAN).kr/0[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    right: Linen.kr/1[0]
            -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                    source: Control.kr[1:gain]
            -   BinaryOpUGen(GREATER_THAN).kr/1:
                    left: Control.kr[1:gain]
                    right: -96.0
            -   BinaryOpUGen(MULTIPLICATION).kr:
                    left: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                    right: BinaryOpUGen(GREATER_THAN).kr/1[0]
            -   Lag.kr:
                    lag_time: Control.kr[3:lag]
                    source: BinaryOpUGen(MULTIPLICATION).kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/2:
                    left: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    right: Lag.kr[0]
            -   SendPeakRMS.ar/1:
                    peak_lag: 3.0
                    reply_id: 114.0
                    reply_rate: 20.0
            -   Out.ar:
                    bus: Control.ir[1:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/2[0]

    """
    factory = (
        SynthDefFactory(active=1, gain=0, gate=1, lag=0.1)
        .with_output()
        .with_input(private=True)
        .with_channel_count(channel_count)
        .with_signal_block(_peak_rms_block_builder("/levels/chain/prefader"))
        .with_signal_block(_gate_block)
        .with_signal_block(_gain_block)
        .with_signal_block(_peak_rms_block_builder("/levels/chain/postfader"))
    )
    return factory.build(name=f"mixer/chain-output/{channel_count}")


def build_rack_output_synthdef(channel_count):
    """
    Build rack output synthdef.

    ::

        >>> from supriya.daw import synthdefs
        >>> synthdef = synthdefs.build_rack_output_synthdef(channel_count=1)
        >>> print(synthdef)
        synthdef:
            name: mixer/rack-output/1
            ugens:
            -   Control.ir: null
            -   In.ar:
                    bus: Control.ir[0:in_]
            -   Control.kr: null
            -   Linen.kr/0:
                    attack_time: Control.kr[2:lag]
                    done_action: 2.0
                    gate: Control.kr[1:gate]
                    release_time: Control.kr[2:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: In.ar[0]
                    right: Linen.kr/0[0]
            -   Linen.kr/1:
                    attack_time: Control.kr[2:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[2:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(GREATER_THAN).kr:
                    left: Linen.kr/1[0]
                    right: 0.0
            -   HPZ1.kr:
                    source: BinaryOpUGen(GREATER_THAN).kr[0]
            -   UnaryOpUGen(ABSOLUTE_VALUE).kr:
                    source: HPZ1.kr[0]
            -   SendTrig.kr:
                    id_: 0.0
                    trigger: UnaryOpUGen(ABSOLUTE_VALUE).kr[0]
                    value: BinaryOpUGen(GREATER_THAN).kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    right: Linen.kr/1[0]
            -   SendPeakRMS.ar:
                    peak_lag: 3.0
                    reply_id: 116.0
                    reply_rate: 20.0
            -   ReplaceOut.ar:
                    bus: Control.ir[1:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/1[0]

    """
    factory = (
        SynthDefFactory(active=1, gate=1, lag=0.1)
        .with_output(replacing=True)
        .with_input(private=True)
        .with_channel_count(channel_count)
        .with_signal_block(_gate_block)
        .with_signal_block(_peak_rms_block_builder("/levels/rack/output"))
    )
    return factory.build(name=f"mixer/rack-output/{channel_count}")


def build_track_input_synthdef(channel_count):
    """
    Build track input synthdef.

    ::

        >>> from supriya.daw import synthdefs
        >>> synthdef = synthdefs.build_track_input_synthdef(channel_count=1)
        >>> print(synthdef)
        synthdef:
            name: mixer/track-input/1
            ugens:
            -   Control.ir: null
            -   InFeedback.ar:
                    bus: Control.ir[0:in_]
            -   In.ar:
                    bus: Control.ir[1:out]
            -   BinaryOpUGen(ADDITION).ar:
                    left: In.ar[0]
                    right: InFeedback.ar[0]
            -   SendPeakRMS.ar:
                    peak_lag: 3.0
                    reply_id: 116.0
                    reply_rate: 20.0
            -   Control.kr: null
            -   Linen.kr/0:
                    attack_time: Control.kr[3:lag]
                    done_action: 2.0
                    gate: Control.kr[2:gate]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: BinaryOpUGen(ADDITION).ar[0]
                    right: Linen.kr/0[0]
            -   Linen.kr/1:
                    attack_time: Control.kr[3:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(GREATER_THAN).kr/0:
                    left: Linen.kr/1[0]
                    right: 0.0
            -   HPZ1.kr:
                    source: BinaryOpUGen(GREATER_THAN).kr/0[0]
            -   UnaryOpUGen(ABSOLUTE_VALUE).kr:
                    source: HPZ1.kr[0]
            -   SendTrig.kr:
                    id_: 0.0
                    trigger: UnaryOpUGen(ABSOLUTE_VALUE).kr[0]
                    value: BinaryOpUGen(GREATER_THAN).kr/0[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    right: Linen.kr/1[0]
            -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                    source: Control.kr[1:gain]
            -   BinaryOpUGen(GREATER_THAN).kr/1:
                    left: Control.kr[1:gain]
                    right: -96.0
            -   BinaryOpUGen(MULTIPLICATION).kr:
                    left: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                    right: BinaryOpUGen(GREATER_THAN).kr/1[0]
            -   Lag.kr:
                    lag_time: Control.kr[3:lag]
                    source: BinaryOpUGen(MULTIPLICATION).kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/2:
                    left: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    right: Lag.kr[0]
            -   ReplaceOut.ar:
                    bus: Control.ir[1:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/2[0]

    """

    def signal_block(builder, source, state):
        return In.ar(bus=builder["out"], channel_count=state["channel_count"]) + source

    factory = (
        SynthDefFactory(active=1, gain=0, gate=1, lag=0.1)
        .with_output(replacing=True)
        .with_input(feedback=True, private=True)
        .with_channel_count(channel_count)
        .with_signal_block(signal_block)
        .with_signal_block(_peak_rms_block_builder("/levels/track/input"))
        .with_signal_block(_gate_block)
        .with_signal_block(_gain_block)
    )
    return factory.build(name=f"mixer/track-input/{channel_count}")


def build_track_output_synthdef(channel_count):
    """
    Build track output synthdef.

    ::

        >>> from supriya.daw import synthdefs
        >>> synthdef = synthdefs.build_track_output_synthdef(channel_count=1)
        >>> print(synthdef)
        synthdef:
            name: mixer/track-output/1
            ugens:
            -   Control.ir: null
            -   In.ar:
                    bus: Control.ir[0:out]
            -   SendPeakRMS.ar/0:
                    peak_lag: 3.0
                    reply_id: 114.0
                    reply_rate: 20.0
            -   Control.kr: null
            -   Linen.kr/0:
                    attack_time: Control.kr[3:lag]
                    done_action: 2.0
                    gate: Control.kr[2:gate]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: In.ar[0]
                    right: Linen.kr/0[0]
            -   Linen.kr/1:
                    attack_time: Control.kr[3:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(GREATER_THAN).kr/0:
                    left: Linen.kr/1[0]
                    right: 0.0
            -   HPZ1.kr:
                    source: BinaryOpUGen(GREATER_THAN).kr/0[0]
            -   UnaryOpUGen(ABSOLUTE_VALUE).kr:
                    source: HPZ1.kr[0]
            -   SendTrig.kr:
                    id_: 0.0
                    trigger: UnaryOpUGen(ABSOLUTE_VALUE).kr[0]
                    value: BinaryOpUGen(GREATER_THAN).kr/0[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    right: Linen.kr/1[0]
            -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                    source: Control.kr[1:gain]
            -   BinaryOpUGen(GREATER_THAN).kr/1:
                    left: Control.kr[1:gain]
                    right: -96.0
            -   BinaryOpUGen(MULTIPLICATION).kr:
                    left: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                    right: BinaryOpUGen(GREATER_THAN).kr/1[0]
            -   Lag.kr:
                    lag_time: Control.kr[3:lag]
                    source: BinaryOpUGen(MULTIPLICATION).kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/2:
                    left: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    right: Lag.kr[0]
            -   SendPeakRMS.ar/1:
                    peak_lag: 3.0
                    reply_id: 114.0
                    reply_rate: 20.0
            -   ReplaceOut.ar:
                    bus: Control.ir[0:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/2[0]

    """
    factory = (
        SynthDefFactory(active=1, gain=0, gate=1, lag=0.1)
        .with_output(replacing=True)
        .with_input()
        .with_channel_count(channel_count)
        .with_signal_block(_peak_rms_block_builder("/levels/track/prefader"))
        .with_signal_block(_gate_block)
        .with_signal_block(_gain_block)
        .with_signal_block(_peak_rms_block_builder("/levels/track/postfader"))
    )
    return factory.build(name=f"mixer/track-output/{channel_count}")


def build_send_synthdef(source_track_count, target_track_count):
    synthdef_builder = SynthDefBuilder(
        active=1,
        gain=0,
        gate=1,
        in_=Parameter(value=0, parameter_rate="scalar"),
        lag=0.1,
        out=Parameter(value=0, parameter_rate="scalar"),
    )
    with synthdef_builder:
        source = In.ar(bus=synthdef_builder["in_"], channel_count=source_track_count)
        mix_factor = source_track_count / target_track_count
        if source_track_count == target_track_count:
            pass
        elif target_track_count == 1:
            source = Mix.new(source) / mix_factor
        elif source_track_count == 1:
            source = UGenArray([source] * target_track_count)
        else:
            panners = []
            for i, channel in enumerate(source):
                position = (-1 / len(source)) + ((2 / len(source)) * i)
                amplitude = 1
                width = 2 * (1 / mix_factor)
                if mix_factor > 1:
                    amplitude = 1 / mix_factor
                panner = PanAz.ar(
                    channel_count=target_track_count,
                    source=channel,
                    position=position,
                    amplitude=amplitude,
                    width=width,
                )
                panners.extend(panner)
            source = Mix.multichannel(panners, target_track_count)
        source *= with_gain(synthdef_builder)
        Out.ar(bus=synthdef_builder["out"], source=source)
    name = f"mixer/send/{source_track_count}x{target_track_count}"
    return synthdef_builder.build(name=name)
