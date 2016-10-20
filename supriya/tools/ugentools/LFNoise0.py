# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class LFNoise0(UGen):
    """
    A step noise generator.

    ::

        >>> ugentools.LFNoise0.ar()
        LFNoise0.ar()

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
        Constructs an audio-rate step noise generator.

        ::

            >>> ugentools.LFNoise0.ar(
            ...     frequency=10,
            ...     )
            LFNoise0.ar()

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
        Constructs a control-rate step noise generator.

        ::

            >>> ugentools.LFNoise0.kr(
            ...     frequency=10,
            ...     )
            LFNoise0.kr()

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
        Gets `frequency` input of LFNoise0.

        ::

            >>> frequency = 0.5
            >>> lf_noise_0 = ugentools.LFNoise0.ar(
            ...     frequency=frequency,
            ...     )
            >>> lf_noise_0.frequency
            0.5

        Returns input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]
