# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Sweep(UGen):
    r'''

    ::

        >>> sweep = ugentools.Sweep.(
        ...     rate=1,
        ...     trigger=0,
        ...     )
        >>> sweep

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'rate',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        rate=1,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            rate=rate,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        rate=1,
        trigger=0,
        ):
        r'''Constructs an audio-rate Sweep.

        ::

            >>> sweep = ugentools.Sweep.ar(
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> sweep

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            rate=rate,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        rate=1,
        trigger=0,
        ):
        r'''Constructs a control-rate Sweep.

        ::

            >>> sweep = ugentools.Sweep.kr(
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> sweep

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            rate=rate,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def rate(self):
        r'''Gets `rate` input of Sweep.

        ::

            >>> sweep = ugentools.Sweep.ar(
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> sweep.rate

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('rate')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of Sweep.

        ::

            >>> sweep = ugentools.Sweep.ar(
            ...     rate=1,
            ...     trigger=0,
            ...     )
            >>> sweep.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]