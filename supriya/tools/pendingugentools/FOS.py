# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class FOS(Filter):
    r'''

    ::

        >>> fos = ugentools.FOS.ar(
        ...     a_0=0,
        ...     a_1=0,
        ...     b_1=0,
        ...     source=source,
        ...     )
        >>> fos
        FOS.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'a_0',
        'a_1',
        'b_1',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        a_0=0,
        a_1=0,
        b_1=0,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            a_0=a_0,
            a_1=a_1,
            b_1=b_1,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a_0=0,
        a_1=0,
        b_1=0,
        source=None,
        ):
        r'''Constructs an audio-rate FOS.

        ::

            >>> fos = ugentools.FOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     b_1=0,
            ...     source=source,
            ...     )
            >>> fos
            FOS.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a_0=a_0,
            a_1=a_1,
            b_1=b_1,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        a_0=0,
        a_1=0,
        b_1=0,
        source=None,
        ):
        r'''Constructs a control-rate FOS.

        ::

            >>> fos = ugentools.FOS.kr(
            ...     a_0=0,
            ...     a_1=0,
            ...     b_1=0,
            ...     source=source,
            ...     )
            >>> fos
            FOS.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a_0=a_0,
            a_1=a_1,
            b_1=b_1,
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
    def a_0(self):
        r'''Gets `a_0` input of FOS.

        ::

            >>> fos = ugentools.FOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     b_1=0,
            ...     source=source,
            ...     )
            >>> fos.a_0
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('a_0')
        return self._inputs[index]

    @property
    def a_1(self):
        r'''Gets `a_1` input of FOS.

        ::

            >>> fos = ugentools.FOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     b_1=0,
            ...     source=source,
            ...     )
            >>> fos.a_1
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('a_1')
        return self._inputs[index]

    @property
    def b_1(self):
        r'''Gets `b_1` input of FOS.

        ::

            >>> fos = ugentools.FOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     b_1=0,
            ...     source=source,
            ...     )
            >>> fos.b_1
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('b_1')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of FOS.

        ::

            >>> fos = ugentools.FOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     b_1=0,
            ...     source=source,
            ...     )
            >>> fos.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]