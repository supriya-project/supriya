from supriya.ugens.Filter import Filter


class Slew(Filter):
    """
    A slew rate limiter.

    ::

        >>> source = supriya.ugens.In.ar(bus=0)
        >>> slew = supriya.ugens.Slew.ar(
        ...     dn=1,
        ...     source=source,
        ...     up=1,
        ...     )
        >>> slew
        Slew.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'up',
        'dn',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        dn=1,
        source=None,
        up=1,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            dn=dn,
            source=source,
            up=up,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        dn=1,
        source=None,
        up=1,
        ):
        """
        Constructs an audio-rate Slew.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> slew = supriya.ugens.Slew.ar(
            ...     dn=1,
            ...     source=source,
            ...     up=1,
            ...     )
            >>> slew
            Slew.ar()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            dn=dn,
            source=source,
            up=up,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        dn=1,
        source=None,
        up=1,
        ):
        """
        Constructs a control-rate Slew.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> slew = supriya.ugens.Slew.kr(
            ...     dn=1,
            ...     source=source,
            ...     up=1,
            ...     )
            >>> slew
            Slew.kr()

        Returns ugen graph.
        """
        import supriya.synthdefs
        calculation_rate = supriya.synthdefs.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            dn=dn,
            source=source,
            up=up,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def dn(self):
        """
        Gets `dn` input of Slew.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> slew = supriya.ugens.Slew.ar(
            ...     dn=1,
            ...     source=source,
            ...     up=1,
            ...     )
            >>> slew.dn
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('dn')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Slew.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> slew = supriya.ugens.Slew.ar(
            ...     dn=1,
            ...     source=source,
            ...     up=1,
            ...     )
            >>> slew.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def up(self):
        """
        Gets `up` input of Slew.

        ::

            >>> source = supriya.ugens.In.ar(bus=0)
            >>> slew = supriya.ugens.Slew.ar(
            ...     dn=1,
            ...     source=source,
            ...     up=1,
            ...     )
            >>> slew.up
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('up')
        return self._inputs[index]
