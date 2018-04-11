from supriya.ugens.UGen import UGen


class LFDNoise1(UGen):
    """
    A dynamic ramp noise generator.

    ::

        >>> supriya.ugens.LFDNoise1.ar()
        LFDNoise1.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=500,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=500,
        ):
        """
        Constructs an audio-rate ramp noise generator.

        ::

            >>> supriya.ugens.LFDNoise1.ar(
            ...     frequency=10,
            ...     )
            LFDNoise1.ar()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=500,
        ):
        """
        Constructs a control-rate ramp noise generator.

        ::

            >>> supriya.ugens.LFDNoise1.kr(
            ...     frequency=10,
            ...     )
            LFDNoise1.kr()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of LFDNoise1.

        ::

            >>> frequency = 0.5
            >>> lf_noise_0 = supriya.ugens.LFDNoise1.ar(
            ...     frequency=frequency,
            ...     )
            >>> lf_noise_0.frequency
            0.5

        Returns input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]
