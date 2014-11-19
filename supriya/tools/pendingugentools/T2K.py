# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.A2K import A2K


class T2K(A2K):
    r'''

    ::

        >>> t_2_k = ugentools.T2K.(
        ...     source=None,
        ...     )
        >>> t_2_k

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        source=None,
        ):
        A2K.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        r'''Constructs a control-rate T2K.

        ::

            >>> t_2_k = ugentools.T2K.kr(
            ...     source=None,
            ...     )
            >>> t_2_k

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of T2K.

        ::

            >>> t_2_k = ugentools.T2K.ar(
            ...     source=None,
            ...     )
            >>> t_2_k.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]