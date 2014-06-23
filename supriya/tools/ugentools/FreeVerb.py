# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class FreeVerb(UGen):
    r'''FreeVerb reverb unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> source = ugentools.SoundIn.ar()
        >>> ugentools.FreeVerb.ar(
        ...     source=source,
        ...     )
        FreeVerb.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'mix',
        'room_size',
        'damping',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        damping=0.5,
        mix=0.33,
        room_size=0.5,
        source=None,
        ):
        UGen.__init__(
            self,
            rate=rate,
            damping=damping,
            mix=mix,
            room_size=room_size,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        damping=0.5,
        mix=0.33,
        room_size=0.5,
        source=None,
        ):
        r'''Creates an audio-rate FreeVerb reverb unit.

        ::

            >>> from supriya.tools import ugentools
            >>> source = ugentools.SoundIn.ar(bus=0)
            >>> ugentools.FreeVerb.ar(
            ...     damping=0.5,
            ...     mix=0.33,
            ...     room_size=0.5,
            ...     source=source,
            ...     )
            FreeVerb.ar()

        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            damping=damping,
            mix=mix,
            room_size=room_size,
            source=source,
            )
        return ugen
