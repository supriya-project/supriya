from supriya.tools.audiotools.Argument import Argument
from supriya.tools.audiotools.UGen import UGen


class DelayC(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('source'),
        Argument('maximum_delay_time', 0.2),
        Argument('delay_time', 0.2),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        delay_time=0.2,
        maximum_delay_time=0.2,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            delay_time=delay_time,
            maximum_delay_time=maximum_delay_time,
            source=source,
            )
