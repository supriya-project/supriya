# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Filter import Filter


class Decay2(Filter):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'attack_time',
        'decay_time',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        attack_time=None,
        decay_time=None,
        rate=None,
        source=None,
        ):
        Filter.__init__(
            self,
            attack_time=attack_time,
            decay_time=decay_time,
            rate=rate,
            source=source,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        attack_time=None,
        decay_time=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            attack_time=attack_time,
            decay_time=decay_time,
            rate=rate,
            source=source,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        attack_time=None,
        decay_time=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            attack_time=attack_time,
            decay_time=decay_time,
            rate=rate,
            source=source,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def attack_time(self):
        r'''Gets `attack_time` input of Decay2.

        ::

            >>> attack_time = None
            >>> decay_2 = ugentools.Decay2.ar(
            ...     attack_time=attack_time,
            ...     )
            >>> decay_2.attack_time

        Returns input.
        '''
        index = self._ordered_input_names.index('attack_time')
        return self._inputs[index]

    @property
    def decay_time(self):
        r'''Gets `decay_time` input of Decay2.

        ::

            >>> decay_time = None
            >>> decay_2 = ugentools.Decay2.ar(
            ...     decay_time=decay_time,
            ...     )
            >>> decay_2.decay_time

        Returns input.
        '''
        index = self._ordered_input_names.index('decay_time')
        return self._inputs[index]

    @property
    def source(self):
        r'''Gets `source` input of Decay2.

        ::

            >>> source = None
            >>> decay_2 = ugentools.Decay2.ar(
            ...     source=source,
            ...     )
            >>> decay_2.source

        Returns input.
        '''
        index = self._ordered_input_names.index('source')
        return self._inputs[index]