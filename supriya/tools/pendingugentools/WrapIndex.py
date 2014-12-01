# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Index import Index


class WrapIndex(Index):
    r'''

    ::

        >>> wrap_index = ugentools.WrapIndex.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        >>> wrap_index
        WrapIndex.ar()

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
        buffer_id=None,
        source=None,
        ):
        r'''Constructs an audio-rate WrapIndex.

        ::

            >>> wrap_index = ugentools.WrapIndex.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> wrap_index
            WrapIndex.ar()

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
        buffer_id=None,
        source=None,
        ):
        r'''Constructs a control-rate WrapIndex.

        ::

            >>> wrap_index = ugentools.WrapIndex.kr(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> wrap_index
            WrapIndex.kr()

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
        r'''Gets `buffer_id` input of WrapIndex.

        ::

            >>> wrap_index = ugentools.WrapIndex.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> wrap_index.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of WrapIndex.

        ::

            >>> wrap_index = ugentools.WrapIndex.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> wrap_index.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]