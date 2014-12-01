# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class SendTrig(UGen):
    r'''

    ::

        >>> send_trig = ugentools.SendTrig.ar(
        ...     id=0,
        ...     source=source,
        ...     value=0,
        ...     )
        >>> send_trig
        SendTrig.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'id',
        'value',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        id=0,
        source=None,
        value=0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            id=id,
            source=source,
            value=value,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        id=0,
        source=source,
        value=0,
        ):
        r'''Constructs an audio-rate SendTrig.

        ::

            >>> send_trig = ugentools.SendTrig.ar(
            ...     id=0,
            ...     source=source,
            ...     value=0,
            ...     )
            >>> send_trig
            SendTrig.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            id=id,
            source=source,
            value=value,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        id=0,
        source=source,
        value=0,
        ):
        r'''Constructs a control-rate SendTrig.

        ::

            >>> send_trig = ugentools.SendTrig.kr(
            ...     id=0,
            ...     source=source,
            ...     value=0,
            ...     )
            >>> send_trig
            SendTrig.kr()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        calculation_rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            id=id,
            source=source,
            value=value,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def id(self):
        r'''Gets `id` input of SendTrig.

        ::

            >>> send_trig = ugentools.SendTrig.ar(
            ...     id=0,
            ...     source=source,
            ...     value=0,
            ...     )
            >>> send_trig.id
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('id')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of SendTrig.

        ::

            >>> send_trig = ugentools.SendTrig.ar(
            ...     id=0,
            ...     source=source,
            ...     value=0,
            ...     )
            >>> send_trig.source

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]

    @property
    def value(self):
        r'''Gets `value` input of SendTrig.

        ::

            >>> send_trig = ugentools.SendTrig.ar(
            ...     id=0,
            ...     source=source,
            ...     value=0,
            ...     )
            >>> send_trig.value
            0.0

        Returns ugen input.
        '''
        index = self._ordered_input_names.index('value')
        return self._inputs[index]