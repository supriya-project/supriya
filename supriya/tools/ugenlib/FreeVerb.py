from supriya.tools.audiolib.Argument import Argument
from supriya.tools.audiolib.UGen import UGen


class FreeVerb(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        Argument('source'),
        Argument('mix', 0.33),
        Argument('room_size', 0.5),
        Argument('damping', 0.5),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        damping=0.5,
        mix=0.33,
        room_size=0.5,
        source=None,
        ):
        UGen.__init__(
            self,
            calculation_rate=calculation_rate,
            damping=damping,
            mix=mix,
            room_size=room_size,
            source=source,
            )
