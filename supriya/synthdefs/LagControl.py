import collections

from .Control import Control
from .MultiOutUGen import MultiOutUGen


class LagControl(Control):
    """
    A lagged control-rate control ugen.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "UGen Internals"

    _ordered_input_names = collections.OrderedDict([("lags", None)])

    _unexpanded_input_names = ("lags",)

    ### INITIALIZER ###

    def __init__(self, parameters, calculation_rate=None, starting_control_index=0):
        import supriya.synthdefs

        coerced_parameters = []
        for parameter in parameters:
            if not isinstance(parameter, supriya.synthdefs.Parameter):
                parameter = supriya.synthdefs.Parameter(name=parameter, value=0)
            coerced_parameters.append(parameter)
        self._parameters = tuple(coerced_parameters)
        lags = []
        for parameter in self._parameters:
            lag = parameter.lag or 0.0
            lags.extend([lag] * len(parameter))
        MultiOutUGen.__init__(
            self,
            channel_count=len(self),
            calculation_rate=calculation_rate,
            special_index=starting_control_index,
            lags=lags,
        )
