# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.UGen import UGen


class Compander(UGen):
    r'''A general purpose hard-knee dynamics processor.

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Dynamics UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'control',
        'threshold',
        'slope_below',
        'slope_above',
        'clamp_time',
        'relax_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        clamp_time=0.01,
        control=0.,
        calculation_rate=None,
        relax_time=0.1,
        slope_above=1.,
        slope_below=1.,
        source=0.,
        threshold=0.5,
        ):
        UGen.__init__(
            self,
            clamp_time=clamp_time,
            control=control,
            calculation_rate=calculation_rate,
            relax_time=relax_time,
            slope_above=slope_above,
            slope_below=slope_below,
            source=source,
            threshold=threshold,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        clamp_time=0.01,
        control=0.,
        relax_time=0.1,
        slope_above=1.,
        slope_below=1.,
        source=0.,
        threshold=0.5,
        ):
        r'''Constructs an audio-rate dynamics processor.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> compander = ugentools.Compander.ar(
            ...    source=source,
            ...    )
            >>> compander
            Compander.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            clamp_time=clamp_time,
            control=control,
            calculation_rate=calculation_rate,
            relax_time=relax_time,
            slope_above=slope_above,
            slope_below=slope_below,
            source=source,
            threshold=threshold,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def clamp_time(self):
        r'''Gets `clamp_time` input of Compander.

        ::

            >>> clamp_time = 0.01
            >>> source = ugentools.In.ar(bus=0)
            >>> compander = ugentools.Compander.ar(
            ...     clamp_time=clamp_time,
            ...     source=source,
            ...     )
            >>> compander.clamp_time
            0.01

        Returns input.
        '''
        index = self._ordered_input_names.index('clamp_time')
        return self._inputs[index]

    @property
    def control(self):
        r'''Gets `control` input of Compander.

        ::

            >>> control = 0.0
            >>> source = ugentools.In.ar(bus=0)
            >>> compander = ugentools.Compander.ar(
            ...     control=control,
            ...     source=source,
            ...     )
            >>> compander.control
            0.0

        Returns input.
        '''
        index = self._ordered_input_names.index('control')
        return self._inputs[index]

    @property
    def relax_time(self):
        r'''Gets `relax_time` input of Compander.

        ::

            >>> relax_time = 0.1
            >>> source = ugentools.In.ar(bus=0)
            >>> compander = ugentools.Compander.ar(
            ...     relax_time=relax_time,
            ...     source=source,
            ...     )
            >>> compander.relax_time
            0.1

        Returns input.
        '''
        index = self._ordered_input_names.index('relax_time')
        return self._inputs[index]

    @property
    def slope_above(self):
        r'''Gets `slope_above` input of Compander.

        ::

            >>> slope_above = 1.0
            >>> source = ugentools.In.ar(bus=0)
            >>> compander = ugentools.Compander.ar(
            ...     slope_above=slope_above,
            ...     source=source,
            ...     )
            >>> compander.slope_above
            1.0

        Returns input.
        '''
        index = self._ordered_input_names.index('slope_above')
        return self._inputs[index]

    @property
    def slope_below(self):
        r'''Gets `slope_below` input of Compander.

        ::

            >>> slope_below = 1.0
            >>> source = ugentools.In.ar(bus=0)
            >>> compander = ugentools.Compander.ar(
            ...     slope_below=slope_below,
            ...     source=source,
            ...     )
            >>> compander.slope_below
            1.0

        Returns input.
        '''
        index = self._ordered_input_names.index('slope_below')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Compander.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> compander = ugentools.Compander.ar(
            ...     source=source,
            ...     )
            >>> compander.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=CalculationRate.AUDIO,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def threshold(self):
        r'''Gets `threshold` input of Compander.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> threshold = 0.5
            >>> compander = ugentools.Compander.ar(
            ...     source=source,
            ...     threshold=threshold,
            ...     )
            >>> compander.threshold
            0.5

        Returns input.
        '''
        index = self._ordered_input_names.index('threshold')
        return self._inputs[index]