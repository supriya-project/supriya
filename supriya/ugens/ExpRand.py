from supriya.ugens.UGen import UGen


class ExpRand(UGen):
    """
    An exponential random distribution.

    ::

        >>> exp_rand = supriya.ugens.ExpRand.ir()
        >>> exp_rand
        ExpRand.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        minimum=0.,
        maximum=1.,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            minimum=minimum,
            maximum=maximum,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(
        cls,
        maximum=1,
        minimum=0.01,
        ):
        """
        Constructs a scalar-rate exponential random distribution.

        ::

            >>> exp_rand = supriya.ugens.ExpRand.ir(
            ...     maximum=[1.1, 1.2, 1.3],
            ...     minimum=[0.25, 0.75],
            ...     )
            >>> exp_rand
            UGenArray({3})

        returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        """
        Gets `maximum` input of ExpRand.

        ::

            >>> exp_rand = supriya.ugens.ExpRand.ir(
            ...     minimum=-1.0,
            ...     maximum=1.0,
            ...     )
            >>> exp_rand.maximum
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        """
        Gets `minimum` input of ExpRand.

        ::

            >>> exp_rand = supriya.ugens.ExpRand.ir(
            ...     minimum=-1.0,
            ...     maximum=1.0,
            ...     )
            >>> exp_rand.minimum
            -1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]
