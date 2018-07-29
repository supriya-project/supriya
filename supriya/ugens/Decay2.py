from supriya.ugens.Filter import Filter


class Decay2(Filter):
    """
    A leaky signal integrator.

    ::

        >>> source = supriya.ugens.Impulse.ar()
        >>> decay_2 = supriya.ugens.Decay2.ar(
        ...     source=source,
        ...     )
        >>> decay_2
        Decay2.ar()

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'attack_time',
        'decay_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        attack_time=0.01,
        decay_time=1.0,
        calculation_rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            attack_time=attack_time,
            decay_time=decay_time,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        attack_time=0.01,
        decay_time=1.0,
        source=None,
        ):
        """
        Constructs an audio-rate leaky signal integrator.

        ::

            >>> source = supriya.ugens.Impulse.ar(frequency=[100, 101])
            >>> decay_2 = supriya.ugens.Decay2.ar(
            ...     source=source,
            ...     )
            >>> decay_2
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            attack_time=attack_time,
            decay_time=decay_time,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        attack_time=0.01,
        decay_time=1.0,
        source=None,
        ):
        """
        Constructs a control-rate leaky signal integrator.

        ::

            >>> source = supriya.ugens.Impulse.kr(frequency=[100, 101])
            >>> decay_2 = supriya.ugens.Decay2.kr(
            ...     source=source,
            ...     )
            >>> decay_2
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            attack_time=attack_time,
            decay_time=decay_time,
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def attack_time(self):
        """
        Gets `attack_time` input of Decay2.

        ::

            >>> attack_time = 0.5
            >>> decay_time = 0.25
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> decay_2 = supriya.ugens.Decay2.ar(
            ...     attack_time=attack_time,
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> decay_2.attack_time
            0.5

        Returns input.
        """
        index = self._ordered_input_names.index('attack_time')
        return self._inputs[index]

    @property
    def decay_time(self):
        """
        Gets `decay_time` input of Decay2.

        ::

            >>> attack_time = 0.5
            >>> decay_time = 0.25
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> decay_2 = supriya.ugens.Decay2.ar(
            ...     attack_time=attack_time,
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> decay_2.decay_time
            0.25

        Returns input.
        """
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Decay2.

        ::

            >>> attack_time = 0.5
            >>> decay_time = 0.25
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> decay_2 = supriya.ugens.Decay2.ar(
            ...     attack_time=attack_time,
            ...     decay_time=decay_time,
            ...     source=source,
            ...     )
            >>> decay_2.source
            In.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
