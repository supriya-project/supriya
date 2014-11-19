# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Median(Filter):
    r'''

    ::

        >>> median = ugentools.Median.(
        ...     length=3,
        ...     source=None,
        ...     )
        >>> median

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'length',
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        length=3,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            length=length,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        length=3,
        source=None,
        ):
        r'''Constructs an audio-rate Median.

        ::

            >>> median = ugentools.Median.ar(
            ...     length=3,
            ...     source=None,
            ...     )
            >>> median

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            length=length,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        length=3,
        source=None,
        ):
        r'''Constructs a control-rate Median.

        ::

            >>> median = ugentools.Median.kr(
            ...     length=3,
            ...     source=None,
            ...     )
            >>> median

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            length=length,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def length(self):
        r'''Gets `length` input of Median.

        ::

            >>> median = ugentools.Median.ar(
            ...     length=3,
            ...     source=None,
            ...     )
            >>> median.length

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Median.

        ::

            >>> median = ugentools.Median.ar(
            ...     length=3,
            ...     source=None,
            ...     )
            >>> median.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]