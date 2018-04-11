from supriya.ugens.LPZ1 import LPZ1


class HPZ1(LPZ1):
    """
    A two point difference filter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> hpz_1 = supriya.ugens.HPZ1.ar(
        ...     source=source,
        ...     )
        >>> hpz_1
        HPZ1.ar()

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
        LPZ1.__init__(
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
        Constructs an audio-rate HPZ1.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> hpz_1 = supriya.ugens.HPZ1.ar(
            ...     source=source,
            ...     )
            >>> hpz_1
            HPZ1.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
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
        Constructs a control-rate HPZ1.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> hpz_1 = supriya.ugens.HPZ1.kr(
            ...     source=source,
            ...     )
            >>> hpz_1
            HPZ1.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
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
        Gets `source` input of HPZ1.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> hpz_1 = supriya.ugens.HPZ1.ar(
            ...     source=source,
            ...     )
            >>> hpz_1.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
