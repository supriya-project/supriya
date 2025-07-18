import asyncio
import atexit
import concurrent.futures
import enum
import logging
import os
import platform
import re
import shlex
import subprocess
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import (
    IO,
    Callable,
    Iterator,
    Literal,
    cast,
)

import psutil
import uqbar.io
import uqbar.objects

from .enums import BootStatus
from .exceptions import ServerCannotBoot
from .typing import FutureLike

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
    executable: str | None = None
    hardware_buffer_size: int | None = None
    initial_node_id: int = 1000
    input_bus_channel_count: int = 8
    input_device: str | None = None
    input_stream_mask: str = ""
    ip_address: str = DEFAULT_IP_ADDRESS
    load_synthdefs: bool = True
    maximum_logins: int = 1
    maximum_node_count: int = 1024
    maximum_synthdef_count: int = 1024
    memory_locking: bool = False
    memory_size: int = 8192
    output_bus_channel_count: int = 8
    output_device: str | None = None
    output_stream_mask: str = ""
    password: str | None = None
    port: int = DEFAULT_PORT
    protocol: str = "udp"
    random_number_generator_count: int = 64
    realtime: bool = True
    restricted_path: str | None = None
    safety_clip: Literal["inf"] | int | None = None
    sample_rate: int | None = None
    threads: int = 6
    ugen_plugins_path: str | None = None
    verbosity: int = 0
    wire_buffer_count: int = 64
    zero_configuration: bool = False

    ### INITIALIZER ###

    def __post_init__(self):
        if self.audio_bus_channel_count < (
            self.input_bus_channel_count + self.output_bus_channel_count
        ):
            raise ValueError("Insufficient audio buses")

    ### CLASS VARIABLES ###

    def __iter__(self):
        return (arg for arg in self.serialize())

    ### PUBLIC METHODS ###

    def get_audio_bus_ids(self, client_id: int) -> tuple[int, int]:
        audio_buses_per_client = (
            self.private_audio_bus_channel_count // self.maximum_logins
        )
        minimum = self.first_private_bus_id + (client_id * audio_buses_per_client)
        maximum = self.first_private_bus_id + ((client_id + 1) * audio_buses_per_client)
        return minimum, maximum

    def get_buffer_ids(self, client_id: int) -> tuple[int, int]:
        buffers_per_client = self.buffer_count // self.maximum_logins
        minimum = client_id * buffers_per_client
        maximum = (client_id + 1) * buffers_per_client
        return minimum, maximum

    def get_control_bus_ids(self, client_id: int) -> tuple[int, int]:
        control_buses_per_client = self.control_bus_channel_count // self.maximum_logins
        minimum = client_id * control_buses_per_client
        maximum = (client_id + 1) * control_buses_per_client
        return minimum, maximum

    def get_sync_ids(self, client_id: int) -> tuple[int, int]:
        return client_id << 26, (client_id + 1) << 26

    def serialize(self) -> list[str]:
        result = [str(find(self.executable))]
        pairs: dict[str, list[str] | str | None] = {}
        if self.realtime:
            if self.ip_address != DEFAULT_IP_ADDRESS:
                pairs["-B"] = self.ip_address
            if self.protocol == "tcp":
                pairs["-t"] = str(self.port)
            else:
                pairs["-u"] = str(self.port)
            if self.input_device == self.output_device:
                if self.input_device:
                    pairs["-H"] = str(self.input_device)
            else:
                pairs["-H"] = [
                    str(self.input_device or ""),
                    str(self.output_device or ""),
                ]
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
        if self.block_size != 64:
            pairs["-z"] = str(self.block_size)
        if self.buffer_count != 1024:
            pairs["-b"] = str(self.buffer_count)
        if self.control_bus_channel_count != 16384:
            pairs["-c"] = str(self.control_bus_channel_count)
        if self.hardware_buffer_size is not None:
            pairs["-Z"] = str(self.hardware_buffer_size)
        if self.input_bus_channel_count != 8:
            pairs["-i"] = str(self.input_bus_channel_count)
        if self.input_stream_mask:
            pairs["-I"] = str(self.input_stream_mask)
        if not self.load_synthdefs:
            pairs["-D"] = "0"
        if self.maximum_node_count != 1024:
            pairs["-n"] = str(self.maximum_node_count)
        if self.maximum_synthdef_count != 1024:
            pairs["-d"] = str(self.maximum_synthdef_count)
        if self.memory_locking:
            pairs["-L"] = None
        if self.memory_size != 8192:
            pairs["-m"] = str(self.memory_size)
        if self.output_bus_channel_count != 8:
            pairs["-o"] = str(self.output_bus_channel_count)
        if self.output_stream_mask:
            pairs["-O"] = str(self.output_stream_mask)
        if self.random_number_generator_count != 64:
            pairs["-r"] = str(self.random_number_generator_count)
        if self.restricted_path is not None:
            pairs["-P"] = str(self.restricted_path)
        if self.safety_clip is not None:
            pairs["-s"] = str(self.safety_clip)
        if self.threads != 6 and find(self.executable).stem == "supernova":
            pairs["-T"] = str(self.threads)
        if self.ugen_plugins_path:
            pairs["-U"] = str(self.ugen_plugins_path)
        if 0 < self.verbosity:
            pairs["-v"] = str(self.verbosity)
        if self.wire_buffer_count != 64:
            pairs["-w"] = str(self.wire_buffer_count)
        for key, value in sorted(pairs.items()):
            result.append(key)
            if isinstance(value, str):
                result.append(value)
            elif isinstance(value, list):
                result.extend(value)
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
        paths.extend(
            [
                Path(
                    "/Applications/SuperCollider.app/Contents/Resources/" + executable
                ),
                Path(
                    "/Applications/SuperCollider/SuperCollider.app/Contents/Resources/"
                    + executable
                ),
            ]
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
    for process in psutil.process_iter():
        if process.name() in ("scsynth", "supernova", "scsynth.exe", "supernova.exe"):
            logger.info(f"killing {process!r}")
            process.kill()


class LineStatus(enum.IntEnum):
    CONTINUE = 0
    READY = 1
    ERROR = 2


class Capture:
    def __init__(
        self,
        *,
        future: FutureLike[bool] | None = None,
        process_protocol: "ProcessProtocol",
        start_pattern: str | None = None,
        stop_pattern: str | None = None,
    ) -> None:
        self.future = future
        self.lines: list[str] = []
        self.process_protocol = process_protocol
        self.start_pattern = re.compile(start_pattern) if start_pattern else None
        self.stop_pattern = re.compile(stop_pattern) if stop_pattern else None

    def __enter__(self) -> "Capture":
        self.capturing = self.start_pattern is None
        self.process_protocol.captures.add(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.process_protocol.captures.remove(self)
        self.capturing = False
        if self.future and not self.future.done():
            self.future.set_result(False)

    def __iter__(self) -> Iterator[str]:
        return iter(self.lines)

    def __len__(self) -> int:
        return len(self.lines)

    def capture(self, line: str) -> None:
        should_capture = False
        if self.capturing:
            if self.stop_pattern and self.stop_pattern.match(line):
                self.capturing = False
                if self.future:
                    self.future.set_result(True)
            should_capture = True
        elif (
            self.start_pattern
            and self.start_pattern.match(line)
            and (not self.future or not self.future.done())
        ):
            self.capturing = True
            should_capture = True
        if should_capture:
            self.lines.append(line)


class ProcessProtocol:
    def __init__(
        self,
        *,
        name: str | None = None,
        on_boot_callback: Callable | None = None,
        on_panic_callback: Callable | None = None,
        on_quit_callback: Callable | None = None,
    ) -> None:
        self.buffer_ = ""
        self.captures: set[Capture] = set()
        self.error_text = ""
        self.name = name
        self.on_boot_callback = on_boot_callback
        self.on_panic_callback = on_panic_callback
        self.on_quit_callback = on_quit_callback
        self.status = BootStatus.OFFLINE
        self.options = Options()

    def _boot(self, options: Options) -> bool:
        self.options = options
        logger.info(
            f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
            "booting ..."
        )
        if self.status != BootStatus.OFFLINE:
            logger.info(
                f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
                "... already booted!"
            )
            return False
        self.status = BootStatus.BOOTING
        self.error_text = ""
        self.buffer_ = ""
        logger.info(
            f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
            "command: {}".format(shlex.join(options))
        )
        return True

    def _handle_data_received(
        self,
        *,
        boot_future: FutureLike[bool],
        text: str,
    ) -> tuple[bool, bool]:
        resolved = False
        errored = False
        if "\n" in text:
            text, _, self.buffer_ = text.rpartition("\n")
            for line in text.splitlines():
                for capture in self.captures:
                    capture.capture(line)
                line_status = self._parse_line(line)
                if line_status == LineStatus.READY:
                    boot_future.set_result(True)
                    self.status = BootStatus.ONLINE
                    resolved = True
                    logger.info(
                        f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
                        "... booted!"
                    )
                elif line_status == LineStatus.ERROR:
                    if not boot_future.done():
                        boot_future.set_result(False)
                        self.status = BootStatus.OFFLINE
                        self.error_text = line
                        resolved = True
                        errored = True
                    logger.info("... failed to boot!")
        else:
            self.buffer_ = text
        return resolved, errored

    def _parse_line(self, line: str) -> LineStatus:
        logger.info(
            f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
            f"received: {line}"
        )
        if line.startswith(("SuperCollider 3 server ready", "Supernova ready")):
            return LineStatus.READY
        elif line.startswith(("Exception", "ERROR", "*** ERROR")):
            return LineStatus.ERROR
        return LineStatus.CONTINUE

    def _quit(self) -> bool:
        logger.info(
            f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
            "quitting ..."
        )
        if self.status != BootStatus.ONLINE:
            logger.info(
                f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
                "... already quit!"
            )
            return False
        self.status = BootStatus.QUITTING
        return True

    def capture(
        self,
        *,
        future: FutureLike[bool] | None = None,
        start_pattern: str | None = None,
        stop_pattern: str | None = None,
    ) -> Capture:
        return Capture(
            future=future,
            process_protocol=self,
            start_pattern=start_pattern,
            stop_pattern=stop_pattern,
        )


class ThreadedProcessProtocol(ProcessProtocol):
    def __init__(
        self,
        *,
        name: str | None = None,
        on_boot_callback: Callable | None = None,
        on_panic_callback: Callable | None = None,
        on_quit_callback: Callable | None = None,
    ) -> None:
        super().__init__(
            name=name,
            on_boot_callback=on_boot_callback,
            on_panic_callback=on_panic_callback,
            on_quit_callback=on_quit_callback,
        )
        atexit.register(self.quit)
        self.boot_future: concurrent.futures.Future[bool] = concurrent.futures.Future()
        self.exit_future: concurrent.futures.Future[int] = concurrent.futures.Future()

    def _run_process_thread(self, options: Options) -> None:
        with subprocess.Popen(
            list(options),
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            start_new_session=True,
        ) as process:
            self.process = process
            read_thread = threading.Thread(
                args=(),
                daemon=True,
                target=self._run_read_thread,
            )
            read_thread.start()
            self.process.wait()
            was_quitting = self.status == BootStatus.QUITTING
            self.status = BootStatus.OFFLINE
            self.exit_future.set_result(self.process.returncode)
            if not self.boot_future.done():
                self.boot_future.set_result(False)
            if was_quitting and self.on_quit_callback:
                self.on_quit_callback()
            elif not was_quitting and self.on_panic_callback:
                self.on_panic_callback()

    def _run_read_thread(self) -> None:
        while self.status in (BootStatus.BOOTING, BootStatus.ONLINE):
            if not (text := cast(IO[bytes], self.process.stdout).readline().decode()):
                continue
            _, _ = self._handle_data_received(boot_future=self.boot_future, text=text)

    def _shutdown(self) -> None:
        self.process.terminate()
        self.thread.join()
        self.status = BootStatus.OFFLINE

    def boot(self, options: Options) -> None:
        if not self._boot(options):
            return
        self.boot_future = concurrent.futures.Future()
        self.exit_future = concurrent.futures.Future()
        self.thread = threading.Thread(
            args=(options,),
            daemon=True,
            target=self._run_process_thread,
        )
        self.thread.start()
        if not (self.boot_future.result()):
            self._shutdown()
            raise ServerCannotBoot(self.error_text)
        if self.on_boot_callback:
            self.on_boot_callback()

    def quit(self) -> None:
        if not self._quit():
            return
        self._shutdown()
        self.exit_future.result()
        logger.info(
            f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
            "... quit!"
        )


class AsyncProcessProtocol(asyncio.SubprocessProtocol, ProcessProtocol):
    ### INITIALIZER ###

    def __init__(
        self,
        *,
        name: str | None = None,
        on_boot_callback: Callable | None = None,
        on_panic_callback: Callable | None = None,
        on_quit_callback: Callable | None = None,
    ) -> None:
        ProcessProtocol.__init__(
            self,
            name=name,
            on_boot_callback=on_boot_callback,
            on_panic_callback=on_panic_callback,
            on_quit_callback=on_quit_callback,
        )
        asyncio.SubprocessProtocol.__init__(self)
        self.boot_future: asyncio.Future[bool] = asyncio.Future()
        self.exit_future: asyncio.Future[bool] = asyncio.Future()

    ### PUBLIC METHODS ###

    async def boot(self, options: Options) -> None:
        if not self._boot(options):
            return
        loop = asyncio.get_running_loop()
        self.boot_future = loop.create_future()
        self.exit_future = loop.create_future()
        await loop.subprocess_exec(lambda: self, *options, stdin=None, stderr=None)
        if not (await self.boot_future):
            await self.exit_future
            raise ServerCannotBoot(self.error_text)
        if self.on_boot_callback:
            self.on_boot_callback()

    def connection_made(self, transport) -> None:
        def kill() -> None:
            if transport.is_closing():
                return
            try:
                transport.kill()
            except ProcessLookupError:
                pass

        logger.info(
            f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
            "connection made!"
        )
        self.transport = transport
        atexit.register(kill)

    def pipe_connection_lost(self, fd, exc) -> None:
        logger.info(
            f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
            "pipe connection lost!"
        )

    def pipe_data_received(self, fd, data) -> None:
        # *nix and OSX return full lines,
        # but Windows will return partial lines
        # which obligates us to reconstruct them.
        text = self.buffer_ + data.decode().replace("\r\n", "\n")
        _, _ = self._handle_data_received(boot_future=self.boot_future, text=text)

    def process_exited(self) -> None:
        return_code = self.transport.get_returncode()
        logger.info(
            f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
            f"process exited with {return_code}."
        )
        was_quitting = self.status == BootStatus.QUITTING
        try:
            self.exit_future.set_result(return_code)
            self.status = BootStatus.OFFLINE
            if not self.boot_future.done():
                self.boot_future.set_result(False)
        except asyncio.exceptions.InvalidStateError:
            pass
        if was_quitting and self.on_quit_callback:
            self.on_quit_callback()
        elif not was_quitting and self.on_panic_callback:
            self.on_panic_callback()

    async def quit(self) -> None:
        if not self._quit():
            return
        self.transport.close()
        await self.exit_future
        logger.info(
            f"[{self.options.ip_address}:{self.options.port}/{self.name or hex(id(self))}] "
            "... quit!"
        )


class AsyncNonrealtimeProcessProtocol(asyncio.SubprocessProtocol, ProcessProtocol):
    def __init__(self) -> None:
        ProcessProtocol.__init__(self)
        asyncio.SubprocessProtocol.__init__(self)
        self.boot_future: asyncio.Future[bool] = asyncio.Future()
        self.exit_future: asyncio.Future[bool] = asyncio.Future()

    async def run(self, command: list[str], render_directory_path: Path) -> None:
        logger.info(f"running: {shlex.join(command)}")
        loop = asyncio.get_running_loop()
        self.boot_future = loop.create_future()
        self.exit_future = loop.create_future()
        _, _ = await loop.subprocess_exec(
            lambda: self,
            *command,
            stdin=None,
            stderr=None,
            start_new_session=True,
            cwd=render_directory_path,
        )
        await self.exit_future

    def connection_made(self, transport) -> None:
        logger.info("connection made!")
        self.transport = transport

    def pipe_connection_lost(self, fd, exc) -> None:
        logger.info("pipe connection lost!")

    def pipe_data_received(self, fd, data) -> None:
        # *nix and OSX return full lines,
        # but Windows will return partial lines
        # which obligates us to reconstruct them.
        text = self.buffer_ + data.decode().replace("\r\n", "\n")
        _, _ = self._handle_data_received(boot_future=self.boot_future, text=text)

    def process_exited(self) -> None:
        return_code = self.transport.get_returncode()
        logger.info(f"process exited with {return_code}.")
        self.exit_future.set_result(return_code)
        try:
            if not self.boot_future.done():
                self.boot_future.set_result(False)
        except asyncio.exceptions.InvalidStateError:
            pass
