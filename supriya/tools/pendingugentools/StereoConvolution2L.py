# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class StereoConvolution2L(MultiOutUGen):
    r'''

    ::

        >>> stereo_convolution_2_l = ugentools.StereoConvolution2L.ar(
        ...     crossfade=1,
        ...     framesize=2048,
        ...     kernel_l=kernel_l,
        ...     kernel_r=kernel_r,
        ...     source=source,
        ...     trigger=0,
        ...     )
        >>> stereo_convolution_2_l
        StereoConvolution2L.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'kernel_l',
        'kernel_r',
        'trigger',
        'framesize',
        'crossfade',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        crossfade=1,
        framesize=2048,
        kernel_l=None,
        kernel_r=None,
        source=None,
        trigger=0,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            crossfade=crossfade,
            framesize=framesize,
            kernel_l=kernel_l,
            kernel_r=kernel_r,
            source=source,
            trigger=trigger,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        crossfade=1,
        framesize=2048,
        kernel_l=None,
        kernel_r=None,
        source=None,
        trigger=0,
        ):
        r'''Constructs an audio-rate StereoConvolution2L.

        ::

            >>> stereo_convolution_2_l = ugentools.StereoConvolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel_l=kernel_l,
            ...     kernel_r=kernel_r,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> stereo_convolution_2_l
            StereoConvolution2L.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            crossfade=crossfade,
            framesize=framesize,
            kernel_l=kernel_l,
            kernel_r=kernel_r,
            source=source,
            trigger=trigger,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def crossfade(self):
        r'''Gets `crossfade` input of StereoConvolution2L.

        ::

            >>> stereo_convolution_2_l = ugentools.StereoConvolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel_l=kernel_l,
            ...     kernel_r=kernel_r,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> stereo_convolution_2_l.crossfade
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('crossfade')
        return self._inputs[index]

    @property
    def framesize(self):
        r'''Gets `framesize` input of StereoConvolution2L.

        ::

            >>> stereo_convolution_2_l = ugentools.StereoConvolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel_l=kernel_l,
            ...     kernel_r=kernel_r,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> stereo_convolution_2_l.framesize
            2048.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('framesize')
        return self._inputs[index]

    @property
    def kernel_l(self):
        r'''Gets `kernel_l` input of StereoConvolution2L.

        ::

            >>> stereo_convolution_2_l = ugentools.StereoConvolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel_l=kernel_l,
            ...     kernel_r=kernel_r,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> stereo_convolution_2_l.kernel_l

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('kernel_l')
        return self._inputs[index]

    @property
    def kernel_r(self):
        r'''Gets `kernel_r` input of StereoConvolution2L.

        ::

            >>> stereo_convolution_2_l = ugentools.StereoConvolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel_l=kernel_l,
            ...     kernel_r=kernel_r,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> stereo_convolution_2_l.kernel_r

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('kernel_r')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of StereoConvolution2L.

        ::

            >>> stereo_convolution_2_l = ugentools.StereoConvolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel_l=kernel_l,
            ...     kernel_r=kernel_r,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> stereo_convolution_2_l.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def trigger(self):
        r'''Gets `trigger` input of StereoConvolution2L.

        ::

            >>> stereo_convolution_2_l = ugentools.StereoConvolution2L.ar(
            ...     crossfade=1,
            ...     framesize=2048,
            ...     kernel_l=kernel_l,
            ...     kernel_r=kernel_r,
            ...     source=source,
            ...     trigger=0,
            ...     )
            >>> stereo_convolution_2_l.trigger
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('trigger')
        return self._inputs[index]