import asyncio
import logging
import time

import pytest

from supriya.osc import (
    AsyncOscProtocol,
    HealthCheck,
    ThreadedOscProtocol,
    find_free_port,
)
from supriya.scsynth import AsyncProcessProtocol, Options, SyncProcessProtocol


@pytest.fixture(autouse=True)
def log_everything(caplog):
    caplog.set_level(logging.DEBUG, logger="supriya.osc")
    caplog.set_level(logging.DEBUG, logger="supriya.server")


@pytest.mark.asyncio
async def test_AsyncOscProtocol():
    def on_healthcheck_failed():
        healthcheck_failed.append(True)

    try:
        healthcheck_failed = []
        port = find_free_port()
        options = Options(port=port)
        healthcheck = HealthCheck(
            request_pattern=["/status"],
            response_pattern=["/status.reply"],
            callback=on_healthcheck_failed,
            max_attempts=3,
        )
        process_protocol = AsyncProcessProtocol()
        await process_protocol.boot(options)
        assert await process_protocol.boot_future
        osc_protocol = AsyncOscProtocol()
        await osc_protocol.connect("127.0.0.1", port, healthcheck=healthcheck)
        assert osc_protocol.is_running
        assert not healthcheck_failed
        await asyncio.sleep(1)
        process_protocol.quit()
        for _ in range(20):
            await asyncio.sleep(1)
            if not osc_protocol.is_running:
                break
        assert healthcheck_failed
        assert not osc_protocol.is_running
    finally:
        process_protocol.quit()


def test_ThreadedOscProtocol():
    def on_healthcheck_failed():
        healthcheck_failed.append(True)

    healthcheck_failed = []
    options = Options()
    port = find_free_port()
    healthcheck = HealthCheck(
        request_pattern=["/status"],
        response_pattern=["/status.reply"],
        callback=on_healthcheck_failed,
        max_attempts=3,
    )
    process_protocol = SyncProcessProtocol()
    process_protocol.boot(options)
    assert process_protocol.is_running
    osc_protocol = ThreadedOscProtocol()
    osc_protocol.connect("127.0.0.1", port, healthcheck=healthcheck)
    assert osc_protocol.is_running
    assert not healthcheck_failed
    time.sleep(1)
    process_protocol.quit()
    assert not process_protocol.is_running
    assert osc_protocol.is_running
    assert not healthcheck_failed
    for _ in range(20):
        time.sleep(1)
        if not osc_protocol.is_running:
            break
    assert healthcheck_failed
    assert not osc_protocol.is_running
