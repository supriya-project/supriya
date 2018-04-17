import supriya.live
import uqbar.strings


def test_build_input_synthdef_1():
    synthdef = supriya.live.Track.build_input_synthdef(1)
    assert str(synthdef) == uqbar.strings.normalize("""
        synthdef:
            name: mixer/input/1
            ugens:
            -   Control.ir: null
            -   InFeedback.ar:
                    bus: Control.ir[0:in_]
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
            -   Linen.kr/1:
                    attack_time: Control.kr[3:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: Linen.kr/0[0]
                    right: Linen.kr/1[0]
            -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                    source: Control.kr[1:gain]
            -   BinaryOpUGen(GREATER_THAN).kr:
                    left: Control.kr[1:gain]
                    right: -96.0
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                    right: BinaryOpUGen(GREATER_THAN).kr[0]
            -   Lag.kr:
                    lag_time: Control.kr[3:lag]
                    source: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   BinaryOpUGen(MULTIPLICATION).kr/2:
                    left: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    right: Lag.kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: InFeedback.ar[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   ReplaceOut.ar:
                    bus: Control.ir[1:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
        """) + '\n'


def test_build_input_synthdef_2():
    synthdef = supriya.live.Track.build_input_synthdef(2)
    assert str(synthdef) == uqbar.strings.normalize("""
        synthdef:
            name: mixer/input/2
            ugens:
            -   Control.ir: null
            -   InFeedback.ar:
                    bus: Control.ir[0:in_]
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
            -   Linen.kr/1:
                    attack_time: Control.kr[3:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: Linen.kr/0[0]
                    right: Linen.kr/1[0]
            -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                    source: Control.kr[1:gain]
            -   BinaryOpUGen(GREATER_THAN).kr:
                    left: Control.kr[1:gain]
                    right: -96.0
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                    right: BinaryOpUGen(GREATER_THAN).kr[0]
            -   Lag.kr:
                    lag_time: Control.kr[3:lag]
                    source: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   BinaryOpUGen(MULTIPLICATION).kr/2:
                    left: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    right: Lag.kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: InFeedback.ar[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: InFeedback.ar[1]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   ReplaceOut.ar:
                    bus: Control.ir[1:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
        """) + '\n'


def test_build_input_synthdef_4():
    synthdef = supriya.live.Track.build_input_synthdef(4)
    assert str(synthdef) == uqbar.strings.normalize("""
        synthdef:
            name: mixer/input/4
            ugens:
            -   Control.ir: null
            -   InFeedback.ar:
                    bus: Control.ir[0:in_]
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
            -   Linen.kr/1:
                    attack_time: Control.kr[3:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: Linen.kr/0[0]
                    right: Linen.kr/1[0]
            -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                    source: Control.kr[1:gain]
            -   BinaryOpUGen(GREATER_THAN).kr:
                    left: Control.kr[1:gain]
                    right: -96.0
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                    right: BinaryOpUGen(GREATER_THAN).kr[0]
            -   Lag.kr:
                    lag_time: Control.kr[3:lag]
                    source: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   BinaryOpUGen(MULTIPLICATION).kr/2:
                    left: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    right: Lag.kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: InFeedback.ar[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: InFeedback.ar[1]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/2:
                    left: InFeedback.ar[2]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/3:
                    left: InFeedback.ar[3]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   ReplaceOut.ar:
                    bus: Control.ir[1:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                    source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
        """) + '\n'


def test_build_input_synthdef_8():
    synthdef = supriya.live.Track.build_input_synthdef(8)
    assert str(synthdef) == uqbar.strings.normalize("""
        synthdef:
            name: mixer/input/8
            ugens:
            -   Control.ir: null
            -   InFeedback.ar:
                    bus: Control.ir[0:in_]
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
            -   Linen.kr/1:
                    attack_time: Control.kr[3:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: Linen.kr/0[0]
                    right: Linen.kr/1[0]
            -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                    source: Control.kr[1:gain]
            -   BinaryOpUGen(GREATER_THAN).kr:
                    left: Control.kr[1:gain]
                    right: -96.0
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                    right: BinaryOpUGen(GREATER_THAN).kr[0]
            -   Lag.kr:
                    lag_time: Control.kr[3:lag]
                    source: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   BinaryOpUGen(MULTIPLICATION).kr/2:
                    left: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    right: Lag.kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: InFeedback.ar[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: InFeedback.ar[1]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/2:
                    left: InFeedback.ar[2]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/3:
                    left: InFeedback.ar[3]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/4:
                    left: InFeedback.ar[4]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/5:
                    left: InFeedback.ar[5]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/6:
                    left: InFeedback.ar[6]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/7:
                    left: InFeedback.ar[7]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   ReplaceOut.ar:
                    bus: Control.ir[1:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                    source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
                    source[4]: BinaryOpUGen(MULTIPLICATION).ar/4[0]
                    source[5]: BinaryOpUGen(MULTIPLICATION).ar/5[0]
                    source[6]: BinaryOpUGen(MULTIPLICATION).ar/6[0]
                    source[7]: BinaryOpUGen(MULTIPLICATION).ar/7[0]
        """) + '\n'


def test_build_output_synthdef_1():
    synthdef = supriya.live.Track.build_output_synthdef(1)
    assert str(synthdef) == uqbar.strings.normalize("""
        synthdef:
            name: mixer/output/1
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
            -   Linen.kr/1:
                    attack_time: Control.kr[3:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: Linen.kr/0[0]
                    right: Linen.kr/1[0]
            -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                    source: Control.kr[1:gain]
            -   BinaryOpUGen(GREATER_THAN).kr:
                    left: Control.kr[1:gain]
                    right: -96.0
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                    right: BinaryOpUGen(GREATER_THAN).kr[0]
            -   Lag.kr:
                    lag_time: Control.kr[3:lag]
                    source: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   BinaryOpUGen(MULTIPLICATION).kr/2:
                    left: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    right: Lag.kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar:
                    left: In.ar[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   SendPeakRMS.ar/1:
                    peak_lag: 3.0
                    reply_id: 114.0
                    reply_rate: 20.0
            -   ReplaceOut.ar:
                    bus: Control.ir[0:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
        """) + '\n'


def test_build_output_synthdef_2():
    synthdef = supriya.live.Track.build_output_synthdef(2)
    assert str(synthdef) == uqbar.strings.normalize("""
        synthdef:
            name: mixer/output/2
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
            -   Linen.kr/1:
                    attack_time: Control.kr[3:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: Linen.kr/0[0]
                    right: Linen.kr/1[0]
            -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                    source: Control.kr[1:gain]
            -   BinaryOpUGen(GREATER_THAN).kr:
                    left: Control.kr[1:gain]
                    right: -96.0
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                    right: BinaryOpUGen(GREATER_THAN).kr[0]
            -   Lag.kr:
                    lag_time: Control.kr[3:lag]
                    source: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   BinaryOpUGen(MULTIPLICATION).kr/2:
                    left: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    right: Lag.kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: In.ar[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: In.ar[1]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   SendPeakRMS.ar/1:
                    peak_lag: 3.0
                    reply_id: 114.0
                    reply_rate: 20.0
            -   ReplaceOut.ar:
                    bus: Control.ir[0:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
        """) + '\n'


def test_build_output_synthdef_4():
    synthdef = supriya.live.Track.build_output_synthdef(4)
    assert str(synthdef) == uqbar.strings.normalize("""
        synthdef:
            name: mixer/output/4
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
            -   Linen.kr/1:
                    attack_time: Control.kr[3:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: Linen.kr/0[0]
                    right: Linen.kr/1[0]
            -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                    source: Control.kr[1:gain]
            -   BinaryOpUGen(GREATER_THAN).kr:
                    left: Control.kr[1:gain]
                    right: -96.0
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                    right: BinaryOpUGen(GREATER_THAN).kr[0]
            -   Lag.kr:
                    lag_time: Control.kr[3:lag]
                    source: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   BinaryOpUGen(MULTIPLICATION).kr/2:
                    left: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    right: Lag.kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: In.ar[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: In.ar[1]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/2:
                    left: In.ar[2]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/3:
                    left: In.ar[3]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   SendPeakRMS.ar/1:
                    peak_lag: 3.0
                    reply_id: 114.0
                    reply_rate: 20.0
            -   ReplaceOut.ar:
                    bus: Control.ir[0:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                    source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
        """) + '\n'


def test_build_output_synthdef_8():
    synthdef = supriya.live.Track.build_output_synthdef(8)
    assert str(synthdef) == uqbar.strings.normalize("""
        synthdef:
            name: mixer/output/8
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
            -   Linen.kr/1:
                    attack_time: Control.kr[3:lag]
                    done_action: 0.0
                    gate: Control.kr[0:active]
                    release_time: Control.kr[3:lag]
                    sustain_level: 1.0
            -   BinaryOpUGen(MULTIPLICATION).kr/0:
                    left: Linen.kr/0[0]
                    right: Linen.kr/1[0]
            -   UnaryOpUGen(DB_TO_AMPLITUDE).kr:
                    source: Control.kr[1:gain]
            -   BinaryOpUGen(GREATER_THAN).kr:
                    left: Control.kr[1:gain]
                    right: -96.0
            -   BinaryOpUGen(MULTIPLICATION).kr/1:
                    left: UnaryOpUGen(DB_TO_AMPLITUDE).kr[0]
                    right: BinaryOpUGen(GREATER_THAN).kr[0]
            -   Lag.kr:
                    lag_time: Control.kr[3:lag]
                    source: BinaryOpUGen(MULTIPLICATION).kr/1[0]
            -   BinaryOpUGen(MULTIPLICATION).kr/2:
                    left: BinaryOpUGen(MULTIPLICATION).kr/0[0]
                    right: Lag.kr[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/0:
                    left: In.ar[0]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/1:
                    left: In.ar[1]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/2:
                    left: In.ar[2]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/3:
                    left: In.ar[3]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/4:
                    left: In.ar[4]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/5:
                    left: In.ar[5]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/6:
                    left: In.ar[6]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   BinaryOpUGen(MULTIPLICATION).ar/7:
                    left: In.ar[7]
                    right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
            -   SendPeakRMS.ar/1:
                    peak_lag: 3.0
                    reply_id: 114.0
                    reply_rate: 20.0
            -   ReplaceOut.ar:
                    bus: Control.ir[0:out]
                    source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                    source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                    source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                    source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
                    source[4]: BinaryOpUGen(MULTIPLICATION).ar/4[0]
                    source[5]: BinaryOpUGen(MULTIPLICATION).ar/5[0]
                    source[6]: BinaryOpUGen(MULTIPLICATION).ar/6[0]
                    source[7]: BinaryOpUGen(MULTIPLICATION).ar/7[0]
        """) + '\n'
