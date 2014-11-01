# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class Linen(UGen):
    r'''A simple line generating unit generator.

    ::

        >>> from supriya.tools import ugentools
        >>> ugentools.Linen.kr()
        Linen.kr()

    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    __slots__ = ()

    _ordered_input_names = (
        'gate',
        'attack_time',
        'sustain_level',
        'release_time',
        'done_action',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        attack_time=0.01,
        done_action=0,
        gate=1.,
        rate=None,
        release_time=1.,
        sustain_level=1.,
        ):
        UGen.__init__(
            self,
            attack_time=attack_time,
            done_action=done_action,
            gate=gate,
            rate=rate,
            release_time=release_time,
            sustain_level=sustain_level,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def kr(
        cls,
        attack_time=0.01,
        done_action=0,
        gate=1.,
        rate=None,
        release_time=1.,
        sustain_level=1.,
        ):
        r'''Creates an audio-rate line generator.

        ::

            >>> from supriya.tools import synthdeftools
            >>> from supriya.tools import ugentools
            >>> ugentools.Linen.kr(
            ...     attack_time=5.5,
            ...     done_action=synthdeftools.DoneAction.FREE_SYNTH,
            ...     release_time=0.5,
            ...     sustain_level=0.1,
            ...     )
            Linen.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            attack_time=attack_time,
            done_action=done_action,
            gate=gate,
            rate=rate,
            release_time=release_time,
            sustain_level=sustain_level,
            )
        return ugen

    ### PUBLIC PROPERTIES ###

    @property
    def attack_time(self):
        r'''Gets `attack_time` input of Linen.

        ::

            >>> attack_time = None
            >>> linen = ugentools.Linen.ar(
            ...     attack_time=attack_time,
            ...     )
            >>> linen.attack_time

        Returns input.
        '''
        index = self._ordered_input_names.index('attack_time')
        return self._inputs[index]

    @property
    def done_action(self):
        r'''Gets `done_action` input of Linen.

        ::

            >>> done_action = None
            >>> linen = ugentools.Linen.ar(
            ...     done_action=done_action,
            ...     )
            >>> linen.done_action

        Returns input.
        '''
        index = self._ordered_input_names.index('done_action')
        return self._inputs[index]

    @property
    def gate(self):
        r'''Gets `gate` input of Linen.

        ::

            >>> gate = None
            >>> linen = ugentools.Linen.ar(
            ...     gate=gate,
            ...     )
            >>> linen.gate

        Returns input.
        '''
        index = self._ordered_input_names.index('gate')
        return self._inputs[index]

    @property
    def release_time(self):
        r'''Gets `release_time` input of Linen.

        ::

            >>> release_time = None
            >>> linen = ugentools.Linen.ar(
            ...     release_time=release_time,
            ...     )
            >>> linen.release_time

        Returns input.
        '''
        index = self._ordered_input_names.index('release_time')
        return self._inputs[index]

    @property
    def sustain_level(self):
        r'''Gets `sustain_level` input of Linen.

        ::

            >>> sustain_level = None
            >>> linen = ugentools.Linen.ar(
            ...     sustain_level=sustain_level,
            ...     )
            >>> linen.sustain_level

        Returns input.
        '''
        index = self._ordered_input_names.index('sustain_level')
        return self._inputs[index]