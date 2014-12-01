# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Donce(DUGen):
    r'''

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> donce = ugentools.Donce.ar(
        ...     source=source,
        ...     )
        >>> donce
        Donce.ar()

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
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        source=None,
        ):
        r'''Constructs a Donce.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> donce = ugentools.Donce.new(
            ...     source=source,
            ...     )
            >>> donce
            Donce.new()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of Donce.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> donce = ugentools.Donce.ar(
            ...     source=source,
            ...     )
            >>> donce.source
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