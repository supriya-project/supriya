# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PanB2(MultiOutUGen):
    r'''A 2D ambisonic b-format panner.

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> pan_b_2 = ugentools.PanB2.ar(
        ...     azimuth=0,
        ...     gain=1,
        ...     source=source,
        ...     )
        >>> pan_b_2
        UGenArray({3})

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'azimuth',
        'gain',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        azimuth=0,
        gain=1,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            channel_count=3,
            azimuth=azimuth,
            gain=gain,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        azimuth=0,
        gain=1,
        source=None,
        ):
        r'''Constructs an audio-rate PanB2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_b_2 = ugentools.PanB2.ar(
            ...     azimuth=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b_2
            UGenArray({3})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        azimuth=0,
        gain=1,
        source=None,
        ):
        r'''Constructs a control-rate PanB2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_b_2 = ugentools.PanB2.kr(
            ...     azimuth=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b_2
            UGenArray({3})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            gain=gain,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def azimuth(self):
        r'''Gets `azimuth` input of PanB2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_b_2 = ugentools.PanB2.ar(
            ...     azimuth=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b_2[0].source.azimuth
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('azimuth')
        return self._inputs[index]

    @property
    def gain(self):
        r'''Gets `gain` input of PanB2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_b_2 = ugentools.PanB2.ar(
            ...     azimuth=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b_2[0].source.gain
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('gain')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of PanB2.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> pan_b_2 = ugentools.PanB2.ar(
            ...     azimuth=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b_2[0].source.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]