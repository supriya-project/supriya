# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class Rand(UGen):
    r"""
    A uniform random distribution.

    ::

        >>> ugentools.Rand.ir()
        Rand.ir()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'minimum',
        'maximum',
        )

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
        minimum=0.,
        maximum=1.,
        ):
        r"""
        Constructs a scalar-rate uniform random distribution.

        ::

            >>> ugentools.Rand.ir(
            ...     minimum=0.,
            ...     maximum=1.,
            ...     )
            Rand.ir()

        Returns unit generator graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            minimum=minimum,
            maximum=maximum,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        r"""
        Gets `maximum` input of Rand.

        ::

            >>> maximum = 500
            >>> minimum = 23
            >>> rand = ugentools.Rand.ir(
            ...     maximum=maximum,
            ...     minimum=minimum,
            ...     )
            >>> rand.maximum
            500.0

        Returns input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        r"""
        Gets `minimum` input of Rand.

        ::

            >>> maximum = 500
            >>> minimum = 23
            >>> rand = ugentools.Rand.ir(
            ...     maximum=maximum,
            ...     minimum=minimum,
            ...     )
            >>> rand.minimum
            23.0

        Returns input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]
