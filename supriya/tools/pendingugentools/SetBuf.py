# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class SetBuf(WidthFirstUGen):
    r'''

    ::

        >>> set_buf = ugentools.SetBuf.(
        ...     buf=None,
        ...     offset=0,
        ...     values=None,
        ...     )
        >>> set_buf

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buf',
        'values',
        'offset',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buf=None,
        offset=0,
        values=None,
        ):
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buf=buf,
            offset=offset,
            values=values,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buf=None,
        offset=0,
        values=None,
        ):
        r'''Constructs a SetBuf.

        ::

            >>> set_buf = ugentools.SetBuf.new(
            ...     buf=None,
            ...     offset=0,
            ...     values=None,
            ...     )
            >>> set_buf

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buf=buf,
            offset=offset,
            values=values,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buf(self):
        r'''Gets `buf` input of SetBuf.

        ::

            >>> set_buf = ugentools.SetBuf.ar(
            ...     buf=None,
            ...     offset=0,
            ...     values=None,
            ...     )
            >>> set_buf.buf

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buf')
        return self._inputs[index]

    @property
    def offset(self):
        r'''Gets `offset` input of SetBuf.

        ::

            >>> set_buf = ugentools.SetBuf.ar(
            ...     buf=None,
            ...     offset=0,
            ...     values=None,
            ...     )
            >>> set_buf.offset

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('offset')
        return self._inputs[index]

    @property
    def values(self):
        r'''Gets `values` input of SetBuf.

        ::

            >>> set_buf = ugentools.SetBuf.ar(
            ...     buf=None,
            ...     offset=0,
            ...     values=None,
            ...     )
            >>> set_buf.values

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('values')
        return self._inputs[index]