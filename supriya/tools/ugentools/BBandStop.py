# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BEQSuite import BEQSuite


class BBandStop(BEQSuite):
    r"""
    A band-stop filter.

    ::

        >>> source = ugentools.In.ar(0)
        >>> bband_stop = ugentools.BBandStop.ar(
        ...     bandwidth=1,
        ...     frequency=1200,
        ...     source=source,
        ...     )
        >>> bband_stop
        BBandStop.ar()

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
        r"""
        Constructs an audio-rate BBandStop.

        ::

            >>> source = ugentools.In.ar(0)
            >>> bband_stop = ugentools.BBandStop.ar(
            ...     bandwidth=1,
            ...     frequency=1200,
            ...     source=source,
            ...     )
            >>> bband_stop
            BBandStop.ar()

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
        r"""
        Gets `bandwidth` input of BBandStop.

        ::

            >>> source = ugentools.In.ar(0)
            >>> bband_stop = ugentools.BBandStop.ar(
            ...     bandwidth=1,
            ...     frequency=1200,
            ...     source=source,
            ...     )
            >>> bband_stop.bandwidth
            1.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('bandwidth')
        return self._inputs[index]

    @property
    def frequency(self):
        r"""
        Gets `frequency` input of BBandStop.

        ::

            >>> source = ugentools.In.ar(0)
            >>> bband_stop = ugentools.BBandStop.ar(
            ...     bandwidth=1,
            ...     frequency=1200,
            ...     source=source,
            ...     )
            >>> bband_stop.frequency
            1200.0

        Returns ugen input.
        """
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        r"""
        Gets `source` input of BBandStop.

        ::

            >>> source = ugentools.In.ar(0)
            >>> bband_stop = ugentools.BBandStop.ar(
            ...     bandwidth=1,
            ...     frequency=1200,
            ...     source=source,
            ...     )
            >>> bband_stop.source
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
