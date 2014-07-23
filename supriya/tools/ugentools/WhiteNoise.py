# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class WhiteNoise(UGen):
    r'''White noise unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.WhiteNoise.ar()
        WhiteNoise.ar()

    '''

    ### CLASS VARIABLES ###

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
        r'''Creates an audio-rate white noise unit generator.

        ::

            >>> from supriya.tools import ugentools
            >>> ugentools.WhiteNoise.ar()
            WhiteNoise.ar()

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
        r'''Creates a control-rate white noise unit generator.

        ::

            >>> from supriya.tools import ugentools
            >>> ugentools.WhiteNoise.kr()
            WhiteNoise.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            )
        return ugen