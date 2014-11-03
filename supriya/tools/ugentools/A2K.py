# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class A2K(PureUGen):
    r'''Audio rate to control rate convert unit generator.

    ::

        >>> source = ugentools.SinOsc.ar()
        >>> a_2_k = ugentools.A2K.kr(
        ...     source=source,
        ...     )
        >>> a_2_k
        A2K.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        source=None,
        rate=None,
        ):
        PureUGen.__init__(
            self,
            source=source,
            rate=rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        r'''Constructs an audio-rate to control-rate converter.

        ::

            >>> source = ugentools.SinOsc.ar(frequency=[440, 442])
            >>> ugentools.A2K.kr(
            ...     source=source,
            ...     )
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.CalculationRate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of A2K.

        ::

            >>> source = ugentools.SinOsc.ar()
            >>> a_2_k = ugentools.A2K.kr(
            ...     source=source,
            ...     )
            >>> a_2_k.source
            OutputProxy(
                source=SinOsc(
                    rate=<CalculationRate.AUDIO: 2>,
                    frequency=440.0,
                    phase=0.0
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]