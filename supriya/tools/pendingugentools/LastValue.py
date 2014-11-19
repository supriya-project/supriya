# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class LastValue(UGen):
    r'''

    ::

        >>> last_value = ugentools.LastValue.(
        ...     diff=0.01,
        ...     source=None,
        ...     )
        >>> last_value

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'diff',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        diff=0.01,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            diff=diff,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        diff=0.01,
        source=None,
        ):
        r'''Constructs an audio-rate LastValue.

        ::

            >>> last_value = ugentools.LastValue.ar(
            ...     diff=0.01,
            ...     source=None,
            ...     )
            >>> last_value

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            diff=diff,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        diff=0.01,
        source=None,
        ):
        r'''Constructs a control-rate LastValue.

        ::

            >>> last_value = ugentools.LastValue.kr(
            ...     diff=0.01,
            ...     source=None,
            ...     )
            >>> last_value

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            diff=diff,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def diff(self):
        r'''Gets `diff` input of LastValue.

        ::

            >>> last_value = ugentools.LastValue.ar(
            ...     diff=0.01,
            ...     source=None,
            ...     )
            >>> last_value.diff

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('diff')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of LastValue.

        ::

            >>> last_value = ugentools.LastValue.ar(
            ...     diff=0.01,
            ...     source=None,
            ...     )
            >>> last_value.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]