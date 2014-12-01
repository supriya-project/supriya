# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class TwoPole(Filter):
    r'''A two pole filter.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> two_pole = ugentools.TwoPole.ar(
        ...     frequency=440,
        ...     radius=0.8,
        ...     source=source,
        ...     )
        >>> two_pole
        TwoPole.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

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

            >>> source = ugentools.In.ar(bus=0)
            >>> two_pole = ugentools.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_pole
            TwoPole.ar()

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

            >>> source = ugentools.In.ar(bus=0)
            >>> two_pole = ugentools.TwoPole.kr(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_pole
            TwoPole.kr()

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

            >>> source = ugentools.In.ar(bus=0)
            >>> two_pole = ugentools.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_pole.frequency
            440.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def radius(self):
        r'''Gets `radius` input of TwoPole.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> two_pole = ugentools.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_pole.radius
            0.8

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('radius')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of TwoPole.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> two_pole = ugentools.TwoPole.ar(
            ...     frequency=440,
            ...     radius=0.8,
            ...     source=source,
            ...     )
            >>> two_pole.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=<CalculationRate.AUDIO: 2>,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]