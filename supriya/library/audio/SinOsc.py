from supriya.tools.audio.UGen import UGen
from supriya.tools.audio import ArgumentSpecification


class SinOsc(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        ArgumentSpecification('freq', 440),
        ArgumentSpecification('phase', 0),
        )
