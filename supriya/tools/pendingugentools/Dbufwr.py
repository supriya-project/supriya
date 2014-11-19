# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dbufwr(DUGen):
    r'''

    ::

        >>> dbufwr = ugentools.Dbufwr.(
        ...     )
        >>> dbufwr

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
        input=0,
        loop=1,
        phase=0,
        ):
        r'''Constructs a Dbufwr.

        ::

            >>> dbufwr = ugentools.Dbufwr.new(
            ...     buffer_id=0,
            ...     input=0,
            ...     loop=1,
            ...     phase=0,
            ...     )
            >>> dbufwr

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_id=buffer_id,
            input=input,
            loop=loop,
            phase=phase,
            )
        return ugen
