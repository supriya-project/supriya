from supriya.ugens.PureUGen import PureUGen


class AmpCompA(PureUGen):
    """
    Basic psychoacoustic amplitude compensation (ANSI A-weighting curve).

    ::

        >>> amp_comp_a = supriya.ugens.AmpCompA.ar(
        ...     frequency=1000,
        ...     min_amp=0.32,
        ...     root=0,
        ...     root_amp=1,
        ...     )
        >>> amp_comp_a
        AmpCompA.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Line Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'frequency',
        'root',
        'min_amp',
        'root_amp',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        frequency=1000,
        min_amp=0.32,
        root=0,
        root_amp=1,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            frequency=frequency,
            min_amp=min_amp,
            root=root,
            root_amp=root_amp,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        frequency=1000,
        min_amp=0.32,
        root=0,
        root_amp=1,
        ):
        """
        Constructs an audio-rate AmpCompA.

        ::

            >>> amp_comp_a = supriya.ugens.AmpCompA.ar(
            ...     frequency=1000,
            ...     min_amp=0.32,
            ...     root=0,
            ...     root_amp=1,
            ...     )
            >>> amp_comp_a
            AmpCompA.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            min_amp=min_amp,
            root=root,
            root_amp=root_amp,
            )
        return ugen

    @classmethod
    def ir(
        cls,
        frequency=1000,
        min_amp=0.32,
        root=0,
        root_amp=1,
        ):
        """
        Constructs a scale-rate AmpCompA.

        ::

            >>> amp_comp_a = supriya.ugens.AmpCompA.ir(
            ...     frequency=1000,
            ...     min_amp=0.32,
            ...     root=0,
            ...     root_amp=1,
            ...     )
            >>> amp_comp_a
            AmpCompA.ir()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            min_amp=min_amp,
            root=root,
            root_amp=root_amp,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        frequency=1000,
        min_amp=0.32,
        root=0,
        root_amp=1,
        ):
        """
        Constructs a control-rate AmpCompA.

        ::

            >>> amp_comp_a = supriya.ugens.AmpCompA.kr(
            ...     frequency=1000,
            ...     min_amp=0.32,
            ...     root=0,
            ...     root_amp=1,
            ...     )
            >>> amp_comp_a
            AmpCompA.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            frequency=frequency,
            min_amp=min_amp,
            root=root,
            root_amp=root_amp,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def frequency(self):
        """
        Gets `frequency` input of AmpCompA.

        ::

            >>> amp_comp_a = supriya.ugens.AmpCompA.ar(
            ...     frequency=1000,
            ...     min_amp=0.32,
            ...     root=0,
            ...     root_amp=1,
            ...     )
            >>> amp_comp_a.frequency
            1000.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def min_amp(self):
        """
        Gets `min_amp` input of AmpCompA.

        ::

            >>> amp_comp_a = supriya.ugens.AmpCompA.ar(
            ...     frequency=1000,
            ...     min_amp=0.32,
            ...     root=0,
            ...     root_amp=1,
            ...     )
            >>> amp_comp_a.min_amp
            0.32

        Returns ugen input.
        """
        index = self._ordered_input_names.index('min_amp')
        return self._inputs[index]

    @property
    def root(self):
        """
        Gets `root` input of AmpCompA.

        ::

            >>> amp_comp_a = supriya.ugens.AmpCompA.ar(
            ...     frequency=1000,
            ...     min_amp=0.32,
            ...     root=0,
            ...     root_amp=1,
            ...     )
            >>> amp_comp_a.root
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('root')
        return self._inputs[index]

    @property
    def root_amp(self):
        """
        Gets `root_amp` input of AmpCompA.

        ::

            >>> amp_comp_a = supriya.ugens.AmpCompA.ar(
            ...     frequency=1000,
            ...     min_amp=0.32,
            ...     root=0,
            ...     root_amp=1,
            ...     )
            >>> amp_comp_a.root_amp
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('root_amp')
        return self._inputs[index]
