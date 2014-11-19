# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dswitch1(DUGen):
    r'''

    ::

        >>> dswitch_1 = ugentools.Dswitch1.(
        ...     )
        >>> dswitch_1

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
        index=None,
        list=None,
        ):
        r'''Constructs a Dswitch1.

        ::

            >>> dswitch_1 = ugentools.Dswitch1.new(
            ...     index=None,
            ...     list=None,
            ...     )
            >>> dswitch_1

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            index=index,
            list=list,
            )
        return ugen
