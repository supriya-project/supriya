# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Control import Control


class TrigControl(Control):
    r'''A trigger-rate control ugen.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ##

    def __init__(
        self,
        parameters,
        starting_control_index=0,
        ):
        from supriya.tools import synthdeftools
        Control.__init__(
            self,
            parameters,
            calculation_rate=synthdeftools.CalculationRate.CONTROL,
            starting_control_index=starting_control_index,
            )