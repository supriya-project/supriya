# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dgeom(DUGen):
    r'''

    ::

        >>> dgeom = ugentools.Dgeom.(
        ...     )
        >>> dgeom

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
        grow=2,
        length="float('inf')",
        start=1,
        ):
        r'''Constructs a Dgeom.

        ::

            >>> dgeom = ugentools.Dgeom.new(
            ...     grow=2,
            ...     length="float('inf')",
            ...     start=1,
            ...     )
            >>> dgeom

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            grow=grow,
            length=length,
            start=start,
            )
        return ugen
