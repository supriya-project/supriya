import logging
import os
import pathlib
import signal
import subprocess
import time
from dataclasses import dataclass
from typing import Optional

import uqbar.io

import supriya

logger = logging.getLogger("supriya.server")


@dataclass(frozen=True)
class BootOptions:
    """
    SuperCollider server option configuration.

    ::

        >>> import supriya.realtime
        >>> options = supriya.realtime.BootOptions()

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Main Classes"

    audio_bus_channel_count: int = 128
    block_size: int = 64
    buffer_count: int = 1024
    control_bus_channel_count: int = 4096
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
        if os.environ.get("TRAVIS", None):
            object.__setattr__(self, "input_device", "dummy")
            object.__setattr__(self, "output_device", "dummy")
            object.__setattr__(self, "sample_rate", 44100)
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
        if self.audio_bus_channel_count != 128:
            result.append("-a {}".format(self.audio_bus_channel_count))
        if self.control_bus_channel_count != 4096:
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

    def boot(self, scsynth_path, port):
        options_string = self.as_options_string(port)
        command = "{} {}".format(scsynth_path, options_string)
        logger.info("Boot: {}".format(command))
        process = subprocess.Popen(
            command,
            shell=True,
            stderr=subprocess.STDOUT,
            stdout=subprocess.PIPE,
            start_new_session=True,
        )
        try:
            start_time = time.time()
            timeout = 10
            while True:
                line = process.stdout.readline().decode().rstrip()
                if line:
                    logger.info("Boot: {}".format(line))
                if line.startswith("SuperCollider 3 server ready"):
                    break
                elif line.startswith("ERROR:"):
                    raise supriya.exceptions.ServerCannotBoot(line)
                elif line.startswith(
                    "Exception in World_OpenUDP: bind: Address already in use"
                ):
                    raise supriya.exceptions.ServerCannotBoot(line)
                elif (time.time() - start_time) > timeout:
                    raise supriya.exceptions.ServerCannotBoot(line)
        except supriya.exceptions.ServerCannotBoot:
            try:
                process_group = os.getpgid(process.pid)
                os.killpg(process_group, signal.SIGINT)
                process.terminate()
                process.wait()
            except ProcessLookupError:
                pass
            raise
        return process

    @classmethod
    def find_scsynth(cls, scsynth_path=None):
        scsynth_path = pathlib.Path(
            scsynth_path
            or os.environ.get("SCSYNTH_PATH")
            or supriya.config.get("core", "scsynth_path")
            or "scsynth"
        )
        scsynth_path_candidates = uqbar.io.find_executable(scsynth_path.name)
        if not scsynth_path.is_absolute() and scsynth_path_candidates:
            scsynth_path = pathlib.Path(scsynth_path_candidates[0])
        scsynth_path = scsynth_path.resolve().absolute()
        if not scsynth_path.exists():
            raise RuntimeError("{} does not exist".format(scsynth_path))
        if scsynth_path_candidates and scsynth_path == pathlib.Path(
            scsynth_path_candidates[0]
        ):
            scsynth_path = pathlib.Path(scsynth_path.name)
        return scsynth_path

    @classmethod
    def kill(cls, supernova=False):
        executable = "scsynth"
        if supernova:
            executable = "supernova"
        process = subprocess.Popen("ps -Af", shell=True, stdout=subprocess.PIPE)
        output, _ = process.communicate()
        output = output.decode()
        pids = []
        for line in output.splitlines():
            if executable not in line:
                continue
            print(line)
            parts = line.split()
            pids.append(int(parts[1]))
        if pids:
            for pid in pids:
                os.kill(pid, signal.SIGKILL)

    ### PUBLIC PROPERTIES ###

    @property
    def first_private_bus_id(self):
        return self.output_bus_channel_count + self.input_bus_channel_count

    @property
    def private_audio_bus_channel_count(self):
        private_audio_bus_channel_count = self.audio_bus_channel_count
        private_audio_bus_channel_count -= self.input_bus_channel_count
        private_audio_bus_channel_count -= self.output_bus_channel_count
        return private_audio_bus_channel_count
