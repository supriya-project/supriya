import collections

from supriya import CalculationRate
from supriya.ugens.UGen import UGen


class EnvGen(UGen):
    """
    An envelope generator.

    ::

        >>> envelope = supriya.synthdefs.Envelope.percussive()
        >>> supriya.ugens.EnvGen.ar(envelope=envelope)
        EnvGen.ar()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Envelope Utility UGens"

    _has_done_flag = True

    _ordered_input_names = collections.OrderedDict(
        [
            ("gate", 1.0),
            ("level_scale", 1.0),
            ("level_bias", 0.0),
            ("time_scale", 1.0),
            ("done_action", 0.0),
            ("envelope", None),
        ]
    )

    _unexpanded_input_names = ("envelope",)

    _valid_calculation_rates = (CalculationRate.AUDIO, CalculationRate.CONTROL)

    ### PRIVATE METHODS ###

    @classmethod
    def _new_expanded(
        cls,
        calculation_rate=None,
        done_action=None,
        envelope=None,
        gate=1.0,
        level_bias=0.0,
        level_scale=1.0,
        time_scale=1.0,
    ):
        import supriya.synthdefs

        if not isinstance(done_action, supriya.synthdefs.Parameter):
            done_action = supriya.DoneAction.from_expr(done_action)
        if envelope is None:
            envelope = supriya.synthdefs.Envelope()
        assert isinstance(envelope, supriya.synthdefs.Envelope)
        envelope = envelope.serialize()
        return super(EnvGen, cls)._new_expanded(
            calculation_rate=calculation_rate,
            done_action=done_action,
            envelope=envelope,
            gate=gate,
            level_bias=level_bias,
            level_scale=level_scale,
            time_scale=time_scale,
        )
