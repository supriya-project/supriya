# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Index import Index


class DetectIndex(Index):
    r'''

    ::

        >>> detect_index = ugentools.DetectIndex.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        >>> detect_index
        DetectIndex.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        source=None,
        ):
        Index.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        buffer_id=buffer_id,
        source=source,
        ):
        r'''Constructs an audio-rate DetectIndex.

        ::

            >>> detect_index = ugentools.DetectIndex.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> detect_index
            DetectIndex.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        buffer_id=buffer_id,
        source=source,
        ):
        r'''Constructs a control-rate DetectIndex.

        ::

            >>> detect_index = ugentools.DetectIndex.kr(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> detect_index
            DetectIndex.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of DetectIndex.

        ::

            >>> detect_index = ugentools.DetectIndex.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> detect_index.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of DetectIndex.

        ::

            >>> detect_index = ugentools.DetectIndex.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> detect_index.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]