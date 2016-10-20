# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class Blip(UGen):
    """
    A band limited impulse generator.

    ::

        >>> blip = ugentools.Blip.ar(
        ...     frequency=440,
        ...     harmonic_count=200,
        ...     )
        >>> blip
        Blip.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Oscillator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'harmonic_count',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440,
        harmonic_count=200,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            harmonic_count=harmonic_count,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        harmonic_count=200,
        ):
        """
        Constructs an audio-rate Blip.

        ::

            >>> blip = ugentools.Blip.ar(
            ...     frequency=440,
            ...     harmonic_count=200,
            ...     )
            >>> blip
            Blip.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            harmonic_count=harmonic_count,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=440,
        harmonic_count=200,
        ):
        """
        Constructs a control-rate Blip.

        ::

            >>> blip = ugentools.Blip.kr(
            ...     frequency=440,
            ...     harmonic_count=200,
            ...     )
            >>> blip
            Blip.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            harmonic_count=harmonic_count,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of Blip.

        ::

            >>> blip = ugentools.Blip.ar(
            ...     frequency=440,
            ...     harmonic_count=200,
            ...     )
            >>> blip.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def harmonic_count(self):
        """
        Gets `harmonic_count` input of Blip.

        ::

            >>> blip = ugentools.Blip.ar(
            ...     frequency=440,
            ...     harmonic_count=200,
            ...     )
            >>> blip.harmonic_count
            200.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('harmonic_count')
        return self._inputs[index]
