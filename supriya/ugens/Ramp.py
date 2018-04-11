from supriya.ugens.Lag import Lag


class Ramp(Lag):
    """
    Breaks a continuous signal into line segments.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> ramp = supriya.ugens.Ramp.ar(
        ...     lag_time=0.1,
        ...     source=source,
        ...     )
        >>> ramp
        Ramp.ar()

    """

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
        """
        Constructs an audio-rate Ramp.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> ramp = supriya.ugens.Ramp.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> ramp
            Ramp.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
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
        Constructs a control-rate Ramp.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> ramp = supriya.ugens.Ramp.kr(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> ramp
            Ramp.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
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
        Gets `lag_time` input of Ramp.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> ramp = supriya.ugens.Ramp.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> ramp.lag_time
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('lag_time')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Ramp.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> ramp = supriya.ugens.Ramp.ar(
            ...     lag_time=0.1,
            ...     source=source,
            ...     )
            >>> ramp.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
