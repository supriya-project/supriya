from supriya.tools.ugentools.Filter import Filter


class Median(Filter):
    """
    A median filter.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> median = ugentools.Median.ar(
        ...     length=3,
        ...     source=source,
        ...     )
        >>> median
        Median.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'length',
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        length=3,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            length=length,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        length=3,
        source=None,
        ):
        """
        Constructs an audio-rate Median.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> median = ugentools.Median.ar(
            ...     length=3,
            ...     source=source,
            ...     )
            >>> median
            Median.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            length=length,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        length=3,
        source=None,
        ):
        """
        Constructs a control-rate Median.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> median = ugentools.Median.kr(
            ...     length=3,
            ...     source=source,
            ...     )
            >>> median
            Median.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            length=length,
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
    def length(self):
        """
        Gets `length` input of Median.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> median = ugentools.Median.ar(
            ...     length=3,
            ...     source=source,
            ...     )
            >>> median.length
            3.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('length')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of Median.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> median = ugentools.Median.ar(
            ...     length=3,
            ...     source=source,
            ...     )
            >>> median.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
