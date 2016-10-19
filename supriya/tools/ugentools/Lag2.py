# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.CalculationRate import CalculationRate
from supriya.tools.ugentools.Filter import Filter


class Lag2(Filter):
    r"""
    An exponential lag generator.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> lag_2 = ugentools.Lag2.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ...     )
        >>> lag_2
        Lag2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'lag_time',
        )

    _valid_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
        )


    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        lag_time=0.1,
        source=None,
        ):
        Filter.__init__(
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
        r"""
        Constructs an audio-rate Lag2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> lag_2 = ugentools.Lag2.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_2
            Lag2.ar()

        Returns ugen graph.
        """
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
        r"""
        Constructs a control-rate Lag2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> lag_2 = ugentools.Lag2.kr(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_2
            Lag2.kr()

        Returns ugen graph.
        """
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
        r"""
        Gets `lag_time` input of Lag2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> lag_2 = ugentools.Lag2.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_2.lag_time
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('lag_time')
        return self._inputs[index]

    @property
    def source(self):
        r"""
        Gets `source` input of Lag2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> lag_2 = ugentools.Lag2.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_2.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
