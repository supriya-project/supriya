from supriya.tools.ugentools.LPZ1 import LPZ1


class HPZ1(LPZ1):
    """
    A two point difference filter.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> hpz_1 = ugentools.HPZ1.ar(
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

            >>> source = ugentools.In.ar(bus=0)
            >>> hpz_1 = ugentools.HPZ1.ar(
            ...     source=source,
            ...     )
            >>> hpz_1
            HPZ1.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
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

            >>> source = ugentools.In.ar(bus=0)
            >>> hpz_1 = ugentools.HPZ1.kr(
            ...     source=source,
            ...     )
            >>> hpz_1
            HPZ1.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
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

            >>> source = ugentools.In.ar(bus=0)
            >>> hpz_1 = ugentools.HPZ1.ar(
            ...     source=source,
            ...     )
            >>> hpz_1.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
