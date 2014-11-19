# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class IFFT(WidthFirstUGen):
    r'''

    ::

        >>> ifft = ugentools.IFFT.(
        ...     buffer_=None,
        ...     winsize=0,
        ...     wintype=0,
        ...     )
        >>> ifft

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_',
        'wintype',
        'winsize',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_=None,
        winsize=0,
        wintype=0,
        ):
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            winsize=winsize,
            wintype=wintype,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_=None,
        winsize=0,
        wintype=0,
        ):
        r'''Constructs an audio-rate IFFT.

        ::

            >>> ifft = ugentools.IFFT.ar(
            ...     buffer_=None,
            ...     winsize=0,
            ...     wintype=0,
            ...     )
            >>> ifft

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            winsize=winsize,
            wintype=wintype,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_=None,
        winsize=0,
        wintype=0,
        ):
        r'''Constructs a control-rate IFFT.

        ::

            >>> ifft = ugentools.IFFT.kr(
            ...     buffer_=None,
            ...     winsize=0,
            ...     wintype=0,
            ...     )
            >>> ifft

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            winsize=winsize,
            wintype=wintype,
            )
        return ugen

    @classmethod
    def new(
        cls,
        buffer_=None,
        winsize=0,
        wintype=0,
        ):
        r'''Constructs a IFFT.

        ::

            >>> ifft = ugentools.IFFT.new(
            ...     buffer_=None,
            ...     winsize=0,
            ...     wintype=0,
            ...     )
            >>> ifft

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_=buffer_,
            winsize=winsize,
            wintype=wintype,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_(self):
        r'''Gets `buffer_` input of IFFT.

        ::

            >>> ifft = ugentools.IFFT.ar(
            ...     buffer_=None,
            ...     winsize=0,
            ...     wintype=0,
            ...     )
            >>> ifft.buffer_

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_')
        return self._inputs[index]

    @property
    def wintype(self):
        r'''Gets `wintype` input of IFFT.

        ::

            >>> ifft = ugentools.IFFT.ar(
            ...     buffer_=None,
            ...     winsize=0,
            ...     wintype=0,
            ...     )
            >>> ifft.wintype

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('wintype')
        return self._inputs[index]

    @property
    def winsize(self):
        r'''Gets `winsize` input of IFFT.

        ::

            >>> ifft = ugentools.IFFT.ar(
            ...     buffer_=None,
            ...     winsize=0,
            ...     wintype=0,
            ...     )
            >>> ifft.winsize

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('winsize')
        return self._inputs[index]