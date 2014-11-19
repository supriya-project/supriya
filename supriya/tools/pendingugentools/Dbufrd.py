# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dbufrd(DUGen):
    r'''

    ::

        >>> dbufrd = ugentools.Dbufrd.(
        ...     )
        >>> dbufrd

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
        buffer_id=0,
        loop=1,
        phase=0,
        ):
        r'''Constructs a Dbufrd.

        ::

            >>> dbufrd = ugentools.Dbufrd.new(
            ...     buffer_id=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufrd

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            loop=loop,
            phase=phase,
            )
        return ugen
