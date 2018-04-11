from supriya.ugens.UGen import UGen


class LinRand(UGen):
    """
    A skewed linear random distribution.

    ::

        >>> lin_rand = supriya.ugens.LinRand.ir(
        ...    minimum=-1.,
        ...    maximum=1.,
        ...    skew=0.5,
        ...    )
        >>> lin_rand
        LinRand.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        'skew',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        minimum=0.,
        maximum=1.,
        skew=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            minimum=minimum,
            maximum=maximum,
            skew=skew,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ir(
        cls,
        maximum=1,
        minimum=0,
        skew=0,
        ):
        """
        Constructs a skewed linear random distribution.

        ::

            >>> lin_rand = supriya.ugens.LinRand.ir(
            ...    minimum=-1.,
            ...    maximum=1.,
            ...    skew=[-0.5, 0.5],
            ...    )
            >>> lin_rand
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            skew=skew,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        """
        Gets `maximum` input of LinRand.

        ::

            >>> lin_rand = supriya.ugens.LinRand.ir(
            ...     minimum=-1.0,
            ...     maximum=1.0,
            ...     skew=0.9,
            ...     )
            >>> lin_rand.maximum
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        """
        Gets `minimum` input of LinRand.

        ::

            >>> lin_rand = supriya.ugens.LinRand.ir(
            ...     minimum=-1.0,
            ...     maximum=1.0,
            ...     skew=0.9,
            ...     )
            >>> lin_rand.minimum
            -1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]

    @property
    def skew(self):
        """
        Gets `skew` input of LinRand.

        ::

            >>> lin_rand = supriya.ugens.LinRand.ir(
            ...     minimum=-1.0,
            ...     maximum=1.0,
            ...     skew=0.9,
            ...     )
            >>> lin_rand.skew
            0.9

        Returns ugen input.
        """
        index = self._ordered_input_names.index('skew')
        return self._inputs[index]
