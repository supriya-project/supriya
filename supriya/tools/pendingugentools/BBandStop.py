# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BEQSuite import BEQSuite


class BBandStop(BEQSuite):
    r'''

    ::

        >>> bband_stop = ugentools.BBandStop.(
        ...     bw=1,
        ...     frequency=1200,
        ...     source=None,
        ...     )
        >>> bband_stop

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'frequency',
        'bw',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bw=1,
        frequency=1200,
        source=None,
        ):
        BEQSuite.__init__(
            self,
            calculation_rate=calculation_rate,
            bw=bw,
            frequency=frequency,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        bw=1,
        frequency=1200,
        source=None,
        ):
        r'''Constructs an audio-rate BBandStop.

        ::

            >>> bband_stop = ugentools.BBandStop.ar(
            ...     bw=1,
            ...     frequency=1200,
            ...     source=None,
            ...     )
            >>> bband_stop

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bw=bw,
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
    def bw(self):
        r'''Gets `bw` input of BBandStop.

        ::

            >>> bband_stop = ugentools.BBandStop.ar(
            ...     bw=1,
            ...     frequency=1200,
            ...     source=None,
            ...     )
            >>> bband_stop.bw

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bw')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of BBandStop.

        ::

            >>> bband_stop = ugentools.BBandStop.ar(
            ...     bw=1,
            ...     frequency=1200,
            ...     source=None,
            ...     )
            >>> bband_stop.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of BBandStop.

        ::

            >>> bband_stop = ugentools.BBandStop.ar(
            ...     bw=1,
            ...     frequency=1200,
            ...     source=None,
            ...     )
            >>> bband_stop.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]