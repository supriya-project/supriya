# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class K2A(PureUGen):
    r'''Control rate to audio rate converter unit generator.

    ::

        >>> source = ugentools.SinOsc.kr()
        >>> k_2_a = ugentools.K2A.ar(
        ...     source=source,
        ...     )
        >>> k_2_a
        K2A.ar()

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
    def ar(
        cls,
        source=None,
        ):
        r'''Constructs a control-rate to audio-rate converter.

        ::

            >>> source = ugentools.SinOsc.kr(frequency=[2, 3])
            >>> ugentools.K2A.ar(
            ...     source=source,
            ...     )
            UGenArray({2})

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        r'''Gets `source` input of K2A.

        ::

            >>> source = ugentools.WhiteNoise.kr()
            >>> k_2_a = ugentools.K2A.ar(
            ...     source=source,
            ...     )
            >>> k_2_a.source
            OutputProxy(
                source=WhiteNoise(
                    rate=<Rate.CONTROL: 1>
                    ),
                output_index=0
                )

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]