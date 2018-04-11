from supriya.ugens.UGen import UGen


class Spring(UGen):
    """
    A resonating spring physical model.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> spring = supriya.ugens.Spring.ar(
        ...     damping=0,
        ...     source=source,
        ...     spring=1,
        ...     )
        >>> spring
        Spring.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Physical Modelling UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'spring',
        'damping',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        damping=0,
        source=None,
        spring=1,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damping=damping,
            source=source,
            spring=spring,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damping=0,
        source=None,
        spring=1,
        ):
        """
        Constructs an audio-rate Spring.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> spring = supriya.ugens.Spring.ar(
            ...     damping=0,
            ...     source=source,
            ...     spring=1,
            ...     )
            >>> spring
            Spring.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damping=damping,
            source=source,
            spring=spring,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        damping=0,
        source=None,
        spring=1,
        ):
        """
        Constructs a control-rate Spring.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> spring = supriya.ugens.Spring.kr(
            ...     damping=0,
            ...     source=source,
            ...     spring=1,
            ...     )
            >>> spring
            Spring.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damping=damping,
            source=source,
            spring=spring,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def damping(self):
        """
        Gets `damping` input of Spring.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> spring = supriya.ugens.Spring.ar(
            ...     damping=0,
            ...     source=source,
            ...     spring=1,
            ...     )
            >>> spring.damping
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('damping')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Spring.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> spring = supriya.ugens.Spring.ar(
            ...     damping=0,
            ...     source=source,
            ...     spring=1,
            ...     )
            >>> spring.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def spring(self):
        """
        Gets `spring` input of Spring.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> spring = supriya.ugens.Spring.ar(
            ...     damping=0,
            ...     source=source,
            ...     spring=1,
            ...     )
            >>> spring.spring
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('spring')
        return self._inputs[index]
