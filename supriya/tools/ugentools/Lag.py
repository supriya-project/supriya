# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Rate import Rate
from supriya.tools.ugentools.Filter import Filter


class Lag(Filter):
    r'''A lag unit generator.

    ::

        >>> source = ugentools.In.kr(bus=0)
        >>> ugentools.Lag.kr(
        ...     lag_time=0.5,
        ...     source=source,
        ...     )
        Lag.kr()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'lag_time',
        )

    _valid_rates = (
        Rate.AUDIO,
        Rate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        lag_time=0.1,
        rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            rate=rate,
            source=source,
            lag_time=lag_time,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(
        cls,
        lag_time=None,
        rate=None,
        source=None,
        ):
        if lag_time == 0:
            return source
        source_rate = Rate.from_input(source)
        if source_rate == Rate.SCALAR:
            return source
        ugen = cls(
            lag_time=lag_time,
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        lag_time=0.1,
        source=None,
        ):
        r'''Creates an audio-rate lag.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.Lag.ar(
            ...     lag_time=0.5,
            ...     source=source,
            ...     )
            Lag.ar()

        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            lag_time=lag_time,
            rate=rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        lag_time=0.1,
        source=None,
        ):
        r'''Creates a control-rate lag.

        ::

            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.Lag.kr(
            ...     lag_time=0.5,
            ...     source=source,
            ...     )
            Lag.kr()

        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            lag_time=lag_time,
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def lag_time(self):
        r'''Gets `lag_time` input of Lag.

        ::

            >>> lag_time = None
            >>> lag = ugentools.Lag.ar(
            ...     lag_time=lag_time,
            ...     )
            >>> lag.lag_time

        Returns input.
        '''
        index = self._ordered_input_names.index('lag_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Lag.

        ::

            >>> source = None
            >>> lag = ugentools.Lag.ar(
            ...     source=source,
            ...     )
            >>> lag.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]