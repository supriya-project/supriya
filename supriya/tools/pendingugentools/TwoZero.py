# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.TwoPole import TwoPole


class TwoZero(TwoPole):
    r'''

    ::

        >>> two_zero = ugentools.TwoZero.(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=None,
        ...     )
        >>> two_zero

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'radius',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=440,
        radius=0.8,
        source=None,
        ):
        TwoPole.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            radius=radius,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=440,
        radius=0.8,
        source=None,
        ):
        r'''Constructs an audio-rate TwoZero.

        ::

            >>> two_zero = ugentools.TwoZero.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=None,
            ...     )
            >>> two_zero

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            radius=radius,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        frequency=440,
        radius=0.8,
        source=None,
        ):
        r'''Constructs a control-rate TwoZero.

        ::

            >>> two_zero = ugentools.TwoZero.kr(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=None,
            ...     )
            >>> two_zero

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            radius=radius,
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
        r'''Gets `source` input of TwoZero.

        ::

            >>> two_zero = ugentools.TwoZero.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=None,
            ...     )
            >>> two_zero.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of TwoZero.

        ::

            >>> two_zero = ugentools.TwoZero.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=None,
            ...     )
            >>> two_zero.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def radius(self):
        r'''Gets `radius` input of TwoZero.

        ::

            >>> two_zero = ugentools.TwoZero.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=None,
            ...     )
            >>> two_zero.radius

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('radius')
        return self._inputs[index]