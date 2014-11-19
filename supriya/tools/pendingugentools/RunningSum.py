# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class RunningSum(UGen):
    r'''

    ::

        >>> running_sum = ugentools.RunningSum.(
        ...     numsamp=40,
        ...     source=None,
        ...     )
        >>> running_sum

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'numsamp',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        numsamp=40,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            numsamp=numsamp,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        numsamp=40,
        source=None,
        ):
        r'''Constructs an audio-rate RunningSum.

        ::

            >>> running_sum = ugentools.RunningSum.ar(
            ...     numsamp=40,
            ...     source=None,
            ...     )
            >>> running_sum

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            numsamp=numsamp,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        numsamp=40,
        source=None,
        ):
        r'''Constructs a control-rate RunningSum.

        ::

            >>> running_sum = ugentools.RunningSum.kr(
            ...     numsamp=40,
            ...     source=None,
            ...     )
            >>> running_sum

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            numsamp=numsamp,
            source=source,
            )
        return ugen

    # def rms(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of RunningSum.

        ::

            >>> running_sum = ugentools.RunningSum.ar(
            ...     numsamp=40,
            ...     source=None,
            ...     )
            >>> running_sum.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def numsamp(self):
        r'''Gets `numsamp` input of RunningSum.

        ::

            >>> running_sum = ugentools.RunningSum.ar(
            ...     numsamp=40,
            ...     source=None,
            ...     )
            >>> running_sum.numsamp

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('numsamp')
        return self._inputs[index]