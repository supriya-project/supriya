# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_RandWipe(PV_ChainUGen):
    r'''

    ::

        >>> pv_rand_wipe = ugentools.PV_RandWipe.(
        ...     buffer_a=None,
        ...     buffer_b=None,
        ...     trigger=0,
        ...     wipe=0,
        ...     )
        >>> pv_rand_wipe

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_a',
        'buffer_b',
        'wipe',
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_a=None,
        buffer_b=None,
        trigger=0,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            trigger=trigger,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_a=None,
        buffer_b=None,
        trigger=0,
        wipe=0,
        ):
        r'''Constructs a PV_RandWipe.

        ::

            >>> pv_rand_wipe = ugentools.PV_RandWipe.new(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_wipe

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            trigger=trigger,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_a(self):
        r'''Gets `buffer_a` input of PV_RandWipe.

        ::

            >>> pv_rand_wipe = ugentools.PV_RandWipe.ar(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_wipe.buffer_a

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_a')
        return self._inputs[index]

    @property
    def buffer_b(self):
        r'''Gets `buffer_b` input of PV_RandWipe.

        ::

            >>> pv_rand_wipe = ugentools.PV_RandWipe.ar(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_wipe.buffer_b

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_b')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of PV_RandWipe.

        ::

            >>> pv_rand_wipe = ugentools.PV_RandWipe.ar(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_wipe.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def wipe(self):
        r'''Gets `wipe` input of PV_RandWipe.

        ::

            >>> pv_rand_wipe = ugentools.PV_RandWipe.ar(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     trigger=0,
            ...     wipe=0,
            ...     )
            >>> pv_rand_wipe.wipe

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]