# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class ClearBuf(WidthFirstUGen):
    r'''

    ::

        >>> clear_buf = ugentools.ClearBuf.(
        ...     )
        >>> clear_buf

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = ()

    _valid_calculation_rates = None

    ### INITIALIZER ###

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
