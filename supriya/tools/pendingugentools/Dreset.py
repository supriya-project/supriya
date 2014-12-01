# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dreset(DUGen):
    r'''

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> dreset = ugentools.Dreset.ar(
        ...     reset=0,
        ...     source=source,
        ...     )
        >>> dreset
        Dreset.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'reset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        reset=0,
        source=None,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            reset=reset,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        reset=0,
        source=None,
        ):
        r'''Constructs a Dreset.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> dreset = ugentools.Dreset.new(
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> dreset
            Dreset.new()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            reset=reset,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def reset(self):
        r'''Gets `reset` input of Dreset.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> dreset = ugentools.Dreset.ar(
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> dreset.reset
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('reset')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Dreset.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> dreset = ugentools.Dreset.ar(
            ...     reset=0,
            ...     source=source,
            ...     )
            >>> dreset.source
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