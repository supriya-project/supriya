import collections

from supriya import CalculationRate
from supriya.synthdefs import PseudoUGen, UGen

from .delay import DelayN


class Amplitude(UGen):
    """
    An amplitude follower.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> amplitude = supriya.ugens.Amplitude.kr(
        ...     attack_time=0.01,
        ...     release_time=0.01,
        ...     source=source,
        ... )
        >>> amplitude
        Amplitude.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("attack_time", 0.01), ("release_time", 0.01)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)


class Compander(UGen):
    """
    A general purpose hard-knee dynamics processor.

    """

    _ordered_input_names = collections.OrderedDict(
        [
            ("source", None),
            ("control", 0.0),
            ("threshold", 0.5),
            ("slope_below", 1.0),
            ("slope_above", 1.0),
            ("clamp_time", 0.01),
            ("relax_time", 0.1),
        ]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class CompanderD(PseudoUGen):
    """
    A convenience constructor for Compander.
    """

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        threshold=0.5,
        clamp_time=0.01,
        relax_time=0.1,
        slope_above=1.0,
        slope_below=1.0,
    ):
        """
        Constructs an audio-rate dynamics processor.

        ..  container:: example

            ::

                >>> source = supriya.ugens.In.ar(bus=0)
                >>> compander_d = supriya.ugens.CompanderD.ar(
                ...     source=source,
                ... )
                >>> supriya.graph(compander_d)  # doctest: +SKIP

            ::

                >>> print(compander_d)
                synthdef:
                    name: d4e7b88df56af5070a88f09b0f8c633e
                    ugens:
                    -   In.ar:
                            bus: 0.0
                    -   DelayN.ar:
                            source: In.ar[0]
                            maximum_delay_time: 0.01
                            delay_time: 0.01
                    -   Compander.ar:
                            source: In.ar[0]
                            control: DelayN.ar[0]
                            threshold: 0.5
                            slope_below: 1.0
                            slope_above: 1.0
                            clamp_time: 0.01
                            relax_time: 0.1

        Returns ugen graph.
        """
        control = DelayN.ar(
            source=source, maximum_delay_time=clamp_time, delay_time=clamp_time
        )
        return Compander._new_expanded(
            clamp_time=clamp_time,
            calculation_rate=CalculationRate.AUDIO,
            relax_time=relax_time,
            slope_above=slope_above,
            slope_below=slope_below,
            source=source,
            control=control,
            threshold=threshold,
        )


class Limiter(UGen):
    """
    A peak limiter.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> limiter = supriya.ugens.Limiter.ar(
        ...     duration=0.01,
        ...     level=1,
        ...     source=source,
        ... )
        >>> limiter
        Limiter.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("level", 1), ("duration", 0.01)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)


class Normalizer(UGen):
    """
    A dynamics flattener.

    ::

        >>> source = supriya.ugens.In.ar(0)
        >>> normalizer = supriya.ugens.Normalizer.ar(
        ...     duration=0.01,
        ...     level=1,
        ...     source=source,
        ... )
        >>> normalizer
        Normalizer.ar()

    """

    _ordered_input_names = collections.OrderedDict(
        [("source", None), ("level", 1), ("duration", 0.01)]
    )
    _valid_calculation_rates = (CalculationRate.AUDIO,)
