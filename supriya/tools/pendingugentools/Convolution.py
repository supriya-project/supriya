# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Convolution(UGen):
    r'''

    ::

        >>> convolution = ugentools.Convolution.(
        ...     framesize=512,
        ...     kernel=None,
        ...     source=None,
        ...     )
        >>> convolution

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'kernel',
        'framesize',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        framesize=512,
        kernel=None,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            framesize=framesize,
            kernel=kernel,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        framesize=512,
        kernel=None,
        source=None,
        ):
        r'''Constructs an audio-rate Convolution.

        ::

            >>> convolution = ugentools.Convolution.ar(
            ...     framesize=512,
            ...     kernel=None,
            ...     source=None,
            ...     )
            >>> convolution

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            framesize=framesize,
            kernel=kernel,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def framesize(self):
        r'''Gets `framesize` input of Convolution.

        ::

            >>> convolution = ugentools.Convolution.ar(
            ...     framesize=512,
            ...     kernel=None,
            ...     source=None,
            ...     )
            >>> convolution.framesize

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('framesize')
        return self._inputs[index]

    @property
    def kernel(self):
        r'''Gets `kernel` input of Convolution.

        ::

            >>> convolution = ugentools.Convolution.ar(
            ...     framesize=512,
            ...     kernel=None,
            ...     source=None,
            ...     )
            >>> convolution.kernel

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('kernel')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Convolution.

        ::

            >>> convolution = ugentools.Convolution.ar(
            ...     framesize=512,
            ...     kernel=None,
            ...     source=None,
            ...     )
            >>> convolution.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]