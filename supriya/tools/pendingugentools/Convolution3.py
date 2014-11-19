# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Convolution3(UGen):
    r'''

    ::

        >>> convolution_3 = ugentools.Convolution3.(
        ...     framesize=2048,
        ...     kernel=None,
        ...     source=None,
        ...     trigger=0,
        ...     )
        >>> convolution_3

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
        r'''Constructs an audio-rate Convolution3.

        ::

            >>> convolution_3 = ugentools.Convolution3.ar(
            ...     framesize=2048,
            ...     kernel=None,
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> convolution_3

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

    @classmethod
    def kr(
        cls,
        framesize=2048,
        kernel=None,
        source=None,
        trigger=0,
        ):
        r'''Constructs a control-rate Convolution3.

        ::

            >>> convolution_3 = ugentools.Convolution3.kr(
            ...     framesize=2048,
            ...     kernel=None,
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> convolution_3

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
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
        r'''Gets `source` input of Convolution3.

        ::

            >>> convolution_3 = ugentools.Convolution3.ar(
            ...     framesize=2048,
            ...     kernel=None,
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> convolution_3.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def kernel(self):
        r'''Gets `kernel` input of Convolution3.

        ::

            >>> convolution_3 = ugentools.Convolution3.ar(
            ...     framesize=2048,
            ...     kernel=None,
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> convolution_3.kernel

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('kernel')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of Convolution3.

        ::

            >>> convolution_3 = ugentools.Convolution3.ar(
            ...     framesize=2048,
            ...     kernel=None,
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> convolution_3.trigger

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]

    @property
    def framesize(self):
        r'''Gets `framesize` input of Convolution3.

        ::

            >>> convolution_3 = ugentools.Convolution3.ar(
            ...     framesize=2048,
            ...     kernel=None,
            ...     source=None,
            ...     trigger=0,
            ...     )
            >>> convolution_3.framesize

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('framesize')
        return self._inputs[index]