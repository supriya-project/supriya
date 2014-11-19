# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.DUGen import DUGen


class Dpoll(DUGen):
    r'''

    ::

        >>> dpoll = ugentools.Dpoll.(
        ...     )
        >>> dpoll

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
        label=None,
        run=1,
        source=None,
        trigid=-1,
        ):
        r'''Constructs a Dpoll.

        ::

            >>> dpoll = ugentools.Dpoll.new(
            ...     label=None,
            ...     run=1,
            ...     source=None,
            ...     trigid=-1,
            ...     )
            >>> dpoll

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            label=label,
            run=run,
            source=source,
            trigid=trigid,
            )
        return ugen

    # def new1(): ...
