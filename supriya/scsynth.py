import os
import platform
import signal
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

import uqbar.io
import uqbar.objects

DEFAULT_IP_ADDRESS = "127.0.0.1"
DEFAULT_PORT = 57110
ENVAR_SERVER_EXECUTABLE = "SUPRIYA_SERVER_EXECUTABLE"


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
    executable: Optional[str] = None
    hardware_buffer_size: Optional[int] = None
    initial_node_id: int = 1000
    input_bus_channel_count: int = 8
    input_device: Optional[str] = None
    input_stream_mask: str = ""
    ip_address: str = DEFAULT_IP_ADDRESS
    load_synthdefs: bool = False
    maximum_logins: int = 1
    maximum_node_count: int = 1024
    maximum_synthdef_count: int = 1024
    memory_locking: bool = False
    memory_size: int = 8192
    output_bus_channel_count: int = 8
    output_device: Optional[str] = None
    output_stream_mask: str = ""
    password: Optional[str] = None
    port: int = DEFAULT_PORT
    protocol: str = "udp"
    random_number_generator_count: int = 64
    remote_control_volume: bool = False
    realtime: bool = True
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

    def __iter__(self):
        return (arg for arg in self.serialize())

    ### PUBLIC METHODS ###

    def serialize(self) -> List[str]:
        result = [str(find(self.executable))]
        if self.realtime:
            if self.protocol == "tcp":
                result.extend(["-t", str(self.port)])
            else:
                result.extend(["-u", str(self.port)])
            if self.input_device:
                result.extend(["-H", str(self.input_device)])
                if self.output_device != self.input_device:
                    result.append(str(self.output_device))
            if self.maximum_logins != 64:
                result.extend(["-l", str(self.maximum_logins)])
            if self.password:
                result.extend(["-p", str(self.password)])
            if self.sample_rate is not None:
                result.extend(["-S", str(self.sample_rate)])
            if not self.zero_configuration:
                result.extend(["-R", "0"])
        if self.audio_bus_channel_count != 1024:
            result.extend(["-a", str(self.audio_bus_channel_count)])
        if self.control_bus_channel_count != 16384:
            result.extend(["-c", str(self.control_bus_channel_count)])
        if self.input_bus_channel_count != 8:
            result.extend(["-i", str(self.input_bus_channel_count)])
        if self.output_bus_channel_count != 8:
            result.extend(["-o", str(self.output_bus_channel_count)])
        if self.buffer_count != 1024:
            result.extend(["-b", str(self.buffer_count)])
        if self.maximum_node_count != 1024:
            result.extend(["-n", str(self.maximum_node_count)])
        if self.maximum_synthdef_count != 1024:
            result.extend(["-d", str(self.maximum_synthdef_count)])
        if self.block_size != 64:
            result.extend(["-z", str(self.block_size)])
        if self.hardware_buffer_size is not None:
            result.extend(["-Z", str(self.hardware_buffer_size)])
        if self.memory_size != 8192:
            result.extend(["-m", str(self.memory_size)])
        if self.random_number_generator_count != 64:
            result.extend(["-r", str(self.random_number_generator_count)])
        if self.wire_buffer_count != 64:
            result.extend(["-w", str(self.wire_buffer_count)])
        if not self.load_synthdefs:
            result.extend(["-D", "0"])
        if self.input_stream_mask:
            result.extend(["-I", str(self.input_stream_mask)])
        if self.output_stream_mask:
            result.extend(["-O", str(self.output_stream_mask)])
        if 0 < self.verbosity:
            result.extend(["-v", str(self.verbosity)])
        if self.restricted_path is not None:
            result.extend(["-P", str(self.restricted_path)])
        if self.memory_locking:
            result.append("-L")
        if self.ugen_plugins_path:
            result.extend(["-U", str(self.ugen_plugins_path)])
        if self.threads and find(self.executable).stem == "supernova":
            result.extend(["-t", str(self.threads)])
        return result

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


def find(scsynth_path=None):
    """Find the ``scsynth`` executable.

    The following paths, if defined, will be searched (prioritised as ordered):

    1. The absolute path ``scsynth_path``
    2. The environment variable ``SUPRIYA_SERVER_EXECUTABLE`` (pointing to the `scsynth` binary)
    3. The user's ``PATH``
    4. Common installation directories of the SuperCollider application.

    Returns a path to the ``scsynth`` executable.
    Raises ``RuntimeError`` if no path is found.
    """
    path = Path(scsynth_path or os.environ.get(ENVAR_SERVER_EXECUTABLE) or "scsynth")
    if path.is_absolute() and uqbar.io.find_executable(str(path)):
        return path
    path_candidates = uqbar.io.find_executable(path.name)
    if path_candidates:
        return Path(path_candidates[0])
    paths = []
    executable = scsynth_path or "scsynth"
    if Path(executable).stem == "supernova":
        executable = "supernova"
    system = platform.system()
    if system == "Linux":
        paths.extend(
            [Path("/usr/bin/" + executable), Path("/usr/local/bin/" + executable)]
        )
    elif system == "Darwin":
        paths.append(
            Path("/Applications/SuperCollider.app/Contents/Resources/" + executable)
        )
    elif system == "Windows":
        paths.extend(
            Path(r"C:\Program Files").glob(r"SuperCollider*\\" + executable + ".exe")
        )
    for path in paths:
        if path.exists():
            return path
    raise RuntimeError("Failed to locate executable")


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
