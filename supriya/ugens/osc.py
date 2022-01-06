import collections

from supriya import CalculationRate
from supriya.synthdefs import PureUGen, UGen


class COsc(PureUGen):
    """
    A chorusing wavetable oscillator.

    ::

        >>> cosc = supriya.ugens.COsc.ar(
        ...     beats=0.5,
        ...     buffer_id=23,
        ...     frequency=440,
        ... )
        >>> cosc
        COsc.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("frequency", 440.0), ("beats", 0.5)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class DegreeToKey(PureUGen):
    """
    A signal-to-modal-pitch converter.`

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> degree_to_key = supriya.ugens.DegreeToKey.ar(
        ...     buffer_id=23,
        ...     octave=12,
        ...     source=source,
        ... )
        >>> degree_to_key
        DegreeToKey.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("source", None), ("octave", 12)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Impulse(PureUGen):
    """
    A non-band-limited single-sample impulse generator unit generator.

    ::

        >>> supriya.ugens.Impulse.ar()
        Impulse.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("phase", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Index(PureUGen):
    """
    A clipping buffer indexer.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> index = supriya.ugens.Index.ar(
        ...     buffer_id=23,
        ...     source=source,
        ... )
        >>> index
        Index.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("source", None)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFCub(PureUGen):
    """
    A sine-like oscillator unit generator.

    ::

        >>> supriya.ugens.LFCub.ar()
        LFCub.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("initial_phase", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFGauss(PureUGen):
    """
    A non-band-limited gaussian function oscillator.

    ::

        >>> supriya.ugens.LFGauss.ar()
        LFGauss.ar()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict(
        [
            ("duration", 1),
            ("width", 0.1),
            ("initial_phase", 0),
            ("loop", 1),
            ("done_action", 0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        done_action=0,
        duration=1,
        initial_phase=0,
        loop=1,
        width=0.1,
    ):
        import supriya.synthdefs

        done_action = supriya.DoneAction.from_expr(done_action)
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            done_action=done_action,
            duration=duration,
            initial_phase=initial_phase,
            loop=loop,
            width=width,
        )


class LFPar(PureUGen):
    """
    A parabolic oscillator unit generator.

    ::

        >>> supriya.ugens.LFPar.ar()
        LFPar.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("initial_phase", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFPulse(PureUGen):
    """
    A non-band-limited pulse oscillator.

    ::

        >>> supriya.ugens.LFPulse.ar()
        LFPulse.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("initial_phase", 0), ("width", 0.5)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFSaw(PureUGen):
    """
    A non-band-limited sawtooth oscillator unit generator.

    ::

        >>> supriya.ugens.LFSaw.ar()
        LFSaw.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("initial_phase", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class LFTri(PureUGen):
    """
    A non-band-limited triangle oscillator unit generator.

    ::

        >>> supriya.ugens.LFTri.ar()
        LFTri.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("initial_phase", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Osc(PureUGen):
    """
    An interpolating wavetable oscillator.
    """

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", 0), ("frequency", 440.0), ("initial_phase", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class OscN(PureUGen):
    """
    A non-interpolating wavetable oscillator.
    """

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", 0), ("frequency", 440.0), ("initial_phase", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Select(PureUGen):
    """
    A signal selector.

    ::

        >>> sources = supriya.ugens.In.ar(bus=0, channel_count=8)
        >>> selector = supriya.ugens.Phasor.kr() * 8
        >>> select = supriya.ugens.Select.ar(
        ...     sources=sources,
        ...     selector=selector,
        ... )
        >>> select
        Select.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("selector", None), ("sources", None)]
    )
    _unexpanded_input_names = ("sources",)
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class SinOsc(PureUGen):
    """
    A sinusoid oscillator unit generator.

    ::

        >>> supriya.ugens.SinOsc.ar()
        SinOsc.ar()

    ::

        >>> print(_)
        synthdef:
            name: ...
            ugens:
            -   SinOsc.ar:
                    frequency: 440.0
                    phase: 0.0

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("phase", 0.0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class SyncSaw(PureUGen):
    """
    A sawtooth wave that is hard synched to a fundamental pitch.

    ::

        >>> sync_saw = supriya.ugens.SyncSaw.ar(
        ...     saw_frequency=440,
        ...     sync_frequency=440,
        ... )
        >>> sync_saw
        SyncSaw.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("sync_frequency", 440), ("saw_frequency", 440)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class VOsc(PureUGen):
    """
    A wavetable lookup oscillator which can be swept smoothly across wavetables.

    ::

        >>> vosc = supriya.ugens.VOsc.ar(
        ...     buffer_id=supriya.ugens.MouseX.kr(0, 7),
        ...     frequency=440,
        ...     phase=0,
        ... )
        >>> vosc
        VOsc.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("frequency", 440), ("phase", 0)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class VOsc3(PureUGen):
    """
    A wavetable lookup oscillator which can be swept smoothly across wavetables.

    ::

        >>> vosc_3 = supriya.ugens.VOsc3.ar(
        ...     buffer_id=supriya.ugens.MouseX.kr(0, 7),
        ...     freq_1=110,
        ...     freq_2=220,
        ...     freq_3=440,
        ... )
        >>> vosc_3
        VOsc3.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("freq_1", 110), ("freq_2", 220), ("freq_3", 440)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class VarSaw(PureUGen):
    """
    A sawtooth-triangle oscillator with variable duty.

    ::

        >>> supriya.ugens.VarSaw.ar()
        VarSaw.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("frequency", 440.0), ("initial_phase", 0.0), ("width", 0.5)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Vibrato(PureUGen):
    """
    Vibrato is a slow frequency modulation.

    ::

        >>> vibrato = supriya.ugens.Vibrato.ar(
        ...     delay=0,
        ...     depth=0.02,
        ...     depth_variation=0.1,
        ...     frequency=440,
        ...     initial_phase=0,
        ...     onset=0,
        ...     rate=6,
        ...     rate_variation=0.04,
        ... )
        >>> vibrato
        Vibrato.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("frequency", 440),
            ("rate", 6),
            ("depth", 0.02),
            ("delay", 0),
            ("onset", 0),
            ("rate_variation", 0.04),
            ("depth_variation", 0.1),
            ("initial_phase", 0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class WrapIndex(UGen):
    """
    A wrapping buffer indexer.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> wrap_index = supriya.ugens.WrapIndex.ar(
        ...     buffer_id=23,
        ...     source=source,
        ... )
        >>> wrap_index
        WrapIndex.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("buffer_id", None), ("source", None)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)
