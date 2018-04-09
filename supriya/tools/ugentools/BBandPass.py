from supriya.tools.ugentools.BEQSuite import BEQSuite


class BBandPass(BEQSuite):
    """
    A band-pass filter.

    ::

        >>> source = ugentools.In.ar(0)
        >>> bband_pass = ugentools.BBandPass.ar(
        ...     bandwidth=1,
        ...     frequency=1200,
        ...     source=source,
        ...     )
        >>> bband_pass
        BBandPass.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Filter UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'bandwidth',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bandwidth=1,
        frequency=1200,
        source=None,
        ):
        BEQSuite.__init__(
            self,
            calculation_rate=calculation_rate,
            bandwidth=bandwidth,
            frequency=frequency,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bandwidth=1,
        frequency=1200,
        source=None,
        ):
        """
        Constructs an audio-rate BBandPass.

        ::

            >>> source = ugentools.In.ar(0)
            >>> bband_pass = ugentools.BBandPass.ar(
            ...     bandwidth=1,
            ...     frequency=1200,
            ...     source=source,
            ...     )
            >>> bband_pass
            BBandPass.ar()

        Returns ugen graph.
        """
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bandwidth=bandwidth,
            frequency=frequency,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def sc(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def bandwidth(self):
        """
        Gets `bandwidth` input of BBandPass.

        ::

            >>> source = ugentools.In.ar(0)
            >>> bband_pass = ugentools.BBandPass.ar(
            ...     bandwidth=1,
            ...     frequency=1200,
            ...     source=source,
            ...     )
            >>> bband_pass.bandwidth
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('bandwidth')
        return self._inputs[index]

    @property
    def frequency(self):
        """
        Gets `frequency` input of BBandPass.

        ::

            >>> source = ugentools.In.ar(0)
            >>> bband_pass = ugentools.BBandPass.ar(
            ...     bandwidth=1,
            ...     frequency=1200,
            ...     source=source,
            ...     )
            >>> bband_pass.frequency
            1200.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        """
        Gets `source` input of BBandPass.

        ::

            >>> source = ugentools.In.ar(0)
            >>> bband_pass = ugentools.BBandPass.ar(
            ...     bandwidth=1,
            ...     frequency=1200,
            ...     source=source,
            ...     )
            >>> bband_pass.source
            In.ar()[0]

        Returns ugen input.
        """
        index = self._ordered_input_names.index('source')
        return self._inputs[index]
