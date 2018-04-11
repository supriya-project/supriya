from supriya.ugens.UGen import UGen


class Schmidt(UGen):
    """
    A Schmidt trigger.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> schmidt = supriya.ugens.Schmidt.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ...     )
        >>> schmidt
        Schmidt.ar()

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
        Constucts an audio-rate Schmidt ugen.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> schmidt = supriya.ugens.Schmidt.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> schmidt
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
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
        Constucts a scalar-rate Schmidt ugen.

        ::

            >>> source = [supriya.ugens.Rand.ir(), supriya.ugens.Rand.ir()]
            >>> schmidt = supriya.ugens.Schmidt.ir(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> schmidt
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.SCALAR
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
        Constucts a control-rate Schmidt ugen.

        ::

            >>> source = supriya.ugens.SinOsc.kr(frequency=[4, 2])
            >>> schmidt = supriya.ugens.Schmidt.kr(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> schmidt
            UGenArray({2})

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
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
        Gets `maximum` input of Schmidt.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> schmidt = supriya.ugens.Schmidt.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> schmidt.maximum
            0.9

        Returns input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        """
        Gets `minimum` input of Schmidt.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> schmidt = supriya.ugens.Schmidt.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> schmidt.minimum
            0.1

        Returns input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `minimum` input of Schmidt.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> schmidt = supriya.ugens.Schmidt.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> schmidt.source
            SinOsc.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
