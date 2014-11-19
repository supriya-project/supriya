# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_ChainUGen import PV_ChainUGen


class FFT(PV_ChainUGen):
    r'''

    ::

        >>> fft = ugentools.FFT.(
        ...     active=1,
        ...     buffer_id=None,
        ...     hop=0.5,
        ...     source=None,
        ...     window_size=0,
        ...     window_type=0,
        ...     )
        >>> fft

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        'hop',
        'window_type',
        'active',
        'window_size',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        active=1,
        buffer_id=None,
        hop=0.5,
        source=None,
        window_size=0,
        window_type=0,
        ):
        PV_ChainUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            active=active,
            buffer_id=buffer_id,
            hop=hop,
            source=source,
            window_size=window_size,
            window_type=window_type,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        active=1,
        buffer_id=None,
        hop=0.5,
        source=None,
        window_size=0,
        window_type=0,
        ):
        r'''Constructs a FFT.

        ::

            >>> fft = ugentools.FFT.new(
            ...     active=1,
            ...     buffer_id=None,
            ...     hop=0.5,
            ...     source=None,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            active=active,
            buffer_id=buffer_id,
            hop=hop,
            source=source,
            window_size=window_size,
            window_type=window_type,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def active(self):
        r'''Gets `active` input of FFT.

        ::

            >>> fft = ugentools.FFT.ar(
            ...     active=1,
            ...     buffer_id=None,
            ...     hop=0.5,
            ...     source=None,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.active

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('active')
        return self._inputs[index]

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of FFT.

        ::

            >>> fft = ugentools.FFT.ar(
            ...     active=1,
            ...     buffer_id=None,
            ...     hop=0.5,
            ...     source=None,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def hop(self):
        r'''Gets `hop` input of FFT.

        ::

            >>> fft = ugentools.FFT.ar(
            ...     active=1,
            ...     buffer_id=None,
            ...     hop=0.5,
            ...     source=None,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.hop

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('hop')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of FFT.

        ::

            >>> fft = ugentools.FFT.ar(
            ...     active=1,
            ...     buffer_id=None,
            ...     hop=0.5,
            ...     source=None,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def window_size(self):
        r'''Gets `window_size` input of FFT.

        ::

            >>> fft = ugentools.FFT.ar(
            ...     active=1,
            ...     buffer_id=None,
            ...     hop=0.5,
            ...     source=None,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.window_size

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('window_size')
        return self._inputs[index]

    @property
    def window_type(self):
        r'''Gets `window_type` input of FFT.

        ::

            >>> fft = ugentools.FFT.ar(
            ...     active=1,
            ...     buffer_id=None,
            ...     hop=0.5,
            ...     source=None,
            ...     window_size=0,
            ...     window_type=0,
            ...     )
            >>> fft.window_type

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('window_type')
        return self._inputs[index]