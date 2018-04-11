from supriya.ugens.MultiOutUGen import MultiOutUGen


class Splay(MultiOutUGen):
    # TODO: This is actually a pseudo ugen.
    """
    A stereo field spreader.

    ::

        >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
        >>> splay = supriya.ugens.Splay.ar(
        ...     center=0,
        ...     source=source,
        ...     level=1,
        ...     level_comp=True,
        ...     spread=1,
        ...     )
        >>> splay
        UGenArray({2})

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'spread',
        'level',
        'center',
        'level_comp',
        'source',
        )

    _unexpanded_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        center=0,
        source=None,
        level=1,
        level_comp=True,
        spread=1,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            center=center,
            channel_count=2,
            source=source,
            level=level,
            level_comp=level_comp,
            spread=spread,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_single(
        cls,
        calculation_rate=None,
        center=0,
        source=None,
        level=1,
        level_comp=True,
        spread=1,
        ):
        ugen = cls(
            **kwargs
            )
        return ugen

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        center=0,
        source=None,
        level=1,
        level_comp=True,
        spread=1,
        ):
        """
        Constructs an audio-rate Splay.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> splay = supriya.ugens.Splay.ar(
            ...     center=0,
            ...     source=source,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay
            Splay.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            center=center,
            source=source,
            level=level,
            level_comp=level_comp,
            spread=spread,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        center=0,
        source=None,
        level=1,
        level_comp=True,
        spread=1,
        ):
        """
        Constructs a control-rate Splay.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> splay = supriya.ugens.Splay.kr(
            ...     center=0,
            ...     source=source,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay
            Splay.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            center=center,
            source=source,
            level=level,
            level_comp=level_comp,
            spread=spread,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def center(self):
        """
        Gets `center` input of Splay.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> splay = supriya.ugens.Splay.ar(
            ...     center=0,
            ...     source=source,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay.center
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('center')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Splay.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> splay = supriya.ugens.Splay.ar(
            ...     center=0,
            ...     source=source,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay.source

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def level(self):
        """
        Gets `level` input of Splay.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> splay = supriya.ugens.Splay.ar(
            ...     center=0,
            ...     source=source,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay.level
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def level_comp(self):
        """
        Gets `level_comp` input of Splay.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> splay = supriya.ugens.Splay.ar(
            ...     center=0,
            ...     source=source,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay.level_comp
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('level_comp')
        return self._inputs[index]

    @property
    def spread(self):
        """
        Gets `spread` input of Splay.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> splay = supriya.ugens.Splay.ar(
            ...     center=0,
            ...     source=source,
            ...     level=1,
            ...     level_comp=True,
            ...     spread=1,
            ...     )
            >>> splay.spread
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('spread')
        return self._inputs[index]
