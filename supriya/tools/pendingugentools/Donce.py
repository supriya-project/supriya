# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Donce(DUGen):
    r'''

    ::

        >>> donce = ugentools.Donce.(
        ...     source=None,
        ...     )
        >>> donce

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
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        source=None,
        ):
        r'''Constructs a Donce.

        ::

            >>> donce = ugentools.Donce.new(
            ...     source=None,
            ...     )
            >>> donce

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of Donce.

        ::

            >>> donce = ugentools.Donce.ar(
            ...     source=None,
            ...     )
            >>> donce.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]