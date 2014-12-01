# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class LPZ1(Filter):
    r'''

    ::

        >>> source = ugentools.In.ar(0)
        >>> lpz_1 = ugentools.LPZ1.ar(
        ...     source=source,
        ...     )
        >>> lpz_1
        LPZ1.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=source,
        ):
        r'''Constructs an audio-rate LPZ1.

        ::

            >>> source = ugentools.In.ar(0)
            >>> lpz_1 = ugentools.LPZ1.ar(
            ...     source=source,
            ...     )
            >>> lpz_1
            LPZ1.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        source=source,
        ):
        r'''Constructs a control-rate LPZ1.

        ::

            >>> source = ugentools.In.ar(0)
            >>> lpz_1 = ugentools.LPZ1.kr(
            ...     source=source,
            ...     )
            >>> lpz_1
            LPZ1.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
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
    def source(self):
        r'''Gets `source` input of LPZ1.

        ::

            >>> source = ugentools.In.ar(0)
            >>> lpz_1 = ugentools.LPZ1.ar(
            ...     source=source,
            ...     )
            >>> lpz_1.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]