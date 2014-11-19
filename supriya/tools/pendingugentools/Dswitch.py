# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Dswitch1 import Dswitch1


class Dswitch(Dswitch1):
    r'''

    ::

        >>> dswitch = ugentools.Dswitch.(
        ...     )
        >>> dswitch

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
        r'''Constructs a Dswitch.

        ::

            >>> dswitch = ugentools.Dswitch.new(
            ...     index=None,
            ...     list=None,
            ...     )
            >>> dswitch

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
