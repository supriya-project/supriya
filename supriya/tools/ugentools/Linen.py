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