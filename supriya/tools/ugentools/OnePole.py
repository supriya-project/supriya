from supriya.tools.ugentools.Filter import Filter


class OnePole(Filter):
    """
    A one pole filter.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> one_pole = ugentools.OnePole.ar(
        ...     coefficient=0.5,
        ...     source=source,
        ...     )
        >>> one_pole
        OnePole.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'coefficient',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        coefficient=0.5,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            coefficient=coefficient,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        coefficient=0.5,
        source=None,
        ):
        """
        Constructs an audio-rate OnePole.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> one_pole = ugentools.OnePole.ar(
            ...     coefficient=0.5,
            ...     source=source,
            ...     )
            >>> one_pole
            OnePole.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coefficient=coefficient,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        coefficient=0.5,
        source=None,
        ):
        """
        Constructs a control-rate OnePole.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> one_pole = ugentools.OnePole.kr(
            ...     coefficient=0.5,
            ...     source=source,
            ...     )
            >>> one_pole
            OnePole.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            coefficient=coefficient,
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
    def coefficient(self):
        """
        Gets `coefficient` input of OnePole.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> one_pole = ugentools.OnePole.ar(
            ...     coefficient=0.5,
            ...     source=source,
            ...     )
            >>> one_pole.coefficient
            0.5

        Returns ugen input.
        """
        index = self._ordered_input_names.index('coefficient')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of OnePole.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> one_pole = ugentools.OnePole.ar(
            ...     coefficient=0.5,
            ...     source=source,
            ...     )
            >>> one_pole.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
