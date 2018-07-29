from supriya.ugens.Filter import Filter


class Formlet(Filter):
    """
    A FOF-like filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> formlet = supriya.ugens.Formlet.ar(
        ...     attack_time=1,
        ...     decay_time=1,
        ...     frequency=440,
        ...     source=source,
        ...     )
        >>> formlet
        Formlet.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'attack_time',
        'decay_time',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        attack_time=1,
        decay_time=1,
        frequency=440,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            attack_time=attack_time,
            decay_time=decay_time,
            frequency=frequency,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        attack_time=1,
        decay_time=1,
        frequency=440,
        source=None,
        ):
        """
        Constructs an audio-rate Formlet.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> formlet = supriya.ugens.Formlet.ar(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> formlet
            Formlet.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            attack_time=attack_time,
            decay_time=decay_time,
            frequency=frequency,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        attack_time=1,
        decay_time=1,
        frequency=440,
        source=None,
        ):
        """
        Constructs a control-rate Formlet.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> formlet = supriya.ugens.Formlet.kr(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> formlet
            Formlet.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            attack_time=attack_time,
            decay_time=decay_time,
            frequency=frequency,
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
    def attack_time(self):
        """
        Gets `attack_time` input of Formlet.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> formlet = supriya.ugens.Formlet.ar(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> formlet.attack_time
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('attack_time')
        return self._inputs[index]

    @property
    def decay_time(self):
        """
        Gets `decay_time` input of Formlet.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> formlet = supriya.ugens.Formlet.ar(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> formlet.decay_time
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of Formlet.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> formlet = supriya.ugens.Formlet.ar(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> formlet.frequency
            440.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Formlet.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> formlet = supriya.ugens.Formlet.ar(
            ...     attack_time=1,
            ...     decay_time=1,
            ...     frequency=440,
            ...     source=source,
            ...     )
            >>> formlet.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
