# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Peak import Peak


class RunningMin(Peak):
    r'''

    ::

        >>> running_min = ugentools.RunningMin.(
        ...     source=None,
        ...     trigger=0,
        ...     )
        >>> running_min

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
        r'''Constructs an audio-rate RunningMin.

        ::

            >>> running_min = ugentools.RunningMin.ar(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> running_min

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
        r'''Constructs a control-rate RunningMin.

        ::

            >>> running_min = ugentools.RunningMin.kr(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> running_min

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
        r'''Gets `source` input of RunningMin.

        ::

            >>> running_min = ugentools.RunningMin.ar(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> running_min.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of RunningMin.

        ::

            >>> running_min = ugentools.RunningMin.ar(
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> running_min.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]