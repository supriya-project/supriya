# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class ClearBuf(WidthFirstUGen):
    r'''

    ::

        >>> clear_buf = ugentools.ClearBuf.(
        ...     buf=None,
        ...     )
        >>> clear_buf

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buf',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buf=None,
        ):
        WidthFirstUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            buf=buf,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buf=None,
        ):
        r'''Constructs a ClearBuf.

        ::

            >>> clear_buf = ugentools.ClearBuf.new(
            ...     buf=None,
            ...     )
            >>> clear_buf

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buf=buf,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buf(self):
        r'''Gets `buf` input of ClearBuf.

        ::

            >>> clear_buf = ugentools.ClearBuf.ar(
            ...     buf=None,
            ...     )
            >>> clear_buf.buf

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buf')
        return self._inputs[index]