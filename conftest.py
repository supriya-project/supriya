import os
import signal
import subprocess

import abjad
import pytest

import supriya


@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["abjad"] = abjad
    doctest_namespace["supriya"] = supriya


@pytest.helpers.register
def kill_scsynth():
    process = subprocess.Popen("ps -Af", shell=True, stdout=subprocess.PIPE)
    output, _ = process.communicate()
    output = output.decode()
    pids = []
    for line in output:
        if "scsynth" not in line:
            continue
        parts = line.split()
        pids.append(int(parts[1]))
    if pids:
        for pid in pids:
            os.kill(pid, signal.SIGKILL)
        raise RuntimeError("scsynth was still running: {}".format(pids))


@pytest.fixture(autouse=True)
def server_shutdown():
    kill_scsynth()
    for server in supriya.Server._servers.values():
        server.quit()
    yield
    for server in supriya.Server._servers.values():
        server.quit()
    kill_scsynth()
