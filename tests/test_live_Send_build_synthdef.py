import supriya.live
from supriya.tools import systemtools


class TestCase(systemtools.TestCase):

    def test_build_synthdef_1_1(self):
        synthdef = supriya.live.Send.build_synthdef(1, 1)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/1x1
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
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
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
            """)

    def test_build_synthdef_1_2(self):
        synthdef = supriya.live.Send.build_synthdef(1, 2)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/1x2
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
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
                        left: In.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
            """)

    def test_build_synthdef_1_4(self):
        synthdef = supriya.live.Send.build_synthdef(1, 4)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/1x4
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
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
                        left: In.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/2:
                        left: In.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/3:
                        left: In.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                        source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                        source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
            """)

    def test_build_synthdef_1_8(self):
        synthdef = supriya.live.Send.build_synthdef(1, 8)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/1x8
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
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
                        left: In.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/2:
                        left: In.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/3:
                        left: In.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/4:
                        left: In.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/5:
                        left: In.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/6:
                        left: In.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/7:
                        left: In.ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                        source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                        source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
                        source[4]: BinaryOpUGen(MULTIPLICATION).ar/4[0]
                        source[5]: BinaryOpUGen(MULTIPLICATION).ar/5[0]
                        source[6]: BinaryOpUGen(MULTIPLICATION).ar/6[0]
                        source[7]: BinaryOpUGen(MULTIPLICATION).ar/7[0]
            """)

    def test_build_synthdef_2_1(self):
        synthdef = supriya.live.Send.build_synthdef(2, 1)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/2x1
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   BinaryOpUGen(ADDITION).ar:
                        left: In.ar[0]
                        right: In.ar[1]
                -   BinaryOpUGen(FLOAT_DIVISION).ar:
                        left: BinaryOpUGen(ADDITION).ar[0]
                        right: 2.0
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
                        left: BinaryOpUGen(FLOAT_DIVISION).ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
            """)

    def test_build_synthdef_2_2(self):
        synthdef = supriya.live.Send.build_synthdef(2, 2)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/2x2
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
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
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
            """)

    def test_build_synthdef_2_4(self):
        synthdef = supriya.live.Send.build_synthdef(2, 4)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/2x4
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   PanAz.ar/0:
                        amplitude: 1.0
                        channel_count: 4.0
                        orientation: 0.5
                        position: -0.5
                        source: In.ar[0]
                        width: 4.0
                -   PanAz.ar/1:
                        amplitude: 1.0
                        channel_count: 4.0
                        orientation: 0.5
                        position: 0.5
                        source: In.ar[1]
                        width: 4.0
                -   BinaryOpUGen(ADDITION).ar/0:
                        left: PanAz.ar/0[0]
                        right: PanAz.ar/1[0]
                -   BinaryOpUGen(ADDITION).ar/1:
                        left: PanAz.ar/0[1]
                        right: PanAz.ar/1[1]
                -   BinaryOpUGen(ADDITION).ar/2:
                        left: PanAz.ar/0[2]
                        right: PanAz.ar/1[2]
                -   BinaryOpUGen(ADDITION).ar/3:
                        left: PanAz.ar/0[3]
                        right: PanAz.ar/1[3]
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
                        left: BinaryOpUGen(ADDITION).ar/0[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: BinaryOpUGen(ADDITION).ar/1[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/2:
                        left: BinaryOpUGen(ADDITION).ar/2[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/3:
                        left: BinaryOpUGen(ADDITION).ar/3[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                        source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                        source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
            """)

    def test_build_synthdef_2_8(self):
        synthdef = supriya.live.Send.build_synthdef(2, 8)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/2x8
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   PanAz.ar/0:
                        amplitude: 1.0
                        channel_count: 8.0
                        orientation: 0.5
                        position: -0.5
                        source: In.ar[0]
                        width: 8.0
                -   PanAz.ar/1:
                        amplitude: 1.0
                        channel_count: 8.0
                        orientation: 0.5
                        position: 0.5
                        source: In.ar[1]
                        width: 8.0
                -   BinaryOpUGen(ADDITION).ar/0:
                        left: PanAz.ar/0[0]
                        right: PanAz.ar/1[0]
                -   BinaryOpUGen(ADDITION).ar/1:
                        left: PanAz.ar/0[1]
                        right: PanAz.ar/1[1]
                -   BinaryOpUGen(ADDITION).ar/2:
                        left: PanAz.ar/0[2]
                        right: PanAz.ar/1[2]
                -   BinaryOpUGen(ADDITION).ar/3:
                        left: PanAz.ar/0[3]
                        right: PanAz.ar/1[3]
                -   BinaryOpUGen(ADDITION).ar/4:
                        left: PanAz.ar/0[4]
                        right: PanAz.ar/1[4]
                -   BinaryOpUGen(ADDITION).ar/5:
                        left: PanAz.ar/0[5]
                        right: PanAz.ar/1[5]
                -   BinaryOpUGen(ADDITION).ar/6:
                        left: PanAz.ar/0[6]
                        right: PanAz.ar/1[6]
                -   BinaryOpUGen(ADDITION).ar/7:
                        left: PanAz.ar/0[7]
                        right: PanAz.ar/1[7]
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
                        left: BinaryOpUGen(ADDITION).ar/0[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: BinaryOpUGen(ADDITION).ar/1[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/2:
                        left: BinaryOpUGen(ADDITION).ar/2[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/3:
                        left: BinaryOpUGen(ADDITION).ar/3[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/4:
                        left: BinaryOpUGen(ADDITION).ar/4[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/5:
                        left: BinaryOpUGen(ADDITION).ar/5[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/6:
                        left: BinaryOpUGen(ADDITION).ar/6[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/7:
                        left: BinaryOpUGen(ADDITION).ar/7[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                        source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                        source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
                        source[4]: BinaryOpUGen(MULTIPLICATION).ar/4[0]
                        source[5]: BinaryOpUGen(MULTIPLICATION).ar/5[0]
                        source[6]: BinaryOpUGen(MULTIPLICATION).ar/6[0]
                        source[7]: BinaryOpUGen(MULTIPLICATION).ar/7[0]
            """)

    def test_build_synthdef_4_1(self):
        synthdef = supriya.live.Send.build_synthdef(4, 1)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/4x1
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   Sum4.ar:
                        input_four: In.ar[3]
                        input_one: In.ar[0]
                        input_three: In.ar[2]
                        input_two: In.ar[1]
                -   BinaryOpUGen(FLOAT_DIVISION).ar:
                        left: Sum4.ar[0]
                        right: 4.0
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
                        left: BinaryOpUGen(FLOAT_DIVISION).ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
            """)

    def test_build_synthdef_4_2(self):
        synthdef = supriya.live.Send.build_synthdef(4, 2)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/4x2
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   PanAz.ar/0:
                        amplitude: 0.5
                        channel_count: 2.0
                        orientation: 0.5
                        position: -0.25
                        source: In.ar[0]
                        width: 1.0
                -   PanAz.ar/1:
                        amplitude: 0.5
                        channel_count: 2.0
                        orientation: 0.5
                        position: 0.25
                        source: In.ar[1]
                        width: 1.0
                -   PanAz.ar/2:
                        amplitude: 0.5
                        channel_count: 2.0
                        orientation: 0.5
                        position: 0.75
                        source: In.ar[2]
                        width: 1.0
                -   PanAz.ar/3:
                        amplitude: 0.5
                        channel_count: 2.0
                        orientation: 0.5
                        position: 1.25
                        source: In.ar[3]
                        width: 1.0
                -   Sum4.ar/0:
                        input_four: PanAz.ar/3[0]
                        input_one: PanAz.ar/0[0]
                        input_three: PanAz.ar/2[0]
                        input_two: PanAz.ar/1[0]
                -   Sum4.ar/1:
                        input_four: PanAz.ar/3[1]
                        input_one: PanAz.ar/0[1]
                        input_three: PanAz.ar/2[1]
                        input_two: PanAz.ar/1[1]
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
                        left: Sum4.ar/0[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: Sum4.ar/1[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
            """)

    def test_build_synthdef_4_4(self):
        synthdef = supriya.live.Send.build_synthdef(4, 4)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/4x4
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
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
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                        source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                        source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
            """)

    def test_build_synthdef_4_8(self):
        synthdef = supriya.live.Send.build_synthdef(4, 8)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/4x8
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   PanAz.ar/0:
                        amplitude: 1.0
                        channel_count: 8.0
                        orientation: 0.5
                        position: -0.25
                        source: In.ar[0]
                        width: 4.0
                -   PanAz.ar/1:
                        amplitude: 1.0
                        channel_count: 8.0
                        orientation: 0.5
                        position: 0.25
                        source: In.ar[1]
                        width: 4.0
                -   PanAz.ar/2:
                        amplitude: 1.0
                        channel_count: 8.0
                        orientation: 0.5
                        position: 0.75
                        source: In.ar[2]
                        width: 4.0
                -   PanAz.ar/3:
                        amplitude: 1.0
                        channel_count: 8.0
                        orientation: 0.5
                        position: 1.25
                        source: In.ar[3]
                        width: 4.0
                -   Sum4.ar/0:
                        input_four: PanAz.ar/3[0]
                        input_one: PanAz.ar/0[0]
                        input_three: PanAz.ar/2[0]
                        input_two: PanAz.ar/1[0]
                -   Sum4.ar/1:
                        input_four: PanAz.ar/3[1]
                        input_one: PanAz.ar/0[1]
                        input_three: PanAz.ar/2[1]
                        input_two: PanAz.ar/1[1]
                -   Sum4.ar/2:
                        input_four: PanAz.ar/3[2]
                        input_one: PanAz.ar/0[2]
                        input_three: PanAz.ar/2[2]
                        input_two: PanAz.ar/1[2]
                -   Sum4.ar/3:
                        input_four: PanAz.ar/3[3]
                        input_one: PanAz.ar/0[3]
                        input_three: PanAz.ar/2[3]
                        input_two: PanAz.ar/1[3]
                -   Sum4.ar/4:
                        input_four: PanAz.ar/3[4]
                        input_one: PanAz.ar/0[4]
                        input_three: PanAz.ar/2[4]
                        input_two: PanAz.ar/1[4]
                -   Sum4.ar/5:
                        input_four: PanAz.ar/3[5]
                        input_one: PanAz.ar/0[5]
                        input_three: PanAz.ar/2[5]
                        input_two: PanAz.ar/1[5]
                -   Sum4.ar/6:
                        input_four: PanAz.ar/3[6]
                        input_one: PanAz.ar/0[6]
                        input_three: PanAz.ar/2[6]
                        input_two: PanAz.ar/1[6]
                -   Sum4.ar/7:
                        input_four: PanAz.ar/3[7]
                        input_one: PanAz.ar/0[7]
                        input_three: PanAz.ar/2[7]
                        input_two: PanAz.ar/1[7]
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
                        left: Sum4.ar/0[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: Sum4.ar/1[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/2:
                        left: Sum4.ar/2[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/3:
                        left: Sum4.ar/3[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/4:
                        left: Sum4.ar/4[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/5:
                        left: Sum4.ar/5[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/6:
                        left: Sum4.ar/6[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/7:
                        left: Sum4.ar/7[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                        source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                        source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
                        source[4]: BinaryOpUGen(MULTIPLICATION).ar/4[0]
                        source[5]: BinaryOpUGen(MULTIPLICATION).ar/5[0]
                        source[6]: BinaryOpUGen(MULTIPLICATION).ar/6[0]
                        source[7]: BinaryOpUGen(MULTIPLICATION).ar/7[0]
            """)

    def test_build_synthdef_8_1(self):
        synthdef = supriya.live.Send.build_synthdef(8, 1)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/8x1
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   Sum4.ar/0:
                        input_four: In.ar[3]
                        input_one: In.ar[0]
                        input_three: In.ar[2]
                        input_two: In.ar[1]
                -   Sum4.ar/1:
                        input_four: In.ar[7]
                        input_one: In.ar[4]
                        input_three: In.ar[6]
                        input_two: In.ar[5]
                -   BinaryOpUGen(ADDITION).ar:
                        left: Sum4.ar/0[0]
                        right: Sum4.ar/1[0]
                -   BinaryOpUGen(FLOAT_DIVISION).ar:
                        left: BinaryOpUGen(ADDITION).ar[0]
                        right: 8.0
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
                        left: BinaryOpUGen(FLOAT_DIVISION).ar[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar[0]
            """)

    def test_build_synthdef_8_2(self):
        synthdef = supriya.live.Send.build_synthdef(8, 2)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/8x2
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   PanAz.ar/0:
                        amplitude: 0.25
                        channel_count: 2.0
                        orientation: 0.5
                        position: -0.125
                        source: In.ar[0]
                        width: 0.5
                -   PanAz.ar/1:
                        amplitude: 0.25
                        channel_count: 2.0
                        orientation: 0.5
                        position: 0.125
                        source: In.ar[1]
                        width: 0.5
                -   PanAz.ar/2:
                        amplitude: 0.25
                        channel_count: 2.0
                        orientation: 0.5
                        position: 0.375
                        source: In.ar[2]
                        width: 0.5
                -   PanAz.ar/3:
                        amplitude: 0.25
                        channel_count: 2.0
                        orientation: 0.5
                        position: 0.625
                        source: In.ar[3]
                        width: 0.5
                -   Sum4.ar/0:
                        input_four: PanAz.ar/3[0]
                        input_one: PanAz.ar/0[0]
                        input_three: PanAz.ar/2[0]
                        input_two: PanAz.ar/1[0]
                -   Sum4.ar/1:
                        input_four: PanAz.ar/3[1]
                        input_one: PanAz.ar/0[1]
                        input_three: PanAz.ar/2[1]
                        input_two: PanAz.ar/1[1]
                -   PanAz.ar/4:
                        amplitude: 0.25
                        channel_count: 2.0
                        orientation: 0.5
                        position: 0.875
                        source: In.ar[4]
                        width: 0.5
                -   PanAz.ar/5:
                        amplitude: 0.25
                        channel_count: 2.0
                        orientation: 0.5
                        position: 1.125
                        source: In.ar[5]
                        width: 0.5
                -   PanAz.ar/6:
                        amplitude: 0.25
                        channel_count: 2.0
                        orientation: 0.5
                        position: 1.375
                        source: In.ar[6]
                        width: 0.5
                -   PanAz.ar/7:
                        amplitude: 0.25
                        channel_count: 2.0
                        orientation: 0.5
                        position: 1.625
                        source: In.ar[7]
                        width: 0.5
                -   Sum4.ar/2:
                        input_four: PanAz.ar/7[0]
                        input_one: PanAz.ar/4[0]
                        input_three: PanAz.ar/6[0]
                        input_two: PanAz.ar/5[0]
                -   BinaryOpUGen(ADDITION).ar/0:
                        left: Sum4.ar/0[0]
                        right: Sum4.ar/2[0]
                -   Sum4.ar/3:
                        input_four: PanAz.ar/7[1]
                        input_one: PanAz.ar/4[1]
                        input_three: PanAz.ar/6[1]
                        input_two: PanAz.ar/5[1]
                -   BinaryOpUGen(ADDITION).ar/1:
                        left: Sum4.ar/1[0]
                        right: Sum4.ar/3[0]
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
                        left: BinaryOpUGen(ADDITION).ar/0[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: BinaryOpUGen(ADDITION).ar/1[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
            """)

    def test_build_synthdef_8_4(self):
        synthdef = supriya.live.Send.build_synthdef(8, 4)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/8x4
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   PanAz.ar/0:
                        amplitude: 0.5
                        channel_count: 4.0
                        orientation: 0.5
                        position: -0.125
                        source: In.ar[0]
                        width: 1.0
                -   PanAz.ar/1:
                        amplitude: 0.5
                        channel_count: 4.0
                        orientation: 0.5
                        position: 0.125
                        source: In.ar[1]
                        width: 1.0
                -   PanAz.ar/2:
                        amplitude: 0.5
                        channel_count: 4.0
                        orientation: 0.5
                        position: 0.375
                        source: In.ar[2]
                        width: 1.0
                -   PanAz.ar/3:
                        amplitude: 0.5
                        channel_count: 4.0
                        orientation: 0.5
                        position: 0.625
                        source: In.ar[3]
                        width: 1.0
                -   Sum4.ar/0:
                        input_four: PanAz.ar/3[0]
                        input_one: PanAz.ar/0[0]
                        input_three: PanAz.ar/2[0]
                        input_two: PanAz.ar/1[0]
                -   Sum4.ar/1:
                        input_four: PanAz.ar/3[1]
                        input_one: PanAz.ar/0[1]
                        input_three: PanAz.ar/2[1]
                        input_two: PanAz.ar/1[1]
                -   Sum4.ar/2:
                        input_four: PanAz.ar/3[2]
                        input_one: PanAz.ar/0[2]
                        input_three: PanAz.ar/2[2]
                        input_two: PanAz.ar/1[2]
                -   Sum4.ar/3:
                        input_four: PanAz.ar/3[3]
                        input_one: PanAz.ar/0[3]
                        input_three: PanAz.ar/2[3]
                        input_two: PanAz.ar/1[3]
                -   PanAz.ar/4:
                        amplitude: 0.5
                        channel_count: 4.0
                        orientation: 0.5
                        position: 0.875
                        source: In.ar[4]
                        width: 1.0
                -   PanAz.ar/5:
                        amplitude: 0.5
                        channel_count: 4.0
                        orientation: 0.5
                        position: 1.125
                        source: In.ar[5]
                        width: 1.0
                -   PanAz.ar/6:
                        amplitude: 0.5
                        channel_count: 4.0
                        orientation: 0.5
                        position: 1.375
                        source: In.ar[6]
                        width: 1.0
                -   PanAz.ar/7:
                        amplitude: 0.5
                        channel_count: 4.0
                        orientation: 0.5
                        position: 1.625
                        source: In.ar[7]
                        width: 1.0
                -   Sum4.ar/4:
                        input_four: PanAz.ar/7[0]
                        input_one: PanAz.ar/4[0]
                        input_three: PanAz.ar/6[0]
                        input_two: PanAz.ar/5[0]
                -   BinaryOpUGen(ADDITION).ar/0:
                        left: Sum4.ar/0[0]
                        right: Sum4.ar/4[0]
                -   Sum4.ar/5:
                        input_four: PanAz.ar/7[1]
                        input_one: PanAz.ar/4[1]
                        input_three: PanAz.ar/6[1]
                        input_two: PanAz.ar/5[1]
                -   BinaryOpUGen(ADDITION).ar/1:
                        left: Sum4.ar/1[0]
                        right: Sum4.ar/5[0]
                -   Sum4.ar/6:
                        input_four: PanAz.ar/7[2]
                        input_one: PanAz.ar/4[2]
                        input_three: PanAz.ar/6[2]
                        input_two: PanAz.ar/5[2]
                -   BinaryOpUGen(ADDITION).ar/2:
                        left: Sum4.ar/2[0]
                        right: Sum4.ar/6[0]
                -   Sum4.ar/7:
                        input_four: PanAz.ar/7[3]
                        input_one: PanAz.ar/4[3]
                        input_three: PanAz.ar/6[3]
                        input_two: PanAz.ar/5[3]
                -   BinaryOpUGen(ADDITION).ar/3:
                        left: Sum4.ar/3[0]
                        right: Sum4.ar/7[0]
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
                        left: BinaryOpUGen(ADDITION).ar/0[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: BinaryOpUGen(ADDITION).ar/1[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/2:
                        left: BinaryOpUGen(ADDITION).ar/2[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/3:
                        left: BinaryOpUGen(ADDITION).ar/3[0]
                        right: BinaryOpUGen(MULTIPLICATION).kr/2[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                        source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                        source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
            """)

    def test_build_synthdef_8_8(self):
        synthdef = supriya.live.Send.build_synthdef(8, 8)
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/send/8x8
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
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
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                        source[2]: BinaryOpUGen(MULTIPLICATION).ar/2[0]
                        source[3]: BinaryOpUGen(MULTIPLICATION).ar/3[0]
                        source[4]: BinaryOpUGen(MULTIPLICATION).ar/4[0]
                        source[5]: BinaryOpUGen(MULTIPLICATION).ar/5[0]
                        source[6]: BinaryOpUGen(MULTIPLICATION).ar/6[0]
                        source[7]: BinaryOpUGen(MULTIPLICATION).ar/7[0]
            """)
