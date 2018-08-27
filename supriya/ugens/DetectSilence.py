import collections
from supriya import CalculationRate
from supriya.ugens.Filter import Filter


class DetectSilence(Filter):
    """
    Evaluates `done_action` when input falls below `threshold`.

    ::

        >>> source = supriya.ugens.WhiteNoise.ar()
        >>> source *= supriya.ugens.Line.kr(start=1, stop=0)
        >>> detect_silence = supriya.ugens.DetectSilence.kr(
        ...     done_action=DoneAction.FREE_SYNTH,
        ...     source=source,
        ...     threshold=0.0001,
        ...     time=1.0,
        ...     )
        >>> detect_silence
        DetectSilence.kr()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Envelope Utility UGens'

    _ordered_input_names = collections.OrderedDict([
        ('source', None),
        ('threshold', 0.0001),
        ('time', 0.1),
        ('done_action', 0),
    ])

    _valid_calculation_rates = (
        CalculationRate.AUDIO,
        CalculationRate.CONTROL,
    )

    ### PRIVATE METHODS ###

    def _optimize_graph(self, sort_bundles):
        pass
