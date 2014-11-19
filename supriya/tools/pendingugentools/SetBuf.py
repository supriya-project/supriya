# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.WidthFirstUGen import WidthFirstUGen


class SetBuf(WidthFirstUGen):
    r'''

    ::

        >>> set_buf = ugentools.SetBuf.(
        ...     )
        >>> set_buf

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
