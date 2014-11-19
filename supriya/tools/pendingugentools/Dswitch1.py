# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dswitch1(DUGen):
    r'''

    ::

        >>> dswitch_1 = ugentools.Dswitch1.(
        ...     index=None,
        ...     list=None,
        ...     )
        >>> dswitch_1

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'list',
        'index',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        index=None,
        list=None,
        ):
        DUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            index=index,
            list=list,
            )

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

    ### PUBLIC PROPERTIES ###

    @property
    def index(self):
        r'''Gets `index` input of Dswitch1.

        ::

            >>> dswitch_1 = ugentools.Dswitch1.ar(
            ...     index=None,
            ...     list=None,
            ...     )
            >>> dswitch_1.index

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('index')
        return self._inputs[index]

    @property
    def list(self):
        r'''Gets `list` input of Dswitch1.

        ::

            >>> dswitch_1 = ugentools.Dswitch1.ar(
            ...     index=None,
            ...     list=None,
            ...     )
            >>> dswitch_1.list

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('list')
        return self._inputs[index]