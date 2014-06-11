# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.Argument import Argument
from supriya.tools.synthdeftools.UGen import UGen


class EnvGen(UGen):
    r'''An envelope generator.

    ::

        >>> from supriya.tools import synthdeftools
        >>> envelope = synthdeftools.Envelope.percussive()
        >>> envelope_generator = synthdeftools.EnvGen.ar(envelope=envelope)
        >>> envelope_generator
        EnvGen.ar()

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('gate'),
        Argument('level_scale'),
        Argument('level_bias'),
        Argument('time_scale'),
        Argument('done_action'),
        Argument('envelope'),
        )

    _unexpanded_argument_names = (
        'envelope',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        done_action=0,
        envelope=None,
        gate=1.0,
        level_bias=0.0,
        level_scale=1.0,
        time_scale=1.0,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            done_action=done_action,
            envelope=envelope,
            gate=gate,
            level_bias=level_bias,
            level_scale=level_scale,
            time_scale=time_scale,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        done_action=0,
        envelope=None,
        **kwargs
        ):
        from supriya.tools import synthdeftools
        done_action = synthdeftools.DoneAction.from_expr(done_action)
        if envelope is None:
            envelope = synthdeftools.Envelope()
        assert isinstance(envelope, synthdeftools.Envelope)
        envelope = tuple(envelope)
        ugen = cls._new(
            calculation_rate=synthdeftools.CalculationRate.AUDIO,
            special_index=0,
            done_action=done_action,
            envelope=envelope,
            **kwargs
            )
        return ugen
