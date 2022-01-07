import configparser
import logging
import pathlib

import platformdirs

try:
    import pyximport

    pyximport.install(language_level=3)
    del pyximport
except ImportError:
    pass

output_path = pathlib.Path(platformdirs.user_cache_dir("supriya", "supriya"))
if not output_path.exists():
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except IOError:
        pass

config = configparser.ConfigParser()
config.read_dict({"core": {"scsynth_path": "scsynth"}})
config_path = pathlib.Path(platformdirs.user_config_dir("supriya", "supriya"))
config_path = config_path / "supriya.cfg"
if not config_path.exists():
    try:
        config_path.parent.mkdir(parents=True, exist_ok=True)
        with config_path.open("w") as file_pointer:
            config.write(file_pointer, True)
    except IOError:
        pass
with config_path.open() as file_pointer:
    config.read_file(file_pointer)

del platformdirs
del configparser
del file_pointer
del pathlib


def _setup_logging(*loggers):
    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    for logger in loggers:
        logging.getLogger(logger).setLevel(logging.DEBUG)


from ._version import __version__, __version_info__  # noqa
from . import utils  # noqa
from .clocks import AsyncClock, AsyncOfflineClock, Clock, OfflineClock  # noqa
from .enums import (  # noqa
    AddAction,
    BinaryOperator,
    CalculationRate,
    DoneAction,
    EnvelopeShape,
    HeaderFormat,
    NodeAction,
    ParameterRate,
    RequestId,
    RequestName,
    SampleFormat,
    SignalRange,
    UnaryOperator,
    Unit,
)
from .io import graph, play, plot, render  # noqa
from .synthdefs import (  # noqa
    Envelope,
    Parameter,
    Range,
    SynthDef,
    SynthDefBuilder,
    SynthDefFactory,
)
from .realtime import (  # noqa
    AsyncServer,
    Buffer,
    BufferGroup,
    Bus,
    BusGroup,
    Group,
    Synth,
    Server,
)
from . import assets  # noqa
from .nonrealtime import Session  # noqa
from .providers import Provider  # noqa
from .scsynth import Options  # noqa
from .soundfiles import Say, SoundFile  # noqa
from .system import Assets  # noqa
