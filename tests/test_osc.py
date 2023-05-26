import asyncio
import logging
import time

import pytest
from uqbar.strings import normalize

from supriya.osc import (
    NTP_DELTA,
    AsyncOscProtocol,
    HealthCheck,
    OscBundle,
    OscMessage,
    ThreadedOscProtocol,
    find_free_port,
)
from supriya.scsynth import AsyncProcessProtocol, Options, SyncProcessProtocol


def test_OscMessage():
    osc_message = OscMessage(
        "/foo",
        1,
        2.5,
        OscBundle(
            contents=(
                OscMessage("/bar", "baz", 3.0),
                OscMessage("/ffff", False, True, None),
            )
        ),
        ["a", "b", ["c", "d"]],
    )
    assert repr(osc_message) == normalize(
        """
    OscMessage('/foo', 1, 2.5, OscBundle(
        contents=(
            OscMessage('/bar', 'baz', 3.0),
            OscMessage('/ffff', False, True, None),
        ),
    ), ['a', 'b', ['c', 'd']])
    """
    )
    assert str(osc_message) == normalize(
        """
    size 112
       0   2f 66 6f 6f  00 00 00 00  2c 69 66 62  5b 73 73 5b   |/foo....,ifb[ss[|
      16   73 73 5d 5d  00 00 00 00  00 00 00 01  40 20 00 00   |ss]]........@ ..|
      32   00 00 00 3c  23 62 75 6e  64 6c 65 00  00 00 00 00   |...<#bundle.....|
      48   00 00 00 01  00 00 00 14  2f 62 61 72  00 00 00 00   |......../bar....|
      64   2c 73 66 00  62 61 7a 00  40 40 00 00  00 00 00 10   |,sf.baz.@@......|
      80   2f 66 66 66  66 00 00 00  2c 46 54 4e  00 00 00 00   |/ffff...,FTN....|
      96   61 00 00 00  62 00 00 00  63 00 00 00  64 00 00 00   |a...b...c...d...|
    """
    )
    datagram = osc_message.to_datagram()
    new_osc_message = OscMessage.from_datagram(datagram)
    assert osc_message == new_osc_message
    assert repr(new_osc_message) == normalize(
        """
    OscMessage('/foo', 1, 2.5, OscBundle(
        contents=(
            OscMessage('/bar', 'baz', 3.0),
            OscMessage('/ffff', False, True, None),
        ),
    ), ['a', 'b', ['c', 'd']])
    """
    )


def test_new_ntp_era():
    """
    Check for NTP timestamp overflow.
    """
    seconds = 2**32 - NTP_DELTA + 1
    datagram = OscBundle._encode_date(seconds=seconds)
    assert datagram.hex() == "0000000100000000"


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
        await process_protocol.quit()
        for _ in range(20):
            await asyncio.sleep(1)
            if not osc_protocol.is_running:
                break
        assert healthcheck_failed
        assert not osc_protocol.is_running
    finally:
        await process_protocol.quit()


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
