import supriya.live
import supriya.system


class TestCase(supriya.system.TestCase):

    def test_build_synthdef_01(self):
        synthdef = supriya.live.Direct.build_synthdef(
            2, 2, [(0, 0), (1, 1)])
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/direct/0:0,1:1
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   Control.kr: null
                -   Linen.kr:
                        attack_time: Control.kr[1:lag]
                        done_action: 2.0
                        gate: Control.kr[0:gate]
                        release_time: Control.kr[1:lag]
                        sustain_level: 1.0
                -   BinaryOpUGen(MULTIPLICATION).ar/0:
                        left: In.ar[0]
                        right: Linen.kr[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: In.ar[1]
                        right: Linen.kr[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
            """)

    def test_build_synthdef_02(self):
        synthdef = supriya.live.Direct.build_synthdef(
            2, 2, [(0, 1), (1, 0)])
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/direct/0:1,1:0
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   Control.kr: null
                -   Linen.kr:
                        attack_time: Control.kr[1:lag]
                        done_action: 2.0
                        gate: Control.kr[0:gate]
                        release_time: Control.kr[1:lag]
                        sustain_level: 1.0
                -   BinaryOpUGen(MULTIPLICATION).ar/0:
                        left: In.ar[0]
                        right: Linen.kr[0]
                -   BinaryOpUGen(MULTIPLICATION).ar/1:
                        left: In.ar[1]
                        right: Linen.kr[0]
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: BinaryOpUGen(MULTIPLICATION).ar/1[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar/0[0]
            """)

    def test_build_synthdef_03(self):
        synthdef = supriya.live.Direct.build_synthdef(
            2, 2, [(0, 1)])
        self.compare_strings(
            str(synthdef),
            """
            synthdef:
                name: mixer/direct/0:1
                ugens:
                -   Control.ir: null
                -   In.ar:
                        bus: Control.ir[0:in_]
                -   Control.kr: null
                -   Linen.kr:
                        attack_time: Control.kr[1:lag]
                        done_action: 2.0
                        gate: Control.kr[0:gate]
                        release_time: Control.kr[1:lag]
                        sustain_level: 1.0
                -   BinaryOpUGen(MULTIPLICATION).ar:
                        left: In.ar[0]
                        right: Linen.kr[0]
                -   DC.ar:
                        source: 0.0
                -   Out.ar:
                        bus: Control.ir[1:out]
                        source[0]: DC.ar[0]
                        source[1]: BinaryOpUGen(MULTIPLICATION).ar[0]
            """)
