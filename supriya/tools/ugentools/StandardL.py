# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class StandardL(UGen):
    """
    A linear-interpolating standard map chaotic generator.

    ::

        >>> standard_l = ugentools.StandardL.ar(
        ...     frequency=22050,
        ...     k=1,
        ...     xi=0.5,
        ...     yi=0,
        ...     )
        >>> standard_l
        StandardL.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Chaos UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'k',
        'xi',
        'yi',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=22050,
        k=1,
        xi=0.5,
        yi=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            k=k,
            xi=xi,
            yi=yi,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=22050,
        k=1,
        xi=0.5,
        yi=0,
        ):
        """
        Constructs an audio-rate StandardL.

        ::

            >>> standard_l = ugentools.StandardL.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_l
            StandardL.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            k=k,
            xi=xi,
            yi=yi,
            )
        return ugen

    # def equation(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of StandardL.

        ::

            >>> standard_l = ugentools.StandardL.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_l.frequency
            22050.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def k(self):
        """
        Gets `k` input of StandardL.

        ::

            >>> standard_l = ugentools.StandardL.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_l.k
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('k')
        return self._inputs[index]

    @property
    def xi(self):
        """
        Gets `xi` input of StandardL.

        ::

            >>> standard_l = ugentools.StandardL.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_l.xi
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('xi')
        return self._inputs[index]

    @property
    def yi(self):
        """
        Gets `yi` input of StandardL.

        ::

            >>> standard_l = ugentools.StandardL.ar(
            ...     frequency=22050,
            ...     k=1,
            ...     xi=0.5,
            ...     yi=0,
            ...     )
            >>> standard_l.yi
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('yi')
        return self._inputs[index]
