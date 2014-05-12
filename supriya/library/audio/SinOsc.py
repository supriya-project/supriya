from supriya.library.audio.UGen import UGen
from supriya.library.audio import ArgumentSpecification


class SinOsc(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        ArgumentSpecification('freq', 440),
        ArgumentSpecification('phase', 0),
        )
