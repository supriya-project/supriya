# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Convolution2(UGen):
    r'''

    ::

        >>> convolution_2 = ugentools.Convolution2.(
        ...     framesize=2048,
        ...     kernel=None,
        ...     source=None,
        ...     trigger=0,
        ...     )
        >>> convolution_2

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'kernel',
        'trigger',
        'framesize',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        framesize=2048,
        kernel=None,
        source=None,
        trigger=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            framesize=framesize,
            kernel=kernel,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        framesize=2048,
        kernel=None,
        source=None,
        trigger=0,
        ):
        r'''Constructs an audio-rate Convolution2.

        ::

            >>> convolution_2 = ugentools.Convolution2.ar(
            ...     framesize=2048,
            ...     kernel=None,
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> convolution_2

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            framesize=framesize,
            kernel=kernel,
            source=source,
            trigger=trigger,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of Convolution2.

        ::

            >>> convolution_2 = ugentools.Convolution2.ar(
            ...     framesize=2048,
            ...     kernel=None,
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> convolution_2.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def kernel(self):
        r'''Gets `kernel` input of Convolution2.

        ::

            >>> convolution_2 = ugentools.Convolution2.ar(
            ...     framesize=2048,
            ...     kernel=None,
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> convolution_2.kernel

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('kernel')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of Convolution2.

        ::

            >>> convolution_2 = ugentools.Convolution2.ar(
            ...     framesize=2048,
            ...     kernel=None,
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> convolution_2.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def framesize(self):
        r'''Gets `framesize` input of Convolution2.

        ::

            >>> convolution_2 = ugentools.Convolution2.ar(
            ...     framesize=2048,
            ...     kernel=None,
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> convolution_2.framesize

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('framesize')
        return self._inputs[index]