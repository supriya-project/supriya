# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class DC(PureUGen):
    r'''DC unit generator.

    ::

        >>> ugentools.DC.ar(
        ...     source=0,
        ...     )
        DC.ar()

    ::

        >>> ugentools.DC.ar(
        ...     source=(1, 2, 3),
        ...     )
        UGenArray({3})
        
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
        rate=None,
        source=None,
        ):
        PureUGen.__init__(
            self,
            rate=rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        source=None,
        ):
        r'''Constructs an audio-rate DC generator.

        ::

            >>> ugentools.DC.ar(
            ...     source=0,
            ...     )
            DC.ar()

        Returns ugen graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.CalculationRate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        source=None,
        ):
        r'''Constructs a control-rate DC generator.

        ::

            >>> ugentools.DC.kr(
            ...     source=0,
            ...     )
            DC.kr()

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
        r'''Gets `source` input of DC.

        ::

            >>> source = 0.5
            >>> dc = ugentools.DC.ar(
            ...     source=source,
            ...     )
            >>> dc.source
            0.5

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]