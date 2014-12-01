# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Lag import Lag


class Ramp(Lag):
    r'''Breaks a continuous signal into line segments.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> ramp = ugentools.Ramp.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ...     )
        >>> ramp
        Ramp.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'lag_time',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        lag_time=0.1,
        source=None,
        ):
        Lag.__init__(
            self,
            calculation_rate=calculation_rate,
            lag_time=lag_time,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        lag_time=0.1,
        source=None,
        ):
        r'''Constructs an audio-rate Ramp.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ramp = ugentools.Ramp.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> ramp
            Ramp.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            lag_time=lag_time,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        lag_time=0.1,
        source=None,
        ):
        r'''Constructs a control-rate Ramp.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ramp = ugentools.Ramp.kr(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> ramp
            Ramp.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            lag_time=lag_time,
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
    def lag_time(self):
        r'''Gets `lag_time` input of Ramp.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ramp = ugentools.Ramp.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> ramp.lag_time
            0.1

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lag_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Ramp.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ramp = ugentools.Ramp.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> ramp.source
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