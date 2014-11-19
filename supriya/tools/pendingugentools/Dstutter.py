# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dstutter(DUGen):
    r'''

    ::

        >>> dstutter = ugentools.Dstutter.(
        ...     )
        >>> dstutter

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
        n=None,
        source=None,
        ):
        r'''Constructs a Dstutter.

        ::

            >>> dstutter = ugentools.Dstutter.new(
            ...     n=None,
            ...     source=None,
            ...     )
            >>> dstutter

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            n=n,
            source=source,
            )
        return ugen
