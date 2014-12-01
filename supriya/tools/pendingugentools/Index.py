# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class Index(PureUGen):
    r'''

    ::

        >>> index = ugentools.Index.ar(
        ...     buffer_id=buffer_id,
        ...     source=source,
        ...     )
        >>> index
        Index.ar()

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
        PureUGen.__init__(
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
        r'''Constructs an audio-rate Index.

        ::

            >>> index = ugentools.Index.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> index
            Index.ar()

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
        r'''Constructs a control-rate Index.

        ::

            >>> index = ugentools.Index.kr(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> index
            Index.kr()

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
        r'''Gets `buffer_id` input of Index.

        ::

            >>> index = ugentools.Index.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> index.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Index.

        ::

            >>> index = ugentools.Index.ar(
            ...     buffer_id=buffer_id,
            ...     source=source,
            ...     )
            >>> index.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]