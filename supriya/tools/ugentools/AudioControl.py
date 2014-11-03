# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.Control import Control


class AudioControl(Control):
    r'''A trigger-calculation_rate control ugen.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'UGen Internals'

    __slots__ = ()

    ### INITIALIZER ##

    def __init__(
        self,
        control_names,
        starting_control_index=0,
        ):
        from supriya.tools import synthdeftools
        Control.__init__(
            self,
            control_names,
            calculation_rate=synthdeftools.CalculationRate.AUDIO,
            starting_control_index=starting_control_index,
            )