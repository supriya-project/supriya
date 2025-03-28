import asyncio
import concurrent.futures
import logging

import pytest
from uqbar.strings import normalize

from supriya.enums import BootStatus
from supriya.osc import (
    AsyncOscProtocol,
    HealthCheck,
    OscBundle,
    OscMessage,
    ThreadedOscProtocol,
    find_free_port,
)
from supriya.osc.messages import NTP_DELTA
from supriya.scsynth import AsyncProcessProtocol, Options, ThreadedProcessProtocol

logger = logging.getLogger(__name__)


async def get(x):
    if asyncio.iscoroutine(x):
        return await x
    elif asyncio.isfuture(x):
        return await x
    elif isinstance(x, concurrent.futures.Future):
        return x.result()
    return x


def test_OscMessage() -> None:
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
    assert (
        repr(osc_message)
        == "OscMessage('/foo', 1, 2.5, OscBundle(contents=[OscMessage('/bar', 'baz', 3.0), OscMessage('/ffff', False, True, None)]), ['a', 'b', ['c', 'd']])"
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
    assert (
        repr(new_osc_message)
        == "OscMessage('/foo', 1, 2.5, OscBundle(contents=[OscMessage('/bar', 'baz', 3.0), OscMessage('/ffff', False, True, None)]), ['a', 'b', ['c', 'd']])"
    )


def test_new_ntp_era() -> None:
    """
    Check for NTP timestamp overflow.
    """
    seconds = 2**32 - NTP_DELTA + 1
    datagram = OscBundle._encode_date(seconds=seconds)
    assert datagram.hex() == "0000000100000000"


@pytest.mark.parametrize(
    "osc_protocol_class, process_protocol_class",
    [
        (AsyncOscProtocol, AsyncProcessProtocol),
        (ThreadedOscProtocol, ThreadedProcessProtocol),
    ],
)
@pytest.mark.asyncio
async def test_OscProtocol(osc_protocol_class, process_protocol_class) -> None:
    def on_healthcheck_failed() -> None:
        healthcheck_failed.append(True)

    logger.info("START")
    healthcheck_failed: list[bool] = []
    port = find_free_port()

    logger.info("INIT PROCESS")
    process_protocol = process_protocol_class()

    logger.info("INIT PROTOCOL")
    osc_protocol = osc_protocol_class(on_panic_callback=on_healthcheck_failed)
    assert osc_protocol.status == BootStatus.OFFLINE

    try:
        logger.info("BOOT PROCESS")
        await get(process_protocol.boot(Options(port=port)))
        await get(process_protocol.boot_future)
        assert process_protocol.status == BootStatus.ONLINE

        logger.info("CONNECT PROTOCOL")
        await get(
            osc_protocol.connect(
                "127.0.0.1",
                port,
                healthcheck=HealthCheck(
                    request_pattern=["/status"],
                    response_pattern=["/status.reply"],
                    max_attempts=3,
                ),
            )
        )
        assert osc_protocol.status == BootStatus.BOOTING

        logger.info("AWAIT CONNECTION")
        await get(osc_protocol.boot_future)
        assert osc_protocol.status == BootStatus.ONLINE

        logger.info("QUIT PROCESS")
        await get(process_protocol.quit())

        logger.info("AWAIT DISCONNECTION")
        await get(osc_protocol.exit_future)
        assert osc_protocol.status == BootStatus.OFFLINE

    finally:
        await get(process_protocol.quit())
