from pathlib import Path

import platformdirs

from ._version import __version__, __version_info__
from .assets.synthdefs import default
from .clocks import (
    AsyncClock,
    AsyncOfflineClock,
    BaseClock,
    Clock,
    ClockContext,
    OfflineClock,
    TimeUnit,
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
    ParameterRate,
    SampleFormat,
    ServerLifecycleEvent,
    ServerShutdownEvent,
)
from .io import graph, play, plot, render
from .osc import OscBundle, OscCallback, OscMessage, find_free_port
from .patterns import Pattern
from .scsynth import Options
from .ugens import (
    Envelope,
    SynthDef,
    SynthDefBuilder,
    UGen,
    UGenOperable,
    UGenVector,
    synthdef,
)

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
    "Envelope",
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
    "ServerLifecycleEvent",
    "ServerShutdownEvent",
    "Synth",
    "SynthDef",
    "SynthDefBuilder",
    "TimeUnit",
    "UGen",
    "UGenOperable",
    "UGenVector",
    "__version__",
    "__version_info__",
    "default",
    "find_free_port",
    "graph",
    "output_path",
    "play",
    "plot",
    "render",
    "synthdef",
]

del Path
del platformdirs
