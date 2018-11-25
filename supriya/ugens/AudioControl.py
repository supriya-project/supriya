from supriya import CalculationRate
from supriya.ugens.Control import Control


class AudioControl(Control):
    """
    A trigger-rate control ugen.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "UGen Internals"

    ### INITIALIZER ##

    def __init__(self, parameters, calculation_rate=None, starting_control_index=0):
        Control.__init__(
            self,
            parameters,
            calculation_rate=CalculationRate.AUDIO,
            starting_control_index=starting_control_index,
        )
