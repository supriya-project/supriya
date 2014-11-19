# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.AbstractIn import AbstractIn


class InTrig(AbstractIn):
    r'''

    ::

        >>> in_trig = ugentools.InTrig.(
        ...     bus=0,
        ...     channel_count=1,
        ...     )
        >>> in_trig

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'bus',
        'channel_count',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        bus=0,
        channel_count=1,
        ):
        AbstractIn.__init__(
            self,
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            )

    ### PUBLIC METHODS ###

    # def isInputUGen(): ...

    @classmethod
    def kr(
        cls,
        bus=0,
        channel_count=1,
        ):
        r'''Constructs a control-rate InTrig.

        ::

            >>> in_trig = ugentools.InTrig.kr(
            ...     bus=0,
            ...     channel_count=1,
            ...     )
            >>> in_trig

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            bus=bus,
            channel_count=channel_count,
            )
        return ugen

    # def newFromDesc(): ...

    ### PUBLIC PROPERTIES ###

    @property
    def bus(self):
        r'''Gets `bus` input of InTrig.

        ::

            >>> in_trig = ugentools.InTrig.ar(
            ...     bus=0,
            ...     channel_count=1,
            ...     )
            >>> in_trig.bus

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('bus')
        return self._inputs[index]

    @property
    def channel_count(self):
        r'''Gets `channel_count` input of InTrig.

        ::

            >>> in_trig = ugentools.InTrig.ar(
            ...     bus=0,
            ...     channel_count=1,
            ...     )
            >>> in_trig.channel_count

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('channel_count')
        return self._inputs[index]