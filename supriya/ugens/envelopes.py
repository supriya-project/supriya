import collections

from supriya import CalculationRate
from supriya.synthdefs import UGen


class Done(UGen):
    """
    Triggers when `source` sets its `done` flag.

    ::

        >>> source = supriya.ugens.Line.kr()
        >>> done = supriya.ugens.Done.kr(
        ...     source=source,
        ... )
        >>> done
        Done.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL,)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, source=None):
        if not (hasattr(source, "has_done_flag") and source.has_done_flag):
            raise ValueError(repr(source))
        UGen.__init__(self, calculation_rate=calculation_rate, source=source)


class EnvGen(UGen):
    """
    An envelope generator.

    ::

        >>> envelope = supriya.synthdefs.Envelope.percussive()
        >>> supriya.ugens.EnvGen.ar(envelope=envelope)
        EnvGen.ar()

    """

    ### CLASS VARIABLES ###

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


class Free(UGen):
    """
    Frees the node at `node_id` when triggered by `trigger`.

    ::

        >>> node_id = 1000
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> free = supriya.ugens.Free.kr(
        ...     node_id=node_id,
        ...     trigger=trigger,
        ... )
        >>> free
        Free.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("trigger", 0.0), ("node_id", None)]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class FreeSelf(UGen):
    """
    Frees the enclosing synth when triggered by `trigger`.

    ::

        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> free_self = supriya.ugens.FreeSelf.kr(
        ...     trigger=trigger,
        ... )
        >>> free_self
        FreeSelf.kr()

    """

    _ordered_input_names = collections.OrderedDict([("trigger", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class FreeSelfWhenDone(UGen):
    """
    Frees the enclosing synth when `source` sets its `done` flag.

    ::

        >>> source = supriya.ugens.Line.kr()
        >>> free_self_when_done = supriya.ugens.FreeSelfWhenDone.kr(
        ...     source=source,
        ... )
        >>> free_self_when_done
        FreeSelfWhenDone.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL,)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, source=None):
        if not (hasattr(source, "has_done_flag") and source.has_done_flag):
            raise ValueError(repr(source))
        UGen.__init__(self, calculation_rate=calculation_rate, source=source)


class Pause(UGen):
    """
    Pauses the node at `node_id` when triggered by `trigger`.

    ::

        >>> node_id = 1000
        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> pause = supriya.ugens.Pause.kr(
        ...     node_id=node_id,
        ...     trigger=trigger,
        ... )
        >>> pause
        Pause.kr()

    """

    _ordered_input_names = collections.OrderedDict(
        [("trigger", None), ("node_id", None)]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class PauseSelf(UGen):
    """
    Pauses the enclosing synth when triggered by `trigger`.

    ::

        >>> trigger = supriya.ugens.Impulse.kr(frequency=1.0)
        >>> pause_self = supriya.ugens.PauseSelf.kr(
        ...     trigger=trigger,
        ... )
        >>> pause_self
        PauseSelf.kr()

    """

    _ordered_input_names = collections.OrderedDict([("trigger", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL,)


class PauseSelfWhenDone(UGen):
    """
    Pauses the enclosing synth when `source` sets its `done` flag.

    ::

        >>> source = supriya.ugens.Line.kr()
        >>> pause_self_when_done = supriya.ugens.PauseSelfWhenDone.kr(
        ...     source=source,
        ... )
        >>> pause_self_when_done
        PauseSelfWhenDone.kr()

    """

    ### CLASS VARIABLES ###

    _ordered_input_names = collections.OrderedDict([("source", None)])
    _valid_calculation_rates = (CalculationRate.CONTROL,)

    ### INITIALIZER ###

    def __init__(self, calculation_rate=None, source=None):
        if not (hasattr(source, "has_done_flag") and source.has_done_flag):
            raise ValueError(repr(source))
        UGen.__init__(self, calculation_rate=calculation_rate, source=source)


class Linen(UGen):
    """
    A simple line generating unit generator.

    ::

        >>> supriya.ugens.Linen.kr()
        Linen.kr()

    """

    _has_done_flag = True
    _ordered_input_names = collections.OrderedDict(
        [
            ("gate", 1.0),
            ("attack_time", 0.01),
            ("sustain_level", 1.0),
            ("release_time", 1.0),
            ("done_action", 0),
        ]
    )
    _valid_calculation_rates = (CalculationRate.CONTROL,)
