# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Lag import Lag


class Lag2(Lag):
    r'''

    ::

        >>> lag_2 = ugentools.Lag2.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ...     )
        >>> lag_2
        Lag2.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

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
        source=source,
        ):
        r'''Constructs an audio-rate Lag2.

        ::

            >>> lag_2 = ugentools.Lag2.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_2
            Lag2.ar()

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
        source=source,
        ):
        r'''Constructs a control-rate Lag2.

        ::

            >>> lag_2 = ugentools.Lag2.kr(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_2
            Lag2.kr()

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
        r'''Gets `lag_time` input of Lag2.

        ::

            >>> lag_2 = ugentools.Lag2.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_2.lag_time
            0.1

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('lag_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Lag2.

        ::

            >>> lag_2 = ugentools.Lag2.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_2.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]