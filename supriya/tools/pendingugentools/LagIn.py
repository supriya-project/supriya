from supriya.tools.ugentools.AbstractIn import AbstractIn


class LagIn(AbstractIn):
    """

    ::

        >>> lag_in = ugentools.LagIn.ar(
        ...     bus=0,
        ...     channel_count=1,
        ...     lag=0.1,
        ...     )
        >>> lag_in
        LagIn.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        'channel_count',
        'lag',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        channel_count=1,
        lag=0.1,
        ):
        AbstractIn.__init__(
            self,
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            lag=lag,
            )

    ### PUBLIC METHODS ###

    # def isInputUGen(): ...

    @classmethod
    def kr(
        cls,
        bus=0,
        channel_count=1,
        lag=0.1,
        ):
        """
        Constructs a control-rate LagIn.

        ::

            >>> lag_in = ugentools.LagIn.kr(
            ...     bus=0,
            ...     channel_count=1,
            ...     lag=0.1,
            ...     )
            >>> lag_in
            LagIn.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            lag=lag,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        """
        Gets `bus` input of LagIn.

        ::

            >>> lag_in = ugentools.LagIn.ar(
            ...     bus=0,
            ...     channel_count=1,
            ...     lag=0.1,
            ...     )
            >>> lag_in.bus
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def channel_count(self):
        """
        Gets `channel_count` input of LagIn.

        ::

            >>> lag_in = ugentools.LagIn.ar(
            ...     bus=0,
            ...     channel_count=1,
            ...     lag=0.1,
            ...     )
            >>> lag_in.channel_count
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]

    @property
    def lag(self):
        """
        Gets `lag` input of LagIn.

        ::

            >>> lag_in = ugentools.LagIn.ar(
            ...     bus=0,
            ...     channel_count=1,
            ...     lag=0.1,
            ...     )
            >>> lag_in.lag
            0.1

        Returns ugen input.
        """
        index = self._ordered_input_names.index('lag')
        return self._inputs[index]
