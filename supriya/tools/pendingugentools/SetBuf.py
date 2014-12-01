# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class SetBuf(WidthFirstUGen):
    r'''

    ::

        >>> set_buf = ugentools.SetBuf.ar(
        ...     buffer_id=buffer_id,
        ...     offset=0,
        ...     values=values,
        ...     )
        >>> set_buf
        SetBuf.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_id',
        'values',
        'offset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_id=None,
        offset=0,
        values=None,
        ):
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            offset=offset,
            values=values,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_id=None,
        offset=0,
        values=None,
        ):
        r'''Constructs a SetBuf.

        ::

            >>> set_buf = ugentools.SetBuf.new(
            ...     buffer_id=buffer_id,
            ...     offset=0,
            ...     values=values,
            ...     )
            >>> set_buf
            SetBuf.new()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            offset=offset,
            values=values,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_id(self):
        r'''Gets `buffer_id` input of SetBuf.

        ::

            >>> set_buf = ugentools.SetBuf.ar(
            ...     buffer_id=buffer_id,
            ...     offset=0,
            ...     values=values,
            ...     )
            >>> set_buf.buffer_id

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_id')
        return self._inputs[index]

    @property
    def offset(self):
        r'''Gets `offset` input of SetBuf.

        ::

            >>> set_buf = ugentools.SetBuf.ar(
            ...     buffer_id=buffer_id,
            ...     offset=0,
            ...     values=values,
            ...     )
            >>> set_buf.offset
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('offset')
        return self._inputs[index]

    @property
    def values(self):
        r'''Gets `values` input of SetBuf.

        ::

            >>> set_buf = ugentools.SetBuf.ar(
            ...     buffer_id=buffer_id,
            ...     offset=0,
            ...     values=values,
            ...     )
            >>> set_buf.values

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('values')
        return self._inputs[index]