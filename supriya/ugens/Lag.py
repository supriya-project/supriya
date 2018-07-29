from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class Lag(Filter):
    """
    A lag generator.

    ::

        >>> source = supriya.ugens.In.kr(bus=0)
        >>> supriya.ugens.Lag.kr(
        ...     lag_time=0.5,
        ...     source=source,
        ...     )
        Lag.kr()

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
        lag_time=0.1,
        calculation_rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            lag_time=lag_time,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(
        cls,
        lag_time=None,
        calculation_rate=None,
        source=None,
        ):
        if lag_time == 0:
            return source
        source_rate = CalculationRate.from_expr(source)
        if source_rate == CalculationRate.SCALAR:
            return source
        ugen = cls(
            lag_time=lag_time,
            calculation_rate=calculation_rate,
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
        """
        Constructs an audio-rate lag.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> supriya.ugens.Lag.ar(
            ...     lag_time=0.5,
            ...     source=source,
            ...     )
            Lag.ar()

        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            lag_time=lag_time,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        lag_time=0.1,
        source=None,
        ):
        """
        Constructs a control-rate lag.

        ::

            >>> source = supriya.ugens.In.kr(bus=0)
            >>> supriya.ugens.Lag.kr(
            ...     lag_time=0.5,
            ...     source=source,
            ...     )
            Lag.kr()

        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            lag_time=lag_time,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def lag_time(self):
        """
        Gets `lag_time` input of Lag.

        ::

            >>> lag_time = 0.1
            >>> source = supriya.ugens.In.kr(bus=0)
            >>> lag = supriya.ugens.Lag.kr(
            ...     lag_time=lag_time,
            ...     source=source,
            ...     )
            >>> lag.lag_time
            0.1

        Returns input.
        """
        index = self._ordered_input_names.index('lag_time')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Lag.

        ::

            >>> source = supriya.ugens.In.kr(bus=0)
            >>> lag = supriya.ugens.Lag.kr(
            ...     source=source,
            ...     )
            >>> lag.source
            In.kr()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
