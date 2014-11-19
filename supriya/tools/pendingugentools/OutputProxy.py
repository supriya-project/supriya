# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class OutputProxy(UGen):
    r'''

    ::

        >>> output_proxy = ugentools.OutputProxy.(
        ...     )
        >>> output_proxy

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
        its_source_ugen=None,
        rate=None,
        ):
        r'''Constructs a OutputProxy.

        ::

            >>> output_proxy = ugentools.OutputProxy.new(
            ...     index=None,
            ...     its_source_ugen=None,
            ...     rate=None,
            ...     )
            >>> output_proxy

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            index=index,
            its_source_ugen=its_source_ugen,
            rate=rate,
            )
        return ugen
