from supriya.tools.ugentools.UGen import UGen


class Crackle(UGen):
    """
    A chaotic noise generator.

    ::

        >>> crackle = ugentools.Crackle.ar(
        ...     chaos_parameter=1.25,
        ...     )
        >>> crackle
        Crackle.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'chaos_parameter',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        chaos_parameter=1.5,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            chaos_parameter=chaos_parameter,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        chaos_parameter=1.5,
        ):
        """
        Constructs an audio-rate chaotic noise generator.

        ::

            >>> crackle = ugentools.Crackle.ar(
            ...     chaos_parameter=[1.25, 1.5],
            ...     )
            >>> crackle
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chaos_parameter=chaos_parameter,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        chaos_parameter=1.5,
        ):
        """
        Constructs a control-rate chaotic noise generator.

        ::

            >>> crackle = ugentools.Crackle.kr(
            ...     chaos_parameter=[1.25, 1.5],
            ...     )
            >>> crackle
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            chaos_parameter=chaos_parameter,
            )
        return ugen

    ### PUBLIC PROPERTIES ###
    
    @property
    def chaos_parameter(self):
        """
        Gets `chaos_parameter` input of Crackle.

        ::

            >>> crackle = ugentools.Crackle.ar(
            ...     chaos_parameter=1.25,
            ...     )
            >>> crackle.chaos_parameter
            1.25

        Returns ugen input.
        """
        index = self._ordered_input_names.index('chaos_parameter')
        return self._inputs[index]
