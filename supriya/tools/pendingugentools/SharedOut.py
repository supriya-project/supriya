# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.AbstractOut import AbstractOut


class SharedOut(AbstractOut):
    r'''

    ::

        >>> shared_out = ugentools.SharedOut.(
        ...     bus=None,
        ...     source=None,
        ...     )
        >>> shared_out

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        'source',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=None,
        source=None,
        ):
        AbstractOut.__init__(
            self,
            calculation_rate=calculation_rate,
            bus=bus,
            source=source,
            )

    ### PUBLIC METHODS ###

    # def isOutputUGen(): ...

    @classmethod
    def kr(
        cls,
        bus=None,
        source=None,
        ):
        r'''Constructs a control-rate SharedOut.

        ::

            >>> shared_out = ugentools.SharedOut.kr(
            ...     bus=None,
            ...     source=None,
            ...     )
            >>> shared_out

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            source=source,
            )
        return ugen

    # def numFixedArgs(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        r'''Gets `bus` input of SharedOut.

        ::

            >>> shared_out = ugentools.SharedOut.ar(
            ...     bus=None,
            ...     source=None,
            ...     )
            >>> shared_out.bus

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of SharedOut.

        ::

            >>> shared_out = ugentools.SharedOut.ar(
            ...     bus=None,
            ...     source=None,
            ...     )
            >>> shared_out.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]