import random
import subprocess
import time
from unittest import mock

import pytest

import supriya.exceptions
import supriya.realtime
from supriya.scsynth import Options


@pytest.mark.timeout(60)
def test_boot():
    server = supriya.realtime.Server(port=57757)
    for i in range(20):
        assert not server.is_running
        server.boot()
        time.sleep(random.random() * 2)
        assert server.is_running
        server.quit()
    assert not server.is_running


def test_boot_options():
    server = supriya.realtime.Server(port=57757)
    try:
        boot_options = Options(memory_size=8192 * 32, load_synthdefs=False)
        # Default
        server.boot()
        assert isinstance(server.options, type(boot_options))
        assert server.options.memory_size == 8192
        assert server.options.load_synthdefs is True
        server.quit()
        # With Options
        server.boot(options=boot_options)
        assert isinstance(server.options, type(boot_options))
        assert server.options.memory_size == 8192 * 32
        assert server.options.load_synthdefs is False
        server.quit()
        # With **kwargs
        server.boot(load_synthdefs=False)
        assert isinstance(server.options, type(boot_options))
        assert server.options.memory_size == 8192
        assert server.options.load_synthdefs is False
        server.quit()
        # With Options and **kwargs
        server.boot(load_synthdefs=False, options=boot_options)
        assert isinstance(server.options, type(boot_options))
        assert server.options.memory_size == 8192 * 32
        assert server.options.load_synthdefs is False
        server.quit()
    finally:
        if server.is_running:
            server.quit()


@pytest.mark.skip("Reimplementing")
def test_server_boot_errors():
    def check_scsynth():
        process = subprocess.Popen("ps -Af", shell=True, stdout=subprocess.PIPE)
        output, _ = process.communicate()
        return output.decode()

    assert "scsynth" not in check_scsynth()

    server = supriya.realtime.Server()
    server.boot()
    assert "scsynth" in check_scsynth()
    assert server.is_running
    assert server.osc_protocol.is_running

    server.quit()
    assert "scsynth" not in check_scsynth()
    assert not server.is_running
    assert not server.osc_protocol.is_running

    with pytest.raises(supriya.exceptions.ServerCannotBoot), mock.patch.object(
        supriya.realtime.Server, "_read_scsynth_boot_output"
    ) as patch:
        patch.side_effect = supriya.exceptions.ServerCannotBoot()
        server.boot()

    assert "scsynth" not in check_scsynth()
    assert not server.is_running
    assert not server.osc_protocol.is_running
