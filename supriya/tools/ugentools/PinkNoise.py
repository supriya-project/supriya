# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class PinkNoise(UGen):
    r'''A pink noise unit generator.

    ::

        >>> ugentools.PinkNoise.ar()
        PinkNoise.ar()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Noise UGens'

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        ):
        UGen.__init__(
            self,
            rate=rate,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        ):
        r'''Creates an audio-rate pink noise unit generator.

        ::

            >>> ugentools.PinkNoise.ar()
            PinkNoise.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        ):
        r'''Creates a control-rate pink noise unit generator.

        ::

            >>> ugentools.PinkNoise.kr()
            PinkNoise.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            )
        return ugen