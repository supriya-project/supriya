import os
import pathlib
import platform
import signal
import subprocess
from dataclasses import dataclass
from typing import Optional

import uqbar.io
import uqbar.objects

import supriya


@dataclass(frozen=True)
class Options:
    """
    SuperCollider server options configuration.

    ::

        >>> import supriya.realtime
        >>> options = supriya.scsynth.Options()

    """

    ### CLASS VARIABLES ###

    audio_bus_channel_count: int = 1024
    block_size: int = 64
    buffer_count: int = 1024
    control_bus_channel_count: int = 16384
    hardware_buffer_size: Optional[int] = None
    initial_node_id: int = 1000
    input_bus_channel_count: int = 8
    input_device: Optional[str] = None
    input_stream_mask: str = ""
    load_synthdefs: bool = True
    maximum_logins: int = 1
    maximum_node_count: int = 1024
    maximum_synthdef_count: int = 1024
    memory_locking: bool = False
    memory_size: int = 8192
    output_bus_channel_count: int = 8
    output_device: Optional[str] = None
    output_stream_mask: str = ""
    password: Optional[str] = None
    protocol: str = "udp"
    random_number_generator_count: int = 64
    remote_control_volume: bool = False
    restricted_path: Optional[str] = None
    sample_rate: Optional[int] = None
    threads: Optional[int] = None
    ugen_plugins_path: Optional[str] = None
    verbosity: int = 0
    wire_buffer_count: int = 64
    zero_configuration: bool = False

    ### INITIALIZER ###

    def __post_init__(self):
        if self.input_bus_channel_count is None:
            object.__setattr__(self, "input_bus_channel_count", 8)
        if self.output_bus_channel_count is None:
            object.__setattr__(self, "output_bus_channel_count", 8)
        if self.input_bus_channel_count < 0:
            raise ValueError(self.input_bus_channel_count)
        if self.output_bus_channel_count < 0:
            raise ValueError(self.output_bus_channel_count)
        if self.audio_bus_channel_count < (
            self.input_bus_channel_count + self.output_bus_channel_count
        ):
            raise ValueError("Insufficient audio buses")

    ### CLASS VARIABLES ###

    def __repr__(self):
        return uqbar.objects.get_repr(self, multiline=True, suppress_defaults=False)

    ### PUBLIC METHODS ###

    def as_options_string(self, port=57110, realtime=True, supernova=False):
        result = []
        if realtime:
            if self.protocol == "tcp":
                result.append("-t {}".format(port))
            else:
                result.append("-u {}".format(port))
            if self.input_device:
                flag = "-H {}".format(self.input_device)
                if self.output_device != self.input_device:
                    flag = "{} {}".format(flag, self.output_device)
                result.append(flag)
            if self.maximum_logins != 64:
                result.append("-l {}".format(self.maximum_logins))
            if self.password:
                result.append("-p {}".format(self.password))
            if self.sample_rate is not None:
                result.append("-S {}".format(int(self.sample_rate)))
            if not self.zero_configuration:
                result.append("-R 0")
        if self.audio_bus_channel_count != 1024:
            result.append("-a {}".format(self.audio_bus_channel_count))
        if self.control_bus_channel_count != 16384:
            result.append("-c {}".format(self.control_bus_channel_count))
        if self.input_bus_channel_count != 8:
            result.append("-i {}".format(self.input_bus_channel_count))
        if self.output_bus_channel_count != 8:
            result.append("-o {}".format(self.output_bus_channel_count))
        if self.buffer_count != 1024:
            result.append("-b {}".format(self.buffer_count))
        if self.maximum_node_count != 1024:
            result.append("-n {}".format(self.maximum_node_count))
        if self.maximum_synthdef_count != 1024:
            result.append("-d {}".format(self.maximum_synthdef_count))
        if self.block_size != 64:
            result.append("-z {}".format(self.block_size))
        if self.hardware_buffer_size is not None:
            result.append("-Z {}".format(int(self.hardware_buffer_size)))
        if self.memory_size != 8192:
            result.append("-m {}".format(self.memory_size))
        if self.random_number_generator_count != 64:
            result.append("-r {}".format(self.random_number_generator_count))
        if self.wire_buffer_count != 64:
            result.append("-w {}".format(self.wire_buffer_count))
        if not self.load_synthdefs:
            result.append("-D 0")
        if self.input_stream_mask:
            result.append("-I {}".format(self.input_stream_mask))
        if self.output_stream_mask:
            result.append("-O {}".format(self.output_stream_mask))
        if 0 < self.verbosity:
            result.append("-v {}".format(self.verbosity))
        if self.restricted_path is not None:
            result.append("-P {}".format(self.restricted_path))
        if self.memory_locking:
            result.append("-L")
        if self.ugen_plugins_path:
            result.append("-U {}".format(self.ugen_plugins_path))
        if supernova and self.threads:
            result.append("-t {}".format(self.threads))
        options_string = " ".join(sorted(result))
        return options_string

    ### PUBLIC PROPERTIES ###

    @property
    def first_private_bus_id(self):
        return self.output_bus_channel_count + self.input_bus_channel_count

    @property
    def private_audio_bus_channel_count(self):
        return (
            self.audio_bus_channel_count
            - self.input_bus_channel_count
            - self.output_bus_channel_count
        )


def _fallback_scsynth_path():
    if platform.system() == "Darwin":
        for path in [
            pathlib.Path("/Applications/SuperCollider.app/Contents/Resources/scsynth"),
            pathlib.Path(
                "/Applications/SuperCollider/SuperCollider.app/Contents/Resources/scsynth"
            ),
        ]:
            if path.exists():
                return path
    elif platform.system() == "Linux":
        for path in [
            pathlib.Path("/usr/bin/scsynth"),
            pathlib.Path("/usr/local/bin/scsynth"),
        ]:
            if path.exists():
                return path
    return None


def find(scsynth_path=None):
    """Find the ``scsynth`` executable.

    The following paths, if defined, will be searched (prioritised as ordered):
    1. The absolute path ``scsynth_path``
    2. The environment variable ``SCSYNTH_PATH``
    3. ``scsynth_path`` if defined in Supriya's configuration file
    4. The user's ``PATH``
    5. Common installation directories of the SuperCollider application.

    Returns a path to the ``scsynth`` executable.
    Raises ``RuntimeError`` if no path is found.
    """
    scsynth_path = pathlib.Path(
        scsynth_path
        or os.environ.get("SCSYNTH_PATH")
        or supriya.config.get("core", "scsynth_path")
        or "scsynth"
    )
    if scsynth_path.is_absolute() and uqbar.io.find_executable(scsynth_path):
        return scsynth_path
    scsynth_path_candidates = uqbar.io.find_executable(scsynth_path.name)
    if scsynth_path_candidates:
        return pathlib.Path(scsynth_path_candidates[0])
    fallback_path = _fallback_scsynth_path()
    if fallback_path is not None:
        return fallback_path
    raise RuntimeError("Failed to locate scsynth")


def kill(supernova=False):
    executable = "supernova" if supernova else "scsynth"
    with subprocess.Popen(
        ["ps", "-Af"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ) as process:
        output = process.stdout.read()
    for line in output.decode().splitlines():
        parts = line.split()
        if not any(part == executable for part in parts):
            continue
        pid = int(parts[1])
        os.kill(pid, signal.SIGKILL)
