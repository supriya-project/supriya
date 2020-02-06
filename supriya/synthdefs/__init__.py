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
)
from .controls import (  # noqa
    AudioControl,
    Control,
    LagControl,
    Parameter,
    TrigControl,
)
from .grapher import SynthDefGrapher  # noqa
from .synthdefs import SynthDef, UGenSortBundle  # noqa

from .BinaryOpUGen import BinaryOpUGen  # noqa
from .Envelope import Envelope  # noqa
from .Range import Range  # noqa
from .SuperColliderSynthDef import SuperColliderSynthDef  # noqa
from .SynthDefBuilder import SynthDefBuilder  # noqa
from .SynthDefCompiler import SynthDefCompiler  # noqa
from .SynthDefDecompiler import SynthDefDecompiler  # noqa
from .SynthDefFactory import SynthDefFactory  # noqa
from .UnaryOpUGen import UnaryOpUGen  # noqa
