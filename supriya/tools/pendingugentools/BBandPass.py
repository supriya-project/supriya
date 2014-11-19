# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.BEQSuite import BEQSuite


class BBandPass(BEQSuite):
    r'''

    ::

        >>> bband_pass = ugentools.BBandPass.(
        ...     bw=1,
        ...     frequency=1200,
        ...     source=None,
        ...     )
        >>> bband_pass

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
        r'''Constructs an audio-rate BBandPass.

        ::

            >>> bband_pass = ugentools.BBandPass.ar(
            ...     bw=1,
            ...     frequency=1200,
            ...     source=None,
            ...     )
            >>> bband_pass

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
    def source(self):
        r'''Gets `source` input of BBandPass.

        ::

            >>> bband_pass = ugentools.BBandPass.ar(
            ...     bw=1,
            ...     frequency=1200,
            ...     source=None,
            ...     )
            >>> bband_pass.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def frequency(self):
        r'''Gets `frequency` input of BBandPass.

        ::

            >>> bband_pass = ugentools.BBandPass.ar(
            ...     bw=1,
            ...     frequency=1200,
            ...     source=None,
            ...     )
            >>> bband_pass.frequency

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('frequency')
        return self._inputs[index]

    @property
    def bw(self):
        r'''Gets `bw` input of BBandPass.

        ::

            >>> bband_pass = ugentools.BBandPass.ar(
            ...     bw=1,
            ...     frequency=1200,
            ...     source=None,
            ...     )
            >>> bband_pass.bw

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bw')
        return self._inputs[index]