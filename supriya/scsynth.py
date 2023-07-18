import asyncio
import atexit
import enum
import logging
import os
import platform
import signal
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import uqbar.io
import uqbar.objects

from .exceptions import ServerCannotBoot

logger = logging.getLogger(__name__)

DEFAULT_IP_ADDRESS = "127.0.0.1"
DEFAULT_PORT = 57110
ENVAR_SERVER_EXECUTABLE = "SUPRIYA_SERVER_EXECUTABLE"


@dataclass(frozen=True)
class Options:
    """
    SuperCollider server options configuration.
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

    def get_audio_bus_ids(self, client_id: int) -> Tuple[int, int]:
        audio_buses_per_client = (
            self.private_audio_bus_channel_count // self.maximum_logins
        )
        minimum = self.first_private_bus_id + (client_id * audio_buses_per_client)
        maximum = self.first_private_bus_id + ((client_id + 1) * audio_buses_per_client)
        return minimum, maximum

    def get_buffer_ids(self, client_id: int) -> Tuple[int, int]:
        buffers_per_client = self.buffer_count // self.maximum_logins
        minimum = client_id * buffers_per_client
        maximum = (client_id + 1) * buffers_per_client
        return minimum, maximum

    def get_control_bus_ids(self, client_id: int) -> Tuple[int, int]:
        control_buses_per_client = self.control_bus_channel_count // self.maximum_logins
        minimum = client_id * control_buses_per_client
        maximum = (client_id + 1) * control_buses_per_client
        return minimum, maximum

    def get_sync_ids(self, client_id: int) -> Tuple[int, int]:
        return client_id << 26, (client_id + 1) << 26

    def serialize(self) -> List[str]:
        result = [str(find(self.executable))]
        pairs: Dict[str, Optional[str]] = {}
        if self.realtime:
            if self.protocol == "tcp":
                pairs["-t"] = str(self.port)
            else:
                pairs["-u"] = str(self.port)
            if self.input_device:
                pairs["-H"] = str(self.input_device)
                if self.output_device != self.input_device:
                    result.append(str(self.output_device))
            if self.maximum_logins != 64:
                pairs["-l"] = str(self.maximum_logins)
            if self.password:
                pairs["-p"] = str(self.password)
            if self.sample_rate is not None:
                pairs["-S"] = str(self.sample_rate)
            if not self.zero_configuration:
                pairs["-R"] = "0"
        if self.audio_bus_channel_count != 1024:
            pairs["-a"] = str(self.audio_bus_channel_count)
        if self.control_bus_channel_count != 16384:
            pairs["-c"] = str(self.control_bus_channel_count)
        if self.input_bus_channel_count != 8:
            pairs["-i"] = str(self.input_bus_channel_count)
        if self.output_bus_channel_count != 8:
            pairs["-o"] = str(self.output_bus_channel_count)
        if self.buffer_count != 1024:
            pairs["-b"] = str(self.buffer_count)
        if self.maximum_node_count != 1024:
            pairs["-n"] = str(self.maximum_node_count)
        if self.maximum_synthdef_count != 1024:
            pairs["-d"] = str(self.maximum_synthdef_count)
        if self.block_size != 64:
            pairs["-z"] = str(self.block_size)
        if self.hardware_buffer_size is not None:
            pairs["-Z"] = str(self.hardware_buffer_size)
        if self.memory_size != 8192:
            pairs["-m"] = str(self.memory_size)
        if self.random_number_generator_count != 64:
            pairs["-r"] = str(self.random_number_generator_count)
        if self.wire_buffer_count != 64:
            pairs["-w"] = str(self.wire_buffer_count)
        if not self.load_synthdefs:
            pairs["-D"] = "0"
        if self.input_stream_mask:
            pairs["-I"] = str(self.input_stream_mask)
        if self.output_stream_mask:
            pairs["-O"] = str(self.output_stream_mask)
        if 0 < self.verbosity:
            pairs["-v"] = str(self.verbosity)
        if self.restricted_path is not None:
            pairs["-P"] = str(self.restricted_path)
        if self.memory_locking:
            pairs["-L"] = None
        if self.ugen_plugins_path:
            pairs["-U"] = str(self.ugen_plugins_path)
        if self.threads and find(self.executable).stem == "supernova":
            pairs["-t"] = str(self.threads)
        for key, value in sorted(pairs.items()):
            result.extend([key, value] if value is not None else [key])
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
    """
    Find the ``scsynth`` executable.

    The following paths, if defined, will be searched (prioritised as ordered):

    1. The absolute path ``scsynth_path``
    2. The environment variable ``SUPRIYA_SERVER_EXECUTABLE`` (pointing to the `scsynth`
       binary)
    3. The user's ``PATH``
    4. Common installation directories of the SuperCollider application.

    Returns a path to the ``scsynth`` executable. Raises ``RuntimeError`` if no path is
    found.
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


def kill():
    with subprocess.Popen(
        ["ps", "-Af"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT
    ) as process:
        output = process.stdout.read()
    for line in output.decode().splitlines():
        parts = line.split()
        if not any(part in ["supernova", "scsynth"] for part in parts):
            continue
        pid = int(parts[1])
        os.kill(pid, signal.SIGKILL)


class LineStatus(enum.IntEnum):
    CONTINUE = 0
    READY = 1
    ERROR = 2


class ProcessProtocol:
    def __init__(self):
        self.is_running = False

    def boot(self, options: Options):
        raise NotImplementedError

    def quit(self):
        raise NotImplementedError

    def _handle_line(self, line):
        if line.startswith("late:"):
            logger.warning(f"Received: {line}")
        elif "error" in line.lower() or "exception" in line.lower():
            logger.error(f"Received: {line}")
        else:
            logger.info(f"Received: {line}")
        if line.startswith(("SuperCollider 3 server ready", "Supernova ready")):
            return LineStatus.READY
        elif line.startswith(("Exception", "ERROR", "*** ERROR")):
            return LineStatus.ERROR
        return LineStatus.CONTINUE


class SyncProcessProtocol(ProcessProtocol):
    def __init__(self):
        super().__init__()
        atexit.register(self.quit)

    def boot(self, options: Options):
        if self.is_running:
            return
        try:
            logger.info("Boot: {}".format(*options))
            self.process = subprocess.Popen(
                list(options),
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
                start_new_session=True,
            )
            start_time = time.time()
            timeout = 10
            while True:
                line = self.process.stdout.readline().decode().rstrip()  # type: ignore
                if not line:
                    continue
                line_status = self._handle_line(line)
                if line_status == LineStatus.READY:
                    break
                elif line_status == LineStatus.ERROR:
                    raise ServerCannotBoot(line)
                elif (time.time() - start_time) > timeout:
                    raise ServerCannotBoot(line)
            self.is_running = True
        except ServerCannotBoot:
            self.process.terminate()
            self.process.wait()
            raise

    def quit(self) -> None:
        if not self.is_running:
            return
        self.process.terminate()
        self.process.wait()
        self.is_running = False


class AsyncProcessProtocol(asyncio.SubprocessProtocol, ProcessProtocol):
    ### INITIALIZER ###

    def __init__(self):
        ProcessProtocol.__init__(self)
        asyncio.SubprocessProtocol.__init__(self)
        self.boot_future = asyncio.Future()
        self.exit_future = asyncio.Future()
        self.error_text = ""

    ### PUBLIC METHODS ###

    async def boot(self, options: Options):
        logger.info("Booting ...")
        if self.is_running:
            logger.info("... already booted!")
            return
        self.is_running = False
        loop = asyncio.get_running_loop()
        self.boot_future = loop.create_future()
        self.exit_future = loop.create_future()
        self.error_text = ""
        self.buffer_ = ""
        _, _ = await loop.subprocess_exec(
            lambda: self, *options, stdin=None, stderr=None
        )
        if not (await self.boot_future):
            raise ServerCannotBoot(self.error_text)

    def connection_made(self, transport):
        logger.info("Connection made!")
        self.is_running = True
        self.transport = transport

    def pipe_connection_lost(self, fd, exc):
        logger.info("Pipe connection lost!")

    def pipe_data_received(self, fd, data):
        # *nix and OSX return full lines,
        # but Windows will return partial lines
        # which obligates us to reconstruct them.
        text = self.buffer_ + data.decode().replace("\r\n", "\n")
        if "\n" in text:
            text, _, self.buffer_ = text.rpartition("\n")
            for line in text.splitlines():
                line_status = self._handle_line(line)
                if line_status == LineStatus.READY:
                    self.boot_future.set_result(True)
                    logger.info("... booted!")
                elif line_status == LineStatus.ERROR:
                    if not self.boot_future.done():
                        self.boot_future.set_result(False)
                        self.error_text = line
                    logger.info("... failed to boot!")
        else:
            self.buffer_ = text

    def process_exited(self):
        logger.info(f"Process exited with {self.transport.get_returncode()}.")
        self.is_running = False
        try:
            self.exit_future.set_result(None)
            if not self.boot_future.done():
                self.boot_future.set_result(False)
        except asyncio.exceptions.InvalidStateError:
            pass

    async def quit(self):
        logger.info("Quitting ...")
        if not self.is_running:
            logger.info("... already quit!")
            return
        self.is_running = False
        self.transport.close()
        await self.exit_future
        logger.info("... quit!")


class AsyncNonrealtimeProcessProtocol(asyncio.SubprocessProtocol):
    def __init__(self, exit_future: asyncio.Future) -> None:
        self.buffer_ = ""
        self.exit_future = exit_future

    async def run(self, command: List[str], render_directory_path: Path) -> None:
        logger.info(f"Running: {' '.join(command)}")
        _, _ = await asyncio.get_running_loop().subprocess_exec(
            lambda: self,
            *command,
            stdin=None,
            stderr=None,
            start_new_session=True,
            cwd=render_directory_path,
        )

    def handle_line(self, line: str) -> None:
        logger.debug(f"Received: {line}")

    def connection_made(self, transport):
        logger.debug("Connecting")
        self.transport = transport

    def pipe_data_received(self, fd, data):
        logger.debug(f"Data: {data}")
        # *nix and OSX return full lines,
        # but Windows will return partial lines
        # which obligates us to reconstruct them.
        text = self.buffer_ + data.decode().replace("\r\n", "\n")
        if "\n" in text:
            text, _, self.buffer_ = text.rpartition("\n")
            for line in text.splitlines():
                self.handle_line(line)
        else:
            self.buffer_ = text

    def process_exited(self):
        logger.debug(f"Exiting with {self.transport.get_returncode()}")
        self.exit_future.set_result(self.transport.get_returncode())
