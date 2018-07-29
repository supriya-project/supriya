from supriya.ugens.WidthFirstUGen import WidthFirstUGen


class RandSeed(WidthFirstUGen):
    """
    Sets the synth's random generator seed.

    ::

        >>> trigger = supriya.ugens.Impulse.ar()
        >>> rand_seed = supriya.ugens.RandSeed.ar(
        ...     seed=1,
        ...     trigger=trigger,
        ...     )
        >>> rand_seed
        RandSeed.ar()

    """
    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'trigger',
        'seed',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        seed=56789,
        trigger=0,
        ):
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            seed=seed,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        seed=56789,
        trigger=0,
        ):
        """
        Constructs an audio-rate RandSeed.

        ::

            >>> trigger = supriya.ugens.Impulse.ar()
            >>> rand_seed = supriya.ugens.RandSeed.ar(
            ...     seed=1,
            ...     trigger=trigger,
            ...     )
            >>> rand_seed
            RandSeed.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            seed=seed,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def ir(
        cls,
        seed=56789,
        trigger=0,
        ):
        """
        Constructs a scalar-rate RandSeed.

        ::

            >>> rand_seed = supriya.ugens.RandSeed.ir(
            ...     seed=1,
            ...     )
            >>> rand_seed
            RandSeed.ir()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            seed=seed,
            trigger=trigger,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        seed=56789,
        trigger=0,
        ):
        """
        Constructs a control-rate RandSeed.

        ::

            >>> trigger = supriya.ugens.Impulse.kr()
            >>> rand_seed = supriya.ugens.RandSeed.kr(
            ...     seed=1,
            ...     trigger=trigger,
            ...     )
            >>> rand_seed
            RandSeed.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            seed=seed,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def seed(self):
        """
        Gets `seed` input of RandSeed.

        ::

            >>> trigger = supriya.ugens.Impulse.ar()
            >>> rand_seed = supriya.ugens.RandSeed.ar(
            ...     seed=1,
            ...     trigger=trigger,
            ...     )
            >>> rand_seed.seed
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('seed')
        return self._inputs[index]

    @property
    def trigger(self):
        """
        Gets `trigger` input of RandSeed.

        ::

            >>> trigger = supriya.ugens.Impulse.ar()
            >>> rand_seed = supriya.ugens.RandSeed.ar(
            ...     seed=1,
            ...     trigger=trigger,
            ...     )
            >>> rand_seed.trigger
            Impulse.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]
