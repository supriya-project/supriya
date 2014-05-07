from supriya.synthdefs.UGen import UGen
from supriya.synthdefs import ArgumentSpecification


class Line(UGen):
    
    ### CLASS VARIABLES ###

    _argument_specifications = (
        ArgumentSpecification('start', 0),
        ArgumentSpecification('end', 1),
        ArgumentSpecification('dur', 1),
        ArgumentSpecification('doneAction', 0),
        )
