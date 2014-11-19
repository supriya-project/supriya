# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Latch(UGen):
    r'''

    ::

        >>> latch = ugentools.Latch.(
        ...     source=None,
        ...     trigger=0,
        ...     )
        >>> latch

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        trigger=0,
        ):
        r'''Constructs an audio-rate Latch.

        ::

            >>> latch = ugentools.Latch.ar(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> latch

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        source=None,
        trigger=0,
        ):
        r'''Constructs a control-rate Latch.

        ::

            >>> latch = ugentools.Latch.kr(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> latch

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of Latch.

        ::

            >>> latch = ugentools.Latch.ar(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> latch.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of Latch.

        ::

            >>> latch = ugentools.Latch.ar(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> latch.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]