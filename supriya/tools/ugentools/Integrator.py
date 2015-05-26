# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Integrator(Filter):
    r'''A leaky integrator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> integrator = ugentools.Integrator.ar(
        ...     coefficient=1,
        ...     source=source,
        ...     )
        >>> integrator
        Integrator.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'coefficient',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        coefficient=1,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            coefficient=coefficient,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        coefficient=1,
        source=None,
        ):
        r'''Constructs an audio-rate Integrator.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> integrator = ugentools.Integrator.ar(
            ...     coefficient=1,
            ...     source=source,
            ...     )
            >>> integrator
            Integrator.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coefficient=coefficient,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        coefficient=1,
        source=None,
        ):
        r'''Constructs a control-rate Integrator.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> integrator = ugentools.Integrator.kr(
            ...     coefficient=1,
            ...     source=source,
            ...     )
            >>> integrator
            Integrator.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coefficient=coefficient,
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
    def coefficient(self):
        r'''Gets `coefficient` input of Integrator.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> integrator = ugentools.Integrator.ar(
            ...     coefficient=1,
            ...     source=source,
            ...     )
            >>> integrator.coefficient
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('coefficient')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Integrator.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> integrator = ugentools.Integrator.ar(
            ...     coefficient=1,
            ...     source=source,
            ...     )
            >>> integrator.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]