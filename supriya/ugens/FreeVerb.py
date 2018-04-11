from supriya.ugens.UGen import UGen


class FreeVerb(UGen):
    """
    A FreeVerb reverb unit generator.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> supriya.ugens.FreeVerb.ar(
        ...     source=source,
        ...     )
        FreeVerb.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Reverb UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'mix',
        'room_size',
        'damping',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        damping=0.5,
        mix=0.33,
        room_size=0.5,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damping=damping,
            mix=mix,
            room_size=room_size,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damping=0.5,
        mix=0.33,
        room_size=0.5,
        source=None,
        ):
        """
        Constructs an audio-rate FreeVerb reverb unit.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> supriya.ugens.FreeVerb.ar(
            ...     damping=0.5,
            ...     mix=0.33,
            ...     room_size=0.5,
            ...     source=source,
            ...     )
            FreeVerb.ar()

        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            damping=damping,
            mix=mix,
            room_size=room_size,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def damping(self):
        """
        Gets `damping` input of FreeVerb.

        ::

            >>> damping = 0.5
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> free_verb = supriya.ugens.FreeVerb.ar(
            ...     damping=damping,
            ...     source=source,
            ...     )
            >>> free_verb.damping
            0.5

        Returns input.
        """
        index = self._ordered_input_names.index('damping')
        return self._inputs[index]

    @property
    def mix(self):
        """
        Gets `mix` input of FreeVerb.

        ::

            >>> mix = 0.33
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> free_verb = supriya.ugens.FreeVerb.ar(
            ...     mix=mix,
            ...     source=source,
            ...     )
            >>> free_verb.mix
            0.33

        Returns input.
        """
        index = self._ordered_input_names.index('mix')
        return self._inputs[index]

    @property
    def room_size(self):
        """
        Gets `room_size` input of FreeVerb.

        ::

            >>> room_size = 0.5
            >>> source = supriya.ugens.In.ar(bus=0)
            >>> free_verb = supriya.ugens.FreeVerb.ar(
            ...     room_size=room_size,
            ...     source=source,
            ...     )
            >>> free_verb.room_size
            0.5

        Returns input.
        """
        index = self._ordered_input_names.index('room_size')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of FreeVerb.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> free_verb = supriya.ugens.FreeVerb.ar(
            ...     source=source,
            ...     )
            >>> free_verb.source
            In.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
