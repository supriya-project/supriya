import asyncio
import atexit
import logging
import os
import signal
import subprocess
import time

import supriya.exceptions

logger = logging.getLogger("supriya.server.protocol")


class ProcessProtocol:
    def __init__(self):
        self.is_running = False
        atexit.register(self.quit)

    def boot(self, options, scsynth_path, port):
        ...

    def quit(self):
        ...


class SyncProcessProtocol(ProcessProtocol):

    ### PUBLIC METHODS ###

    def boot(self, options, scsynth_path, port):
        if self.is_running:
            return
        options_string = options.as_options_string(port)
        command = "{} {}".format(scsynth_path, options_string)
        logger.info("Boot: {}".format(command))
        try:
            self.process = subprocess.Popen(
                command,
                shell=True,
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
                start_new_session=True,
            )
            start_time = time.time()
            timeout = 10
            while True:
                line = self.process.stdout.readline().decode().rstrip()
                if line:
                    logger.info("Boot: {}".format(line))
                if line.startswith("SuperCollider 3 server ready"):
                    break
                elif line.startswith("Supernova ready"):
                    break
                elif line.startswith(("ERROR:", "*** ERROR:")):
                    raise supriya.exceptions.ServerCannotBoot(line)
                elif line.startswith(
                    "Exception in World_OpenUDP: bind: Address already in use"
                ):
                    raise supriya.exceptions.ServerCannotBoot(line)
                elif (time.time() - start_time) > timeout:
                    raise supriya.exceptions.ServerCannotBoot(line)
            self.is_running = True
        except supriya.exceptions.ServerCannotBoot:
            try:
                process_group = os.getpgid(self.process.pid)
                os.killpg(process_group, signal.SIGINT)
                self.process.terminate()
                self.process.wait()
            except ProcessLookupError:
                pass
            raise

    def quit(self):
        if not self.is_running:
            return
        # try:
        #    self.process.communicate(timeout=0.1)
        # except subprocess.TimeoutExpired:
        #    self.process.kill()
        #    self.process.communicate()
        try:
            process_group = os.getpgid(self.process.pid)
            os.killpg(process_group, signal.SIGINT)
        except ProcessLookupError:
            logger.warning(f"Could not find process group for PID {self.process.pid}")
        self.process.terminate()
        self.process.wait()
        self.is_running = False


class AsyncProcessProtocol(asyncio.SubprocessProtocol, ProcessProtocol):

    ### INITIALIZER ###

    def __init__(self):
        ProcessProtocol.__init__(self)
        asyncio.SubprocessProtocol.__init__(self)
        self.boot_future = None
        self.exit_future = None

    ### PUBLIC METHODS ###

    async def boot(self, options, scsynth_path, port):
        if self.is_running:
            return
        self.is_running = False
        options_string = options.as_options_string(port)
        command = "{} {}".format(scsynth_path, options_string)
        logger.info(command)
        loop = asyncio.get_running_loop()
        self.boot_future = loop.create_future()
        self.exit_future = loop.create_future()
        _, _ = await loop.subprocess_exec(
            lambda: self, *command.split(), stdin=None, stderr=None
        )

    def connection_made(self, transport):
        self.is_running = True
        self.transport = transport

    def pipe_data_received(self, fd, data):
        for line in data.splitlines():
            logger.info(line.decode())
            if line.strip().startswith(b"Exception"):
                self.boot_future.set_result(False)
            elif line.strip().startswith(b"SuperCollider 3 server ready"):
                self.boot_future.set_result(True)

    def process_exited(self):
        self.is_running = False
        self.exit_future.set_result(None)
        if not self.boot_future.done():
            self.boot_future.set_result(False)

    def quit(self):
        if not self.is_running:
            return
        if not self.boot_future.done():
            self.boot_future.set_result(False)
        if not self.exit_future.done():
            self.exit_future.set_result
        if not self.transport._loop.is_closed() and not self.transport.is_closing():
            self.transport.close()
        self.is_running = False
