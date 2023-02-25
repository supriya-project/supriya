from pathlib import Path

import platformdirs

from ._version import __version__, __version_info__
from .clocks import AsyncClock, AsyncOfflineClock, Clock, OfflineClock
from .contexts import AsyncServer, Buffer, Bus, Group, Node, Score, Server, Synth
from .enums import (  # noqa
    AddAction,
    CalculationRate,
    DoneAction,
    HeaderFormat,
    SampleFormat,
)
from .io import graph, play, plot, render
from .synthdefs import (
    SynthDef,
    SynthDefBuilder,
    synthdef,
)
from .assets.synthdefs import default
from .scsynth import Options


if not (
    output_path := Path(platformdirs.user_cache_dir("supriya", "supriya"))
).exists():
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except IOError:
        pass

assets_path = Path(__file__).parent / "assets"


__all__ = [
    "AddAction",
    "AsyncClock",
    "AsyncOfflineClock",
    "AsyncServer",
    "Buffer",
    "Bus",
    "CalculationRate",
    "Clock",
    "DoneAction",
    "Group",
    "HeaderFormat",
    "Node",
    "OfflineClock",
    "Options",
    "SampleFormat",
    "Score",
    "Server",
    "Synth",
    "SynthDef",
    "SynthDefBuilder",
    "__version__",
    "__version_info__",
    "default",
    "graph",
    "output_path",
    "play",
    "plot",
    "render",
    "synthdef",
]


del Path
del platformdirs
