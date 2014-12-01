# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.LPZ2 import LPZ2


class BRZ2(LPZ2):
    r'''A two zero fixed midcut filter.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> brz_2 = ugentools.BRZ2.ar(
        ...     source=source,
        ...     )
        >>> brz_2
        BRZ2.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

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
        LPZ2.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        r'''Constructs an audio-rate BRZ2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> brz_2 = ugentools.BRZ2.ar(
            ...     source=source,
            ...     )
            >>> brz_2
            BRZ2.ar()

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
        source=None,
        ):
        r'''Constructs a control-rate BRZ2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> brz_2 = ugentools.BRZ2.kr(
            ...     source=source,
            ...     )
            >>> brz_2
            BRZ2.kr()

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
        r'''Gets `source` input of BRZ2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> brz_2 = ugentools.BRZ2.ar(
            ...     source=source,
            ...     )
            >>> brz_2.source
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