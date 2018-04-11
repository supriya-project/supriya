from supriya.ugens.UGen import UGen


class MantissaMask(UGen):
    """
    A floating-point mantissa mask.

    ::

        >>> source = supriya.ugens.SinOsc.ar()
        >>> mantissa_mask = supriya.ugens.MantissaMask.ar(
        ...     source=source,
        ...     bits=3,
        ...     )
        >>> mantissa_mask
        MantissaMask.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'bits',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bits=3,
        source=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            bits=bits,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bits=3,
        source=0,
        ):
        """
        Constructs an audio-rate floating-point mantissa mask.

        ::

            >>> source = supriya.ugens.SinOsc.ar(frequency=[440, 442])
            >>> mantissa_mask = supriya.ugens.MantissaMask.ar(
            ...     source=source,
            ...     bits=3,
            ...     )
            >>> mantissa_mask
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bits=bits,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        bits=3,
        source=0,
        ):
        """
        Constucts a control-rate floating-point mantissa mask.

        ::

            >>> source = supriya.ugens.SinOsc.kr(frequency=[4, 2])
            >>> mantissa_mask = supriya.ugens.MantissaMask.kr(
            ...     source=source,
            ...     bits=3,
            ...     )
            >>> mantissa_mask
            UGenArray({2})

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bits=bits,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def bits(self):
        """
        Gets `bits` input of MantissaMask.
        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> mantissa_mask = supriya.ugens.MantissaMask.ar(
            ...     source=source,
            ...     bits=3,
            ...     )
            >>> mantissa_mask.bits
            3.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('bits')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of MantissaMask.
        ::

            >>> source = supriya.ugens.SinOsc.ar()
            >>> mantissa_mask = supriya.ugens.MantissaMask.ar(
            ...     source=source,
            ...     bits=3,
            ...     )
            >>> mantissa_mask.source
            SinOsc.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
