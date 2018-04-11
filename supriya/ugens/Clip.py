from supriya.ugens.UGen import UGen


class Clip(UGen):
    """
    Clips a signal outside given thresholds.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> clip = supriya.ugens.Clip.ar(
        ...     maximum=0.9,
        ...     minimum=0.1,
        ...     source=source,
        ...     )
        >>> clip
        Clip.ar()

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
        Constucts an audio-rate Clip ugen.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> clip = supriya.ugens.Clip.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> clip
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
        Constucts a scalar-rate Clip ugen.

        ::

            >>> source = [supriya.ugens.Rand.ir(), supriya.ugens.Rand.ir()]
            >>> clip = supriya.ugens.Clip.ir(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> clip
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
        Constucts a control-rate Clip ugen.

        ::

            >>> source = supriya.ugens.SinOsc.kr(frequency=[4, 2])
            >>> clip = supriya.ugens.Clip.kr(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> clip
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
        Gets `maximum` input of Clip.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> clip = supriya.ugens.Clip.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> clip.maximum
            0.9

        Returns input.
        """
        index = self._ordered_input_names.index('maximum')
        return self._inputs[index]

    @property
    def minimum(self):
        """
        Gets `minimum` input of Clip.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> clip = supriya.ugens.Clip.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> clip.minimum
            0.1

        Returns input.
        """
        index = self._ordered_input_names.index('minimum')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `minimum` input of Clip.

        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> clip = supriya.ugens.Clip.ar(
            ...     maximum=0.9,
            ...     minimum=0.1,
            ...     source=source,
            ...     )
            >>> clip.source
            SinOsc.ar()[0]

        Returns input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
