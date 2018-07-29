from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Lag3(Filter):
    """
    An exponential lag generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> lag_3 = supriya.ugens.Lag3.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ...     )
        >>> lag_3
        Lag3.ar()

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
        """
        Constructs an audio-rate Lag3.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> lag_3 = supriya.ugens.Lag3.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_3
            Lag3.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
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
        """
        Constructs a control-rate Lag3.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> lag_3 = supriya.ugens.Lag3.kr(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_3
            Lag3.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
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
        """
        Gets `lag_time` input of Lag3.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> lag_3 = supriya.ugens.Lag3.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_3.lag_time
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('lag_time')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Lag3.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> lag_3 = supriya.ugens.Lag3.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> lag_3.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
