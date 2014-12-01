# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class DegreeToKey(PureUGen):
    r'''

    ::

        >>> source = ugentools.In.ar(bus=0)
        >>> degree_to_key = ugentools.DegreeToKey.ar(
        ...     buffer_id=buffer_id,
        ...     octave=12,
        ...     source=source,
        ...     )
        >>> degree_to_key
        DegreeToKey.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        'octave',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        octave=12,
        source=None,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            octave=octave,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=None,
        octave=12,
        source=None,
        ):
        r'''Constructs an audio-rate DegreeToKey.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> degree_to_key = ugentools.DegreeToKey.ar(
            ...     buffer_id=buffer_id,
            ...     octave=12,
            ...     source=source,
            ...     )
            >>> degree_to_key
            DegreeToKey.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            octave=octave,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=None,
        octave=12,
        source=None,
        ):
        r'''Constructs a control-rate DegreeToKey.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> degree_to_key = ugentools.DegreeToKey.kr(
            ...     buffer_id=buffer_id,
            ...     octave=12,
            ...     source=source,
            ...     )
            >>> degree_to_key
            DegreeToKey.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            octave=octave,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of DegreeToKey.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> degree_to_key = ugentools.DegreeToKey.ar(
            ...     buffer_id=buffer_id,
            ...     octave=12,
            ...     source=source,
            ...     )
            >>> degree_to_key.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def octave(self):
        r'''Gets `octave` input of DegreeToKey.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> degree_to_key = ugentools.DegreeToKey.ar(
            ...     buffer_id=buffer_id,
            ...     octave=12,
            ...     source=source,
            ...     )
            >>> degree_to_key.octave
            12.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('octave')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of DegreeToKey.

        ::

            >>> source = ugentools.In.ar(bus=0)
            >>> degree_to_key = ugentools.DegreeToKey.ar(
            ...     buffer_id=buffer_id,
            ...     octave=12,
            ...     source=source,
            ...     )
            >>> degree_to_key.source
            OutputProxy(
                source=In(
                    bus=0.0,
                    calculation_rate=<CalculationRate.AUDIO: 2>,
                    channel_count=1
                    ),
                output_index=0
                )

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]