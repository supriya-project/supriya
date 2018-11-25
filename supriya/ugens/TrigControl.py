from supriya.ugens.Control import Control


class TrigControl(Control):
    """
    A trigger-rate control ugen.
    """

    ### CLASS VARIABLES ###

    ### INITIALIZER ##

    def __init__(self, parameters, calculation_rate=None, starting_control_index=0):
        import supriya.synthdefs

        Control.__init__(
            self,
            parameters,
            calculation_rate=supriya.CalculationRate.CONTROL,
            starting_control_index=starting_control_index,
        )
