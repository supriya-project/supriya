from supriya.tools.ugentools.AbstractIn import AbstractIn


class InTrig(AbstractIn):
    """

    ::

        >>> in_trig = ugentools.InTrig.ar(
        ...     bus=0,
        ...     channel_count=1,
        ...     )
        >>> in_trig
        InTrig.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        'channel_count',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        channel_count=1,
        ):
        AbstractIn.__init__(
            self,
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            )

    ### PUBLIC METHODS ###

    # def isInputUGen(): ...

    @classmethod
    def kr(
        cls,
        bus=0,
        channel_count=1,
        ):
        """
        Constructs a control-rate InTrig.

        ::

            >>> in_trig = ugentools.InTrig.kr(
            ...     bus=0,
            ...     channel_count=1,
            ...     )
            >>> in_trig
            InTrig.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        """
        Gets `bus` input of InTrig.

        ::

            >>> in_trig = ugentools.InTrig.ar(
            ...     bus=0,
            ...     channel_count=1,
            ...     )
            >>> in_trig.bus
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def channel_count(self):
        """
        Gets `channel_count` input of InTrig.

        ::

            >>> in_trig = ugentools.InTrig.ar(
            ...     bus=0,
            ...     channel_count=1,
            ...     )
            >>> in_trig.channel_count
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]
