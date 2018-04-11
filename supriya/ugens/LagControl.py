from supriya.ugens.Control import Control
from supriya.ugens.MultiOutUGen import MultiOutUGen


class LagControl(Control):
    """
    A lagged control-rate control ugen.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'UGen Internals'

    __slots__ = ()

    _ordered_input_names = (
        'lags',
        )

    _unexpanded_input_names = (
        'lags',
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        parameters,
        calculation_rate=None,
        starting_control_index=0,
        ):
        from supriya.tools import synthdeftools
        coerced_parameters = []
        for parameter in parameters:
            if not isinstance(parameter, synthdeftools.Parameter):
                parameter = synthdeftools.Parameter(name=parameter, value=0)
            coerced_parameters.append(parameter)
        self._parameters = tuple(coerced_parameters)
        lags = []
        for parameter in self._parameters:
            lag = parameter.lag or 0.
            lags.extend([lag] * len(parameter))
        MultiOutUGen.__init__(
            self,
            channel_count=len(self),
            calculation_rate=calculation_rate,
            special_index=starting_control_index,
            lags=lags,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def lags(self):
        """
        Gets `lags` input of LagControl.

        Returns ugen input.
        """
        index = self._ordered_input_names.index('lags')
        return tuple(self._inputs[index:])
