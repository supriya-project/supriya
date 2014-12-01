# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class PanB(MultiOutUGen):
    r'''

    ::

        >>> pan_b = ugentools.PanB.ar(
        ...     azimuth=0,
        ...     elevation=0,
        ...     gain=1,
        ...     source=source,
        ...     )
        >>> pan_b
        PanB.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'azimuth',
        'elevation',
        'gain',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        azimuth=0,
        elevation=0,
        gain=1,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            elevation=elevation,
            gain=gain,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        azimuth=0,
        elevation=0,
        gain=1,
        source=None,
        ):
        r'''Constructs an audio-rate PanB.

        ::

            >>> pan_b = ugentools.PanB.ar(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b
            PanB.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            elevation=elevation,
            gain=gain,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        azimuth=0,
        elevation=0,
        gain=1,
        source=None,
        ):
        r'''Constructs a control-rate PanB.

        ::

            >>> pan_b = ugentools.PanB.kr(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b
            PanB.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            azimuth=azimuth,
            elevation=elevation,
            gain=gain,
            source=source,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def azimuth(self):
        r'''Gets `azimuth` input of PanB.

        ::

            >>> pan_b = ugentools.PanB.ar(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b.azimuth
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('azimuth')
        return self._inputs[index]

    @property
    def elevation(self):
        r'''Gets `elevation` input of PanB.

        ::

            >>> pan_b = ugentools.PanB.ar(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b.elevation
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('elevation')
        return self._inputs[index]

    @property
    def gain(self):
        r'''Gets `gain` input of PanB.

        ::

            >>> pan_b = ugentools.PanB.ar(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b.gain
            1.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('gain')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of PanB.

        ::

            >>> pan_b = ugentools.PanB.ar(
            ...     azimuth=0,
            ...     elevation=0,
            ...     gain=1,
            ...     source=source,
            ...     )
            >>> pan_b.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]