# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class EnvGen(UGen):
    r'''An envelope generator.

    ::

        >>> from supriya.tools import synthdeftools
        >>> from supriya.tools import ugentools
        >>> envelope = synthdeftools.Envelope.percussive()
        >>> ugentools.EnvGen.ar(envelope=envelope)
        EnvGen.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _ordered_input_names = (
        'gate',
        'level_scale',
        'level_bias',
        'time_scale',
        'done_action',
        'envelope',
        )

    _unexpanded_input_names = (
        'envelope',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        rate=None,
        done_action=0,
        envelope=None,
        gate=1.0,
        level_bias=0.0,
        level_scale=1.0,
        time_scale=1.0,
        ):
        UGen.__init__(
            self,
            rate=rate,
            done_action=done_action,
            envelope=envelope,
            gate=gate,
            level_bias=level_bias,
            level_scale=level_scale,
            time_scale=time_scale,
            )

    ### PRIVATE METHODS ###

    @classmethod
    def _new_expanded(
        cls,
        rate=None,
        done_action=None,
        envelope=None,
        ):
        from supriya.tools import synthdeftools
        done_action = synthdeftools.DoneAction.from_expr(done_action)
        if envelope is None:
            envelope = synthdeftools.Envelope()
        assert isinstance(envelope, synthdeftools.Envelope)
        envelope = tuple(envelope)
        return super(EnvGen, cls)._new_expanded(
            rate=rate,
            done_action=done_action,
            envelope=envelope,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        done_action=0,
        envelope=None,
        **kwargs
        ):
        r'''Creates an audio-rate envelope generator.

        ::

            >>> from supriya.tools import synthdeftools
            >>> from supriya.tools import ugentools
            >>> envelope = synthdeftools.Envelope.percussive()
            >>> ugentools.EnvGen.ar(
            ...     envelope=envelope,
            ...     )
            EnvGen.ar()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.AUDIO
        ugen = cls._new_expanded(
            rate=rate,
            done_action=done_action,
            envelope=envelope,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        done_action=0,
        envelope=None,
        **kwargs
        ):
        r'''Creates an control-rate envelope generator.

        ::

            >>> from supriya.tools import synthdeftools
            >>> from supriya.tools import ugentools
            >>> envelope = synthdeftools.Envelope.percussive()
            >>> ugentools.EnvGen.kr(
            ...     envelope=envelope,
            ...     )
            EnvGen.kr()

        Returns unit generator graph.
        '''
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.CONTROL
        ugen = cls._new_expanded(
            rate=rate,
            done_action=done_action,
            envelope=envelope,
            )
        return ugen
