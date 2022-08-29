import asyncio
import atexit
import enum
import logging
import subprocess
import time

import supriya.exceptions

logger = logging.getLogger("supriya.server.protocol")


class LineStatus(enum.IntEnum):
    CONTINUE = 0
    READY = 1
    ERROR = 2


class ProcessProtocol:
    def __init__(self):
        self.is_running = False
        atexit.register(self.quit)

    def boot(self, options, scsynth_path, port):
        ...

    def quit(self):
        ...

    def _build_command(sef, options, scsynth_path, port):
        options_string = options.as_options_string(port)
        command = [str(scsynth_path), *options_string.split()]
        logger.info("Boot: {}".format(command))
        return command

    def _handle_line(self, line):
        logger.info(f"Received: {line}")
        if line.startswith(("SuperCollider 3 server ready", "Supernova ready")):
            return LineStatus.READY
        elif line.startswith(("Exception", "ERROR", "*** ERROR")):
            return LineStatus.ERROR
        return LineStatus.CONTINUE


class SyncProcessProtocol(ProcessProtocol):

    ### PUBLIC METHODS ###

    def boot(self, options, scsynth_path, port):
        if self.is_running:
            return
        try:
            self.process = subprocess.Popen(
                self._build_command(options, scsynth_path, port),
                stderr=subprocess.STDOUT,
                stdout=subprocess.PIPE,
                start_new_session=True,
            )
            start_time = time.time()
            timeout = 10
            while True:
                line = self.process.stdout.readline().decode().rstrip()
                if not line:
                    continue
                line_status = self._handle_line(line)
                if line_status == LineStatus.READY:
                    break
                elif line_status == LineStatus.ERROR:
                    raise supriya.exceptions.ServerCannotBoot(line)
                elif (time.time() - start_time) > timeout:
                    raise supriya.exceptions.ServerCannotBoot(line)
            self.is_running = True
        except supriya.exceptions.ServerCannotBoot:
            self.process.terminate()
            self.process.wait()
            raise

    def quit(self):
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
        self.boot_future = None
        self.exit_future = None

    ### PUBLIC METHODS ###

    async def boot(self, options, scsynth_path, port):
        logger.info("Booting ...")
        if self.is_running:
            logger.info("... already booted!")
            return
        self.is_running = False
        loop = asyncio.get_running_loop()
        self.boot_future = loop.create_future()
        self.exit_future = loop.create_future()
        self.buffer_ = ""
        _, _ = await loop.subprocess_exec(
            lambda: self,
            *self._build_command(options, scsynth_path, port),
            stdin=None,
            stderr=None,
            start_new_session=True,
        )

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
                    self.boot_future.set_result(False)
                    logger.info("... failed to boot!")
        else:
            self.buffer_ = text

    def process_exited(self):
        self.is_running = False
        self.exit_future.set_result(None)
        if not self.boot_future.done():
            self.boot_future.set_result(False)
        logger.info(f"Process exited with {self.transport.get_returncode()}.")

    def quit(self):
        logger.info("Quitting ...")
        if not self.is_running:
            logger.info("... already quit!")
            return
        if not self.boot_future.done():
            self.boot_future.set_result(False)
        if not self.exit_future.done():
            self.exit_future.set_result
        self.transport.close()
        self.is_running = False
        logger.info("... quit!")
