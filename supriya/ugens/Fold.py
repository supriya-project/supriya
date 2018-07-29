from supriya.ugens.UGen import UGen


class Fold(UGen):
    """
    Folds a signal outside given thresholds.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> fold = supriya.ugens.Fold.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ...     )
        >>> fold
        Fold.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Trigger Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'minimum',
        'maximum',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        maximum=1,
        minimum=0,
        source=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        maximum=1,
        minimum=0,
        source=None,
        ):
        """
        Constucts an audio-rate Fold ugen.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> fold = supriya.ugens.Fold.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> fold
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            source=source,
            )
        return ugen

    @classmethod
    def ir(
        cls,
        maximum=1,
        minimum=0,
        source=None,
        ):
        """
        Constucts a scalar-rate Fold ugen.

        ::

            >>> source = [supriya.ugens.Rand.ir(), supriya.ugens.Rand.ir()]
            >>> fold = supriya.ugens.Fold.ir(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> fold
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.SCALAR
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        maximum=1,
        minimum=0,
        source=None,
        ):
        """
        Constucts a control-rate Fold ugen.

        ::

            >>> source = supriya.ugens.SinOsc.kr(frequency=[4, 2])
            >>> fold = supriya.ugens.Fold.kr(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> fold
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            maximum=maximum,
            minimum=minimum,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def maximum(self):
        """
        Gets `maximum` input of Fold.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> fold = supriya.ugens.Fold.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> fold.maximum
            0.9

        Returns input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        """
        Gets `minimum` input of Fold.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> fold = supriya.ugens.Fold.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> fold.minimum
            0.1

        Returns input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `minimum` input of Fold.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> fold = supriya.ugens.Fold.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> fold.source
            SinOsc.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
