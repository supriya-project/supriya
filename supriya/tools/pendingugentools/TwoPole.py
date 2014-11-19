# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class TwoPole(Filter):
    r'''

    ::

        >>> two_pole = ugentools.TwoPole.(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=None,
        ...     )
        >>> two_pole

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
        Filter.__init__(
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
        r'''Constructs an audio-rate TwoPole.

        ::

            >>> two_pole = ugentools.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=None,
            ...     )
            >>> two_pole

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
        r'''Constructs a control-rate TwoPole.

        ::

            >>> two_pole = ugentools.TwoPole.kr(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=None,
            ...     )
            >>> two_pole

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
    def frequency(self):
        r'''Gets `frequency` input of TwoPole.

        ::

            >>> two_pole = ugentools.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=None,
            ...     )
            >>> two_pole.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def radius(self):
        r'''Gets `radius` input of TwoPole.

        ::

            >>> two_pole = ugentools.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=None,
            ...     )
            >>> two_pole.radius

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('radius')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of TwoPole.

        ::

            >>> two_pole = ugentools.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=None,
            ...     )
            >>> two_pole.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]