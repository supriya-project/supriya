# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Peak import Peak


class RunningMax(Peak):
    r'''

    ::

        >>> running_max = ugentools.RunningMax.(
        ...     source=None,
        ...     trigger=0,
        ...     )
        >>> running_max

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
        Peak.__init__(
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
        r'''Constructs an audio-rate RunningMax.

        ::

            >>> running_max = ugentools.RunningMax.ar(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> running_max

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
        r'''Constructs a control-rate RunningMax.

        ::

            >>> running_max = ugentools.RunningMax.kr(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> running_max

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
        r'''Gets `source` input of RunningMax.

        ::

            >>> running_max = ugentools.RunningMax.ar(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> running_max.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of RunningMax.

        ::

            >>> running_max = ugentools.RunningMax.ar(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> running_max.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]