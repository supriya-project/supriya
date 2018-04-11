from supriya.tools.ugentools.UGen import UGen


class PulseDivider(UGen):
    """

    ::

        >>> pulse_divider = ugentools.PulseDivider.ar(
        ...     div=2,
        ...     start=0,
        ...     trigger=0,
        ...     )
        >>> pulse_divider
        PulseDivider.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'div',
        'start',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        div=2,
        start=0,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            div=div,
            start=start,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        div=2,
        start=0,
        trigger=0,
        ):
        """
        Constructs an audio-rate PulseDivider.

        ::

            >>> pulse_divider = ugentools.PulseDivider.ar(
            ...     div=2,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> pulse_divider
            PulseDivider.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            div=div,
            start=start,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        div=2,
        start=0,
        trigger=0,
        ):
        """
        Constructs a control-rate PulseDivider.

        ::

            >>> pulse_divider = ugentools.PulseDivider.kr(
            ...     div=2,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> pulse_divider
            PulseDivider.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            div=div,
            start=start,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def div(self):
        """
        Gets `div` input of PulseDivider.

        ::

            >>> pulse_divider = ugentools.PulseDivider.ar(
            ...     div=2,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> pulse_divider.div
            2.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('div')
        return self._inputs[index]

    @property
    def start(self):
        """
        Gets `start` input of PulseDivider.

        ::

            >>> pulse_divider = ugentools.PulseDivider.ar(
            ...     div=2,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> pulse_divider.start
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('start')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of PulseDivider.

        ::

            >>> pulse_divider = ugentools.PulseDivider.ar(
            ...     div=2,
            ...     start=0,
            ...     trigger=0,
            ...     )
            >>> pulse_divider.trigger
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
