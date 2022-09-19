"""
Tools for constructing and compiling synthesizer definitions (SynthDefs).
"""
from .builders import SynthDefBuilder, synthdef
from .compilers import SynthDefCompiler, SynthDefDecompiler
from .controls import AudioControl, Control, LagControl, Parameter, Range, TrigControl
from .envelopes import Envelope
from .factories import SynthDefFactory
from .grapher import SynthDefGrapher
from .synthdefs import SuperColliderSynthDef, SynthDef, UGenSortBundle

__all__ = [
    "AudioControl",
    "BinaryOpUGen",
    "Control",
    "Envelope",
    "LagControl",
    "MultiOutUGen",
    "OutputProxy",
    "Parameter",
    "PseudoUGen",
    "Range",
    "SuperColliderSynthDef",
    "SynthDef",
    "SynthDefBuilder",
    "SynthDefCompiler",
    "SynthDefDecompiler",
    "SynthDefFactory",
    "SynthDefGrapher",
    "TrigControl",
    "UGenSortBundle",
    "synthdef",
]
