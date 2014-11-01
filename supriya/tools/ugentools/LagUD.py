# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Rate import Rate
from supriya.tools.ugentools.Filter import Filter


class LagUD(Filter):
    r'''An up/down lag unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.SinOsc.kr(frequency=1.0)
        >>> ugentools.LagUD.kr(
        ...     lag_time_down=1.25,
        ...     lag_time_up=0.5,
        ...     source=source,
        ...     )
        LagUD.kr()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'lag_time_up',
        'lag_time_down',
        )

    _valid_rates = (
        Rate.AUDIO,
        Rate.CONTROL,
        )

    ### INITIALIZER ###

    def __init__(
        self,
        lag_time_down=0.1,
        lag_time_up=0.1,
        rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            lag_time_down=lag_time_down,
            lag_time_up=lag_time_up,
            rate=rate,
            source=source,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(
        cls,
        lag_time_down=None,
        lag_time_up=None,
        rate=None,
        source=None,
        ):
        if lag_time_up == 0 and lag_time_down == 0:
            return source
        source_rate = Rate.from_input(source)
        if source_rate == Rate.SCALAR:
            return source
        ugen = cls(
            lag_time_down=lag_time_down,
            lag_time_up=lag_time_up,
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        lag_time_down=0.1,
        lag_time_up=0.1,
        source=None,
        ):
        r'''Creates a control-rate lag.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.In.ar(bus=0)
            >>> ugentools.LagUD.ar(
            ...     lag_time_down=1.25,
            ...     lag_time_up=0.5,
            ...     source=source,
            ...     )
            LagUD.ar()

        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            lag_time_down=lag_time_down,
            lag_time_up=lag_time_up,
            rate=rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        lag_time_down=0.1,
        lag_time_up=0.1,
        source=None,
        ):
        r'''Creates a control-rate lag.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.In.kr(bus=0)
            >>> ugentools.LagUD.kr(
            ...     lag_time_down=1.25,
            ...     lag_time_up=0.5,
            ...     source=source,
            ...     )
            LagUD.kr()

        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            lag_time_down=lag_time_down,
            lag_time_up=lag_time_up,
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def lag_time_down(self):
        r'''Gets `lag_time_down` input of LagUD.

        ::

            >>> lag_time_down = None
            >>> lag_ud = ugentools.LagUD.ar(
            ...     lag_time_down=lag_time_down,
            ...     )
            >>> lag_ud.lag_time_down

        Returns input.
        '''
        index = self._ordered_input_names.index('lag_time_down')
        return self._inputs[index]

    @property
    def lag_time_up(self):
        r'''Gets `lag_time_up` input of LagUD.

        ::

            >>> lag_time_up = None
            >>> lag_ud = ugentools.LagUD.ar(
            ...     lag_time_up=lag_time_up,
            ...     )
            >>> lag_ud.lag_time_up

        Returns input.
        '''
        index = self._ordered_input_names.index('lag_time_up')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of LagUD.

        ::

            >>> source = None
            >>> lag_ud = ugentools.LagUD.ar(
            ...     source=source,
            ...     )
            >>> lag_ud.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]