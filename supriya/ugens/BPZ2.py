from supriya.ugens.LPZ2 import LPZ2


class BPZ2(LPZ2):
    """
    A two zero fixed midpass filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> bpz_2 = supriya.ugens.BPZ2.ar(
        ...     source=source,
        ...     )
        >>> bpz_2
        BPZ2.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        LPZ2.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        """
        Constructs an audio-rate BPZ2.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> bpz_2 = supriya.ugens.BPZ2.ar(
            ...     source=source,
            ...     )
            >>> bpz_2
            BPZ2.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        """
        Constructs a control-rate BPZ2.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> bpz_2 = supriya.ugens.BPZ2.kr(
            ...     source=source,
            ...     )
            >>> bpz_2
            BPZ2.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        """
        Gets `source` input of BPZ2.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> bpz_2 = supriya.ugens.BPZ2.ar(
            ...     source=source,
            ...     )
            >>> bpz_2.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
