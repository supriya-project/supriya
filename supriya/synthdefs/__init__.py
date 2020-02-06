"""
Tools for constructing and compiling synthesizer definitions (SynthDefs).
"""
from .mixins import OutputProxy, UGenArray, UGenMethodMixin  # noqa
from .bases import (  # noqa
    MultiOutUGen,
    PureMultiOutUGen,
    PureUGen,
    UGen,
    UGenMeta,
    WidthFirstUGen,
    BinaryOpUGen,
    UnaryOpUGen,
)
from .compilers import SynthDefCompiler, SynthDefDecompiler  # noqa
from .controls import (  # noqa
    AudioControl,
    Control,
    LagControl,
    Parameter,
    TrigControl,
)
from .factories import SynthDefFactory  # noqa
from .grapher import SynthDefGrapher  # noqa
from .synthdefs import SynthDef, UGenSortBundle  # noqa

from .Envelope import Envelope  # noqa
from .Range import Range  # noqa
from .SuperColliderSynthDef import SuperColliderSynthDef  # noqa
from .SynthDefBuilder import SynthDefBuilder  # noqa
