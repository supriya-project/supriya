# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.MultiOutUGen import MultiOutUGen


class Pan2(MultiOutUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Spatialization UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'position',
        'level',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        level=1.,
        position=0.,
        rate=None,
        source=None,
        ):
        MultiOutUGen.__init__(
            self,
            channel_count=2,
            level=level,
            position=position,
            rate=rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        level=1.,
        position=0.,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            source=source,
            position=position,
            level=level,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def level(self):
        r'''Gets `level` input of Pan2.

        ::

            >>> level = None
            >>> pan_2 = ugentools.Pan2.ar(
            ...     level=level,
            ...     )
            >>> pan_2.level

        Returns input.
        '''
        index = self._ordered_input_names.index('level')
        return self._inputs[index]

    @property
    def position(self):
        r'''Gets `position` input of Pan2.

        ::

            >>> position = None
            >>> pan_2 = ugentools.Pan2.ar(
            ...     position=position,
            ...     )
            >>> pan_2.position

        Returns input.
        '''
        index = self._ordered_input_names.index('position')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Pan2.

        ::

            >>> source = None
            >>> pan_2 = ugentools.Pan2.ar(
            ...     source=source,
            ...     )
            >>> pan_2.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]