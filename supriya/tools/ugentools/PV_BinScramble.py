# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class PV_BinScramble(PV_ChainUGen):
    r'''

    ::

        >>> pv_bin_scramble = ugentools.PV_BinScramble.(
        ...     buffer_id=None,
        ...     trigger=0,
        ...     width=0.2,
        ...     wipe=0,
        ...     )
        >>> pv_bin_scramble

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'wipe',
        'width',
        'trigger',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        trigger=0,
        width=0.2,
        wipe=0,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            trigger=trigger,
            width=width,
            wipe=wipe,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        trigger=0,
        width=0.2,
        wipe=0,
        ):
        r'''Constructs a PV_BinScramble.

        ::

            >>> pv_bin_scramble = ugentools.PV_BinScramble.new(
            ...     buffer_id=None,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            trigger=trigger,
            width=width,
            wipe=wipe,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of PV_BinScramble.

        ::

            >>> pv_bin_scramble = ugentools.PV_BinScramble.ar(
            ...     buffer_id=None,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of PV_BinScramble.

        ::

            >>> pv_bin_scramble = ugentools.PV_BinScramble.ar(
            ...     buffer_id=None,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def width(self):
        r'''Gets `width` input of PV_BinScramble.

        ::

            >>> pv_bin_scramble = ugentools.PV_BinScramble.ar(
            ...     buffer_id=None,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.width

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('width')
        return self._inputs[index]

    @property
    def wipe(self):
        r'''Gets `wipe` input of PV_BinScramble.

        ::

            >>> pv_bin_scramble = ugentools.PV_BinScramble.ar(
            ...     buffer_id=None,
            ...     trigger=0,
            ...     width=0.2,
            ...     wipe=0,
            ...     )
            >>> pv_bin_scramble.wipe

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('wipe')
        return self._inputs[index]