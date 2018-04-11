from supriya.ugens.UGen import UGen


class Klang(UGen):
    """

    ::

        >>> klang = supriya.ugens.Klang.ar(
        ...     freqoffset=0,
        ...     freqscale=1,
        ...     specifications_array_ref=specifications_array_ref,
        ...     )
        >>> klang
        Klang.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'specifications_array_ref',
        'freqscale',
        'freqoffset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        freqoffset=0,
        freqscale=1,
        specifications_array_ref=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            freqoffset=freqoffset,
            freqscale=freqscale,
            specifications_array_ref=specifications_array_ref,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        freqoffset=0,
        freqscale=1,
        specifications_array_ref=None,
        ):
        """
        Constructs an audio-rate Klang.

        ::

            >>> klang = supriya.ugens.Klang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> klang
            Klang.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            freqoffset=freqoffset,
            freqscale=freqscale,
            specifications_array_ref=specifications_array_ref,
            )
        return ugen

    # def new1(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def freqoffset(self):
        """
        Gets `freqoffset` input of Klang.

        ::

            >>> klang = supriya.ugens.Klang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> klang.freqoffset
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('freqoffset')
        return self._inputs[index]

    @property
    def freqscale(self):
        """
        Gets `freqscale` input of Klang.

        ::

            >>> klang = supriya.ugens.Klang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> klang.freqscale
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('freqscale')
        return self._inputs[index]

    @property
    def specifications_array_ref(self):
        """
        Gets `specifications_array_ref` input of Klang.

        ::

            >>> klang = supriya.ugens.Klang.ar(
            ...     freqoffset=0,
            ...     freqscale=1,
            ...     specifications_array_ref=specifications_array_ref,
            ...     )
            >>> klang.specifications_array_ref

        Returns ugen input.
        """
        index = self._ordered_input_names.index('specifications_array_ref')
        return self._inputs[index]
