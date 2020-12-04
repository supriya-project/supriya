import configparser
import logging
import pathlib

import appdirs

try:
    import pyximport

    pyximport.install(language_level=3)
    del pyximport
except ImportError:
    pass

output_path = pathlib.Path(appdirs.user_cache_dir("supriya", "supriya"))
if not output_path.exists():
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except IOError:
        pass

config = configparser.ConfigParser()
config.read_dict({"core": {"editor": "vim", "scsynth_path": "scsynth"}})
config_path = pathlib.Path(appdirs.user_config_dir("supriya", "supriya"))
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

del appdirs
del configparser
del pathlib


def setup_logging(*loggers):
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    for logger in loggers:
        logging.getLogger(logger).setLevel(logging.DEBUG)


from supriya._version import __version__, __version_info__  # noqa
from supriya import utils  # noqa
from supriya.clock import TempoClock  # noqa
from supriya.enums import (  # noqa
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
from supriya.io import graph, play, render  # noqa
from supriya.synthdefs import (  # noqa
    Envelope,
    Parameter,
    Range,
    SynthDef,
    SynthDefBuilder,
    SynthDefFactory,
)
from supriya.realtime import (  # noqa
    Buffer,
    BufferGroup,
    Bus,
    BusGroup,
    Group,
    Synth,
    Server,
)
from supriya import assets  # noqa
from supriya.nonrealtime import Session  # noqa
from supriya.provider import Provider  # noqa
from supriya.scsynth import Options  # noqa
from supriya.soundfiles import Say, SoundFile  # noqa
from supriya.system import Assets  # noqa

server = Server.default()
