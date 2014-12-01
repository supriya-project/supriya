# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class FFTTrigger(PV_ChainUGen):
    r'''

    ::

        >>> ffttrigger = ugentools.FFTTrigger.ar(
        ...     buffer_id=buffer_id,
        ...     hop=0.5,
        ...     polar=0,
        ...     )
        >>> ffttrigger
        FFTTrigger.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'hop',
        'polar',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        hop=0.5,
        polar=0,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            hop=hop,
            polar=polar,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=buffer_id,
        hop=0.5,
        polar=0,
        ):
        r'''Constructs a FFTTrigger.

        ::

            >>> ffttrigger = ugentools.FFTTrigger.new(
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     polar=0,
            ...     )
            >>> ffttrigger
            FFTTrigger.new()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            hop=hop,
            polar=polar,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of FFTTrigger.

        ::

            >>> ffttrigger = ugentools.FFTTrigger.ar(
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     polar=0,
            ...     )
            >>> ffttrigger.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def hop(self):
        r'''Gets `hop` input of FFTTrigger.

        ::

            >>> ffttrigger = ugentools.FFTTrigger.ar(
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     polar=0,
            ...     )
            >>> ffttrigger.hop
            0.5

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('hop')
        return self._inputs[index]

    @property
    def polar(self):
        r'''Gets `polar` input of FFTTrigger.

        ::

            >>> ffttrigger = ugentools.FFTTrigger.ar(
            ...     buffer_id=buffer_id,
            ...     hop=0.5,
            ...     polar=0,
            ...     )
            >>> ffttrigger.polar
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('polar')
        return self._inputs[index]