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

    __documentation_section__ = 'Reverb UGens'

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

    ### PUBLIC PROPERTIES ###

    @property
    def damping(self):
        r'''Gets `damping` input of FreeVerb.

        ::

            >>> damping = None
            >>> free_verb = ugentools.FreeVerb.ar(
            ...     damping=damping,
            ...     )
            >>> free_verb.damping

        Returns input.
        '''
        index = self._ordered_input_names.index('damping')
        return self._inputs[index]

    @property
    def mix(self):
        r'''Gets `mix` input of FreeVerb.

        ::

            >>> mix = None
            >>> free_verb = ugentools.FreeVerb.ar(
            ...     mix=mix,
            ...     )
            >>> free_verb.mix

        Returns input.
        '''
        index = self._ordered_input_names.index('mix')
        return self._inputs[index]

    @property
    def room_size(self):
        r'''Gets `room_size` input of FreeVerb.

        ::

            >>> room_size = None
            >>> free_verb = ugentools.FreeVerb.ar(
            ...     room_size=room_size,
            ...     )
            >>> free_verb.room_size

        Returns input.
        '''
        index = self._ordered_input_names.index('room_size')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of FreeVerb.

        ::

            >>> source = None
            >>> free_verb = ugentools.FreeVerb.ar(
            ...     source=source,
            ...     )
            >>> free_verb.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]