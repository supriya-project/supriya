from supriya.tools.ugentools.Filter import Filter


class SOS(Filter):
    """
    A second-order filter section.

    ::

        out(i) = (a0 * in(i)) + (a1 * in(i-1)) + (b1 * out(i-1))

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> sos = ugentools.SOS.ar(
        ...     a_0=0,
        ...     a_1=0,
        ...     a_2=0,
        ...     b_1=0,
        ...     b_2=0,
        ...     source=source,
        ...     )
        >>> sos
        SOS.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'a_0',
        'a_1',
        'a_2',
        'b_1',
        'b_2',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        a_0=0,
        a_1=0,
        a_2=0,
        b_1=0,
        b_2=0,
        source=None,
        ):
        Filter.__init__(
            self,
            calculation_rate=calculation_rate,
            a_0=a_0,
            a_1=a_1,
            a_2=a_2,
            b_1=b_1,
            b_2=b_2,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        a_0=0,
        a_1=0,
        a_2=0,
        b_1=0,
        b_2=0,
        source=None,
        ):
        """
        Constructs an audio-rate SOS.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> sos = ugentools.SOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     a_2=0,
            ...     b_1=0,
            ...     b_2=0,
            ...     source=source,
            ...     )
            >>> sos
            SOS.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a_0=a_0,
            a_1=a_1,
            a_2=a_2,
            b_1=b_1,
            b_2=b_2,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        a_0=0,
        a_1=0,
        a_2=0,
        b_1=0,
        b_2=0,
        source=None,
        ):
        """
        Constructs a control-rate SOS.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> sos = ugentools.SOS.kr(
            ...     a_0=0,
            ...     a_1=0,
            ...     a_2=0,
            ...     b_1=0,
            ...     b_2=0,
            ...     source=source,
            ...     )
            >>> sos
            SOS.kr()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            a_0=a_0,
            a_1=a_1,
            a_2=a_2,
            b_1=b_1,
            b_2=b_2,
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
    def a_0(self):
        """
        Gets `a_0` input of SOS.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> sos = ugentools.SOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     a_2=0,
            ...     b_1=0,
            ...     b_2=0,
            ...     source=source,
            ...     )
            >>> sos.a_0
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a_0')
        return self._inputs[index]

    @property
    def a_1(self):
        """
        Gets `a_1` input of SOS.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> sos = ugentools.SOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     a_2=0,
            ...     b_1=0,
            ...     b_2=0,
            ...     source=source,
            ...     )
            >>> sos.a_1
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a_1')
        return self._inputs[index]

    @property
    def a_2(self):
        """
        Gets `a_2` input of SOS.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> sos = ugentools.SOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     a_2=0,
            ...     b_1=0,
            ...     b_2=0,
            ...     source=source,
            ...     )
            >>> sos.a_2
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('a_2')
        return self._inputs[index]

    @property
    def b_1(self):
        """
        Gets `b_1` input of SOS.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> sos = ugentools.SOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     a_2=0,
            ...     b_1=0,
            ...     b_2=0,
            ...     source=source,
            ...     )
            >>> sos.b_1
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('b_1')
        return self._inputs[index]

    @property
    def b_2(self):
        """
        Gets `b_2` input of SOS.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> sos = ugentools.SOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     a_2=0,
            ...     b_1=0,
            ...     b_2=0,
            ...     source=source,
            ...     )
            >>> sos.b_2
            0.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('b_2')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of SOS.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> sos = ugentools.SOS.ar(
            ...     a_0=0,
            ...     a_1=0,
            ...     a_2=0,
            ...     b_1=0,
            ...     b_2=0,
            ...     source=source,
            ...     )
            >>> sos.source
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
