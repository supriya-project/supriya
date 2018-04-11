from supriya.ugens.UGen import UGen


class IRand(UGen):
    """
    An integer uniform random distribution.

    ::

        >>> supriya.ugens.IRand.ir()
        IRand.ir()

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
        minimum=0,
        maximum=127,
        ):
        minimum = int(minimum)
        maximum = int(maximum)
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
        maximum=127,
        minimum=0,
        ):
        """
        Constructs a scalar-rate integer uniform random distribution.

        ::

            >>> i_rand = supriya.ugens.IRand.ir(
            ...     maximum=[1.1, 1.2, 1.3],
            ...     minimum=[0.25, 0.75],
            ...     )
            >>> i_rand
            UGenArray({3})

        returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
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
        Gets `maximum` input of IRand.

        ::

            >>> i_rand = supriya.ugens.IRand.ir(
            ...     minimum=0,
            ...     maximum=127,
            ...     )
            >>> i_rand.maximum
            127.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        """
        Gets `minimum` input of IRand.

        ::

            >>> i_rand = supriya.ugens.IRand.ir(
            ...     minimum=0,
            ...     maximum=127,
            ...     )
            >>> i_rand.minimum
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]
