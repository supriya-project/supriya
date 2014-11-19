# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PV_MagMul import PV_MagMul


class PV_Div(PV_MagMul):
    r'''

    ::

        >>> pv_div = ugentools.PV_Div.(
        ...     buffer_a=None,
        ...     buffer_b=None,
        ...     )
        >>> pv_div

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'buffer_a',
        'buffer_b',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        buffer_a=None,
        buffer_b=None,
        ):
        PV_MagMul.__init__(
            self,
            calculation_rate=calculation_rate,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        buffer_a=None,
        buffer_b=None,
        ):
        r'''Constructs a PV_Div.

        ::

            >>> pv_div = ugentools.PV_Div.new(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     )
            >>> pv_div

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            buffer_a=buffer_a,
            buffer_b=buffer_b,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def buffer_a(self):
        r'''Gets `buffer_a` input of PV_Div.

        ::

            >>> pv_div = ugentools.PV_Div.ar(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     )
            >>> pv_div.buffer_a

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_a')
        return self._inputs[index]

    @property
    def buffer_b(self):
        r'''Gets `buffer_b` input of PV_Div.

        ::

            >>> pv_div = ugentools.PV_Div.ar(
            ...     buffer_a=None,
            ...     buffer_b=None,
            ...     )
            >>> pv_div.buffer_b

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('buffer_b')
        return self._inputs[index]