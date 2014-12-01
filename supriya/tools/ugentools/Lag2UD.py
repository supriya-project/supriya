# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.Filter import Filter


class Lag2UD(Filter):
    r'''An up/down exponential lag generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> lag_2_ud = ugentools.Lag2UD.ar(
        ...     lag_time_d=0.1,
        ...     lag_time_u=0.1,
        ...     source=source,
        ...     )
        >>> lag_2_ud
        Lag2UD.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'lag_time_u',
        'lag_time_d',
        )

    _valid_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        lag_time_d=0.1,
        lag_time_u=0.1,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            lag_time_d=lag_time_d,
            lag_time_u=lag_time_u,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        lag_time_d=0.1,
        lag_time_u=0.1,
        source=None,
        ):
        r'''Constructs an audio-rate Lag2UD.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> lag_2_ud = ugentools.Lag2UD.ar(
            ...     lag_time_d=0.1,
            ...     lag_time_u=0.1,
            ...     source=source,
            ...     )
            >>> lag_2_ud
            Lag2UD.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            lag_time_d=lag_time_d,
            lag_time_u=lag_time_u,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        lag_time_d=0.1,
        lag_time_u=0.1,
        source=None,
        ):
        r'''Constructs a control-rate Lag2UD.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> lag_2_ud = ugentools.Lag2UD.kr(
            ...     lag_time_d=0.1,
            ...     lag_time_u=0.1,
            ...     source=source,
            ...     )
            >>> lag_2_ud
            Lag2UD.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            lag_time_d=lag_time_d,
            lag_time_u=lag_time_u,
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
    def lag_time_d(self):
        r'''Gets `lag_time_d` input of Lag2UD.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> lag_2_ud = ugentools.Lag2UD.ar(
            ...     lag_time_d=0.1,
            ...     lag_time_u=0.1,
            ...     source=source,
            ...     )
            >>> lag_2_ud.lag_time_d
            0.1

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lag_time_d')
        return self._inputs[index]

    @property
    def lag_time_u(self):
        r'''Gets `lag_time_u` input of Lag2UD.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> lag_2_ud = ugentools.Lag2UD.ar(
            ...     lag_time_d=0.1,
            ...     lag_time_u=0.1,
            ...     source=source,
            ...     )
            >>> lag_2_ud.lag_time_u
            0.1

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lag_time_u')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Lag2UD.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> lag_2_ud = ugentools.Lag2UD.ar(
            ...     lag_time_d=0.1,
            ...     lag_time_u=0.1,
            ...     source=source,
            ...     )
            >>> lag_2_ud.source
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