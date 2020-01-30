import logging
import os
import signal
import subprocess
import time

import supriya.exceptions

logger = logging.getLogger("supriya.server")


def boot(options, scsynth_path, port):
    options_string = options.as_options_string(port)
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
