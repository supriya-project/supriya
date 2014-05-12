from supriya.tools.audio.UGen import UGen
from supriya.tools.audio import ArgumentSpecification


class Line(UGen):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _argument_specifications = (
        ArgumentSpecification('start', 0),
        ArgumentSpecification('end', 1),
        ArgumentSpecification('dur', 1),
        ArgumentSpecification('doneAction', 0),
        )
