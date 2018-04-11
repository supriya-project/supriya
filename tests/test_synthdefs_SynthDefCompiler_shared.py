from supriya import SynthDefBuilder
from supriya import systemtools
import supriya.ugens


class TestCase(systemtools.TestCase):

    def test_01(self):
        """
        Cannot share UGens.
        """

        with SynthDefBuilder():
            sine_one = supriya.ugens.SinOsc.ar()
            supriya.ugens.Out.ar(bus=0, source=sine_one)

        with SynthDefBuilder():
            sine_two = supriya.ugens.SinOsc.ar()
            with self.assertRaises(ValueError) as context_manager:
                sine_two * sine_one
            exception_text = context_manager.exception.args[0]
            assert 'UGen input in different scope' in exception_text

    def test_02(self):
        """
        Cannot share parameters.
        """

        with SynthDefBuilder(bus=0) as builder:
            sine_one = supriya.ugens.SinOsc.ar()
            synth_one_bus = builder['bus']
            supriya.ugens.Out.ar(bus=synth_one_bus, source=sine_one)

        with SynthDefBuilder():
            sine_two = supriya.ugens.SinOsc.ar()
            with self.assertRaises(ValueError) as context_manager:
                supriya.ugens.Out.ar(bus=synth_one_bus, source=sine_two)
            exception_text = context_manager.exception.args[0]
            assert 'UGen input in different scope' in exception_text

    def test_03(self):
        """
        Cannot share output proxies.
        """
        with SynthDefBuilder():
            left, right = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            supriya.ugens.Out.ar(bus=0, source=[right, left])

        with SynthDefBuilder():
            with self.assertRaises(ValueError) as context_manager:
                left * right
            exception_text = context_manager.exception.args[0]
            assert 'UGen input in different scope' in exception_text
