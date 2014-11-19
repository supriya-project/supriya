# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.LPZ2 import LPZ2


class HPZ2(LPZ2):
    r'''

    ::

        >>> hpz_2 = ugentools.HPZ2.(
        ...     source=None,
        ...     )
        >>> hpz_2

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
        LPZ2.__init__(
            self,
            calculation_rate=calculation_rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        r'''Constructs an audio-rate HPZ2.

        ::

            >>> hpz_2 = ugentools.HPZ2.ar(
            ...     source=None,
            ...     )
            >>> hpz_2

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    # def coeffs(): ...

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        r'''Constructs a control-rate HPZ2.

        ::

            >>> hpz_2 = ugentools.HPZ2.kr(
            ...     source=None,
            ...     )
            >>> hpz_2

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            source=source,
            )
        return ugen

    # def magResponse(): ...

    # def magResponse2(): ...

    # def magResponse5(): ...

    # def magResponseN(): ...

    # def scopeResponse(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of HPZ2.

        ::

            >>> hpz_2 = ugentools.HPZ2.ar(
            ...     source=None,
            ...     )
            >>> hpz_2.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]