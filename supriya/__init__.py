from pathlib import Path

import platformdirs

from ._version import __version__, __version_info__
from .clocks import (
    AsyncClock,
    AsyncOfflineClock,
    BaseClock,
    Clock,
    ClockContext,
    OfflineClock,
)
from .contexts import (
    AsyncServer,
    BaseServer,
    Buffer,
    BufferGroup,
    Bus,
    BusGroup,
    Context,
    Group,
    Node,
    Score,
    Server,
    Synth,
)
from .enums import (  # noqa
    AddAction,
    CalculationRate,
    DoneAction,
    HeaderFormat,
    SampleFormat,
)
from .io import graph, play, plot, render
from .osc import OscBundle, OscCallback, OscMessage
from .patterns import Pattern
from .synthdefs import (
    SynthDef,
    SynthDefBuilder,
    synthdef,
)
from .ugens import UGen, UGenArray, UGenMethodMixin
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
    "BaseClock",
    "BaseServer",
    "Buffer",
    "BufferGroup",
    "Bus",
    "BusGroup",
    "CalculationRate",
    "Clock",
    "ClockContext",
    "Context",
    "DoneAction",
    "Group",
    "HeaderFormat",
    "Node",
    "OfflineClock",
    "Options",
    "OscBundle",
    "OscCallback",
    "OscMessage",
    "Pattern",
    "SampleFormat",
    "Score",
    "Server",
    "Synth",
    "SynthDef",
    "SynthDefBuilder",
    "UGen",
    "UGenArray",
    "UGenMethodMixin",
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
