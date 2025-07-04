import asyncio
import logging
import re
import subprocess
import sys
from typing import AsyncGenerator

import pytest
import pytest_asyncio
from uqbar.strings import normalize

from supriya import (
    AsyncServer,
    Group,
    OscBundle,
    OscCallback,
    OscMessage,
    ScopeBuffer,
    Server,
    ServerLifecycleCallback,
    ServerLifecycleEvent,
    default,
    scsynth,
)
from supriya.contexts.responses import StatusInfo, VersionInfo
from supriya.exceptions import ServerOffline
from supriya.ugens import SYSTEM_SYNTHDEFS


async def get(x):
    if asyncio.iscoroutine(x):
        return await x
    return x


@pytest.fixture(autouse=True)
def use_caplog(caplog) -> None:
    caplog.set_level(logging.INFO)


@pytest_asyncio.fixture(autouse=True, params=[AsyncServer, Server])
async def context(request) -> AsyncGenerator[AsyncServer | Server, None]:
    context = request.param()
    await get(context.boot())
    context.add_synthdefs(default)
    await get(context.sync())
    yield context


@pytest.mark.asyncio
async def test_ScopeBuffer(context: AsyncServer | Server) -> None:
    with context.osc_protocol.capture() as transcript:
        scope_buffer = context.add_scope_buffer()
    assert transcript.filtered(received=False, status=False) == []
    assert isinstance(scope_buffer, ScopeBuffer)
    assert scope_buffer.context is context
    assert scope_buffer.id_ == 0
    with context.osc_protocol.capture() as transcript:
        scope_buffer.free()
    assert transcript.filtered(received=False, status=False) == []


@pytest.mark.asyncio
async def test_clear_schedule(context: AsyncServer | Server) -> None:
    with context.osc_protocol.capture() as transcript:
        context.clear_schedule()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/clearSched")
    ]


@pytest.mark.asyncio
async def test_default_group(context: AsyncServer | Server) -> None:
    assert isinstance(context.default_group, Group)
    assert context.default_group.context is context
    assert context.default_group.id_ == context.client_id + 1


# Under 3.10/11 we often see the server not receive the sync response,
# so this will time-out.
@pytest.mark.flaky(reruns=5, conditions=sys.version_info[:2] in [(3, 10), (3, 11)])
@pytest.mark.asyncio
async def test_dump_tree(context: AsyncServer | Server) -> None:
    with context.osc_protocol.capture() as transcript:
        tree = await get(context.dump_tree())
        assert str(tree) == normalize(
            """
            NODE TREE 0 group
                1 group
            """
        )
        assert transcript.filtered(received=False, status=False) == [
            OscMessage("/g_dumpTree", 0, 1),
            OscMessage("/sync", 2),
        ]
    for i in range(500):
        context.add_synth(default, amplitude=0.5, frequency=(i * 11) + 20)
    with context.osc_protocol.capture() as transcript:
        tree = await get(context.dump_tree())
    assert str(tree) == normalize(
        """
        NODE TREE 0 group
            1 group
                1499 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5509.0, gate: 1.0, pan: 0.5
                1498 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5498.0, gate: 1.0, pan: 0.5
                1497 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5487.0, gate: 1.0, pan: 0.5
                1496 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5476.0, gate: 1.0, pan: 0.5
                1495 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5465.0, gate: 1.0, pan: 0.5
                1494 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5454.0, gate: 1.0, pan: 0.5
                1493 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5443.0, gate: 1.0, pan: 0.5
                1492 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5432.0, gate: 1.0, pan: 0.5
                1491 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5421.0, gate: 1.0, pan: 0.5
                1490 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5410.0, gate: 1.0, pan: 0.5
                1489 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5399.0, gate: 1.0, pan: 0.5
                1488 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5388.0, gate: 1.0, pan: 0.5
                1487 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5377.0, gate: 1.0, pan: 0.5
                1486 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5366.0, gate: 1.0, pan: 0.5
                1485 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5355.0, gate: 1.0, pan: 0.5
                1484 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5344.0, gate: 1.0, pan: 0.5
                1483 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5333.0, gate: 1.0, pan: 0.5
                1482 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5322.0, gate: 1.0, pan: 0.5
                1481 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5311.0, gate: 1.0, pan: 0.5
                1480 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5300.0, gate: 1.0, pan: 0.5
                1479 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5289.0, gate: 1.0, pan: 0.5
                1478 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5278.0, gate: 1.0, pan: 0.5
                1477 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5267.0, gate: 1.0, pan: 0.5
                1476 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5256.0, gate: 1.0, pan: 0.5
                1475 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5245.0, gate: 1.0, pan: 0.5
                1474 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5234.0, gate: 1.0, pan: 0.5
                1473 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5223.0, gate: 1.0, pan: 0.5
                1472 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5212.0, gate: 1.0, pan: 0.5
                1471 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5201.0, gate: 1.0, pan: 0.5
                1470 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5190.0, gate: 1.0, pan: 0.5
                1469 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5179.0, gate: 1.0, pan: 0.5
                1468 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5168.0, gate: 1.0, pan: 0.5
                1467 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5157.0, gate: 1.0, pan: 0.5
                1466 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5146.0, gate: 1.0, pan: 0.5
                1465 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5135.0, gate: 1.0, pan: 0.5
                1464 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5124.0, gate: 1.0, pan: 0.5
                1463 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5113.0, gate: 1.0, pan: 0.5
                1462 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5102.0, gate: 1.0, pan: 0.5
                1461 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5091.0, gate: 1.0, pan: 0.5
                1460 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5080.0, gate: 1.0, pan: 0.5
                1459 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5069.0, gate: 1.0, pan: 0.5
                1458 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5058.0, gate: 1.0, pan: 0.5
                1457 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5047.0, gate: 1.0, pan: 0.5
                1456 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5036.0, gate: 1.0, pan: 0.5
                1455 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5025.0, gate: 1.0, pan: 0.5
                1454 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5014.0, gate: 1.0, pan: 0.5
                1453 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 5003.0, gate: 1.0, pan: 0.5
                1452 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4992.0, gate: 1.0, pan: 0.5
                1451 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4981.0, gate: 1.0, pan: 0.5
                1450 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4970.0, gate: 1.0, pan: 0.5
                1449 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4959.0, gate: 1.0, pan: 0.5
                1448 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4948.0, gate: 1.0, pan: 0.5
                1447 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4937.0, gate: 1.0, pan: 0.5
                1446 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4926.0, gate: 1.0, pan: 0.5
                1445 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4915.0, gate: 1.0, pan: 0.5
                1444 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4904.0, gate: 1.0, pan: 0.5
                1443 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4893.0, gate: 1.0, pan: 0.5
                1442 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4882.0, gate: 1.0, pan: 0.5
                1441 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4871.0, gate: 1.0, pan: 0.5
                1440 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4860.0, gate: 1.0, pan: 0.5
                1439 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4849.0, gate: 1.0, pan: 0.5
                1438 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4838.0, gate: 1.0, pan: 0.5
                1437 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4827.0, gate: 1.0, pan: 0.5
                1436 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4816.0, gate: 1.0, pan: 0.5
                1435 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4805.0, gate: 1.0, pan: 0.5
                1434 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4794.0, gate: 1.0, pan: 0.5
                1433 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4783.0, gate: 1.0, pan: 0.5
                1432 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4772.0, gate: 1.0, pan: 0.5
                1431 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4761.0, gate: 1.0, pan: 0.5
                1430 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4750.0, gate: 1.0, pan: 0.5
                1429 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4739.0, gate: 1.0, pan: 0.5
                1428 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4728.0, gate: 1.0, pan: 0.5
                1427 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4717.0, gate: 1.0, pan: 0.5
                1426 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4706.0, gate: 1.0, pan: 0.5
                1425 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4695.0, gate: 1.0, pan: 0.5
                1424 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4684.0, gate: 1.0, pan: 0.5
                1423 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4673.0, gate: 1.0, pan: 0.5
                1422 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4662.0, gate: 1.0, pan: 0.5
                1421 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4651.0, gate: 1.0, pan: 0.5
                1420 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4640.0, gate: 1.0, pan: 0.5
                1419 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4629.0, gate: 1.0, pan: 0.5
                1418 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4618.0, gate: 1.0, pan: 0.5
                1417 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4607.0, gate: 1.0, pan: 0.5
                1416 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4596.0, gate: 1.0, pan: 0.5
                1415 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4585.0, gate: 1.0, pan: 0.5
                1414 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4574.0, gate: 1.0, pan: 0.5
                1413 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4563.0, gate: 1.0, pan: 0.5
                1412 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4552.0, gate: 1.0, pan: 0.5
                1411 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4541.0, gate: 1.0, pan: 0.5
                1410 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4530.0, gate: 1.0, pan: 0.5
                1409 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4519.0, gate: 1.0, pan: 0.5
                1408 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4508.0, gate: 1.0, pan: 0.5
                1407 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4497.0, gate: 1.0, pan: 0.5
                1406 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4486.0, gate: 1.0, pan: 0.5
                1405 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4475.0, gate: 1.0, pan: 0.5
                1404 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4464.0, gate: 1.0, pan: 0.5
                1403 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4453.0, gate: 1.0, pan: 0.5
                1402 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4442.0, gate: 1.0, pan: 0.5
                1401 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4431.0, gate: 1.0, pan: 0.5
                1400 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4420.0, gate: 1.0, pan: 0.5
                1399 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4409.0, gate: 1.0, pan: 0.5
                1398 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4398.0, gate: 1.0, pan: 0.5
                1397 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4387.0, gate: 1.0, pan: 0.5
                1396 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4376.0, gate: 1.0, pan: 0.5
                1395 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4365.0, gate: 1.0, pan: 0.5
                1394 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4354.0, gate: 1.0, pan: 0.5
                1393 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4343.0, gate: 1.0, pan: 0.5
                1392 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4332.0, gate: 1.0, pan: 0.5
                1391 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4321.0, gate: 1.0, pan: 0.5
                1390 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4310.0, gate: 1.0, pan: 0.5
                1389 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4299.0, gate: 1.0, pan: 0.5
                1388 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4288.0, gate: 1.0, pan: 0.5
                1387 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4277.0, gate: 1.0, pan: 0.5
                1386 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4266.0, gate: 1.0, pan: 0.5
                1385 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4255.0, gate: 1.0, pan: 0.5
                1384 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4244.0, gate: 1.0, pan: 0.5
                1383 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4233.0, gate: 1.0, pan: 0.5
                1382 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4222.0, gate: 1.0, pan: 0.5
                1381 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4211.0, gate: 1.0, pan: 0.5
                1380 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4200.0, gate: 1.0, pan: 0.5
                1379 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4189.0, gate: 1.0, pan: 0.5
                1378 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4178.0, gate: 1.0, pan: 0.5
                1377 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4167.0, gate: 1.0, pan: 0.5
                1376 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4156.0, gate: 1.0, pan: 0.5
                1375 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4145.0, gate: 1.0, pan: 0.5
                1374 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4134.0, gate: 1.0, pan: 0.5
                1373 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4123.0, gate: 1.0, pan: 0.5
                1372 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4112.0, gate: 1.0, pan: 0.5
                1371 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4101.0, gate: 1.0, pan: 0.5
                1370 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4090.0, gate: 1.0, pan: 0.5
                1369 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4079.0, gate: 1.0, pan: 0.5
                1368 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4068.0, gate: 1.0, pan: 0.5
                1367 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4057.0, gate: 1.0, pan: 0.5
                1366 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4046.0, gate: 1.0, pan: 0.5
                1365 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4035.0, gate: 1.0, pan: 0.5
                1364 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4024.0, gate: 1.0, pan: 0.5
                1363 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4013.0, gate: 1.0, pan: 0.5
                1362 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 4002.0, gate: 1.0, pan: 0.5
                1361 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3991.0, gate: 1.0, pan: 0.5
                1360 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3980.0, gate: 1.0, pan: 0.5
                1359 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3969.0, gate: 1.0, pan: 0.5
                1358 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3958.0, gate: 1.0, pan: 0.5
                1357 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3947.0, gate: 1.0, pan: 0.5
                1356 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3936.0, gate: 1.0, pan: 0.5
                1355 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3925.0, gate: 1.0, pan: 0.5
                1354 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3914.0, gate: 1.0, pan: 0.5
                1353 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3903.0, gate: 1.0, pan: 0.5
                1352 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3892.0, gate: 1.0, pan: 0.5
                1351 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3881.0, gate: 1.0, pan: 0.5
                1350 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3870.0, gate: 1.0, pan: 0.5
                1349 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3859.0, gate: 1.0, pan: 0.5
                1348 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3848.0, gate: 1.0, pan: 0.5
                1347 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3837.0, gate: 1.0, pan: 0.5
                1346 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3826.0, gate: 1.0, pan: 0.5
                1345 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3815.0, gate: 1.0, pan: 0.5
                1344 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3804.0, gate: 1.0, pan: 0.5
                1343 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3793.0, gate: 1.0, pan: 0.5
                1342 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3782.0, gate: 1.0, pan: 0.5
                1341 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3771.0, gate: 1.0, pan: 0.5
                1340 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3760.0, gate: 1.0, pan: 0.5
                1339 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3749.0, gate: 1.0, pan: 0.5
                1338 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3738.0, gate: 1.0, pan: 0.5
                1337 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3727.0, gate: 1.0, pan: 0.5
                1336 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3716.0, gate: 1.0, pan: 0.5
                1335 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3705.0, gate: 1.0, pan: 0.5
                1334 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3694.0, gate: 1.0, pan: 0.5
                1333 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3683.0, gate: 1.0, pan: 0.5
                1332 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3672.0, gate: 1.0, pan: 0.5
                1331 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3661.0, gate: 1.0, pan: 0.5
                1330 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3650.0, gate: 1.0, pan: 0.5
                1329 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3639.0, gate: 1.0, pan: 0.5
                1328 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3628.0, gate: 1.0, pan: 0.5
                1327 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3617.0, gate: 1.0, pan: 0.5
                1326 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3606.0, gate: 1.0, pan: 0.5
                1325 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3595.0, gate: 1.0, pan: 0.5
                1324 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3584.0, gate: 1.0, pan: 0.5
                1323 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3573.0, gate: 1.0, pan: 0.5
                1322 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3562.0, gate: 1.0, pan: 0.5
                1321 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3551.0, gate: 1.0, pan: 0.5
                1320 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3540.0, gate: 1.0, pan: 0.5
                1319 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3529.0, gate: 1.0, pan: 0.5
                1318 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3518.0, gate: 1.0, pan: 0.5
                1317 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3507.0, gate: 1.0, pan: 0.5
                1316 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3496.0, gate: 1.0, pan: 0.5
                1315 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3485.0, gate: 1.0, pan: 0.5
                1314 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3474.0, gate: 1.0, pan: 0.5
                1313 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3463.0, gate: 1.0, pan: 0.5
                1312 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3452.0, gate: 1.0, pan: 0.5
                1311 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3441.0, gate: 1.0, pan: 0.5
                1310 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3430.0, gate: 1.0, pan: 0.5
                1309 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3419.0, gate: 1.0, pan: 0.5
                1308 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3408.0, gate: 1.0, pan: 0.5
                1307 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3397.0, gate: 1.0, pan: 0.5
                1306 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3386.0, gate: 1.0, pan: 0.5
                1305 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3375.0, gate: 1.0, pan: 0.5
                1304 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3364.0, gate: 1.0, pan: 0.5
                1303 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3353.0, gate: 1.0, pan: 0.5
                1302 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3342.0, gate: 1.0, pan: 0.5
                1301 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3331.0, gate: 1.0, pan: 0.5
                1300 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3320.0, gate: 1.0, pan: 0.5
                1299 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3309.0, gate: 1.0, pan: 0.5
                1298 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3298.0, gate: 1.0, pan: 0.5
                1297 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3287.0, gate: 1.0, pan: 0.5
                1296 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3276.0, gate: 1.0, pan: 0.5
                1295 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3265.0, gate: 1.0, pan: 0.5
                1294 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3254.0, gate: 1.0, pan: 0.5
                1293 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3243.0, gate: 1.0, pan: 0.5
                1292 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3232.0, gate: 1.0, pan: 0.5
                1291 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3221.0, gate: 1.0, pan: 0.5
                1290 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3210.0, gate: 1.0, pan: 0.5
                1289 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3199.0, gate: 1.0, pan: 0.5
                1288 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3188.0, gate: 1.0, pan: 0.5
                1287 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3177.0, gate: 1.0, pan: 0.5
                1286 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3166.0, gate: 1.0, pan: 0.5
                1285 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3155.0, gate: 1.0, pan: 0.5
                1284 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3144.0, gate: 1.0, pan: 0.5
                1283 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3133.0, gate: 1.0, pan: 0.5
                1282 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3122.0, gate: 1.0, pan: 0.5
                1281 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3111.0, gate: 1.0, pan: 0.5
                1280 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3100.0, gate: 1.0, pan: 0.5
                1279 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3089.0, gate: 1.0, pan: 0.5
                1278 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3078.0, gate: 1.0, pan: 0.5
                1277 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3067.0, gate: 1.0, pan: 0.5
                1276 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3056.0, gate: 1.0, pan: 0.5
                1275 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3045.0, gate: 1.0, pan: 0.5
                1274 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3034.0, gate: 1.0, pan: 0.5
                1273 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3023.0, gate: 1.0, pan: 0.5
                1272 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3012.0, gate: 1.0, pan: 0.5
                1271 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 3001.0, gate: 1.0, pan: 0.5
                1270 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2990.0, gate: 1.0, pan: 0.5
                1269 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2979.0, gate: 1.0, pan: 0.5
                1268 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2968.0, gate: 1.0, pan: 0.5
                1267 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2957.0, gate: 1.0, pan: 0.5
                1266 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2946.0, gate: 1.0, pan: 0.5
                1265 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2935.0, gate: 1.0, pan: 0.5
                1264 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2924.0, gate: 1.0, pan: 0.5
                1263 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2913.0, gate: 1.0, pan: 0.5
                1262 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2902.0, gate: 1.0, pan: 0.5
                1261 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2891.0, gate: 1.0, pan: 0.5
                1260 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2880.0, gate: 1.0, pan: 0.5
                1259 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2869.0, gate: 1.0, pan: 0.5
                1258 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2858.0, gate: 1.0, pan: 0.5
                1257 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2847.0, gate: 1.0, pan: 0.5
                1256 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2836.0, gate: 1.0, pan: 0.5
                1255 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2825.0, gate: 1.0, pan: 0.5
                1254 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2814.0, gate: 1.0, pan: 0.5
                1253 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2803.0, gate: 1.0, pan: 0.5
                1252 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2792.0, gate: 1.0, pan: 0.5
                1251 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2781.0, gate: 1.0, pan: 0.5
                1250 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2770.0, gate: 1.0, pan: 0.5
                1249 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2759.0, gate: 1.0, pan: 0.5
                1248 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2748.0, gate: 1.0, pan: 0.5
                1247 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2737.0, gate: 1.0, pan: 0.5
                1246 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2726.0, gate: 1.0, pan: 0.5
                1245 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2715.0, gate: 1.0, pan: 0.5
                1244 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2704.0, gate: 1.0, pan: 0.5
                1243 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2693.0, gate: 1.0, pan: 0.5
                1242 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2682.0, gate: 1.0, pan: 0.5
                1241 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2671.0, gate: 1.0, pan: 0.5
                1240 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2660.0, gate: 1.0, pan: 0.5
                1239 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2649.0, gate: 1.0, pan: 0.5
                1238 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2638.0, gate: 1.0, pan: 0.5
                1237 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2627.0, gate: 1.0, pan: 0.5
                1236 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2616.0, gate: 1.0, pan: 0.5
                1235 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2605.0, gate: 1.0, pan: 0.5
                1234 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2594.0, gate: 1.0, pan: 0.5
                1233 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2583.0, gate: 1.0, pan: 0.5
                1232 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2572.0, gate: 1.0, pan: 0.5
                1231 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2561.0, gate: 1.0, pan: 0.5
                1230 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2550.0, gate: 1.0, pan: 0.5
                1229 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2539.0, gate: 1.0, pan: 0.5
                1228 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2528.0, gate: 1.0, pan: 0.5
                1227 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2517.0, gate: 1.0, pan: 0.5
                1226 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2506.0, gate: 1.0, pan: 0.5
                1225 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2495.0, gate: 1.0, pan: 0.5
                1224 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2484.0, gate: 1.0, pan: 0.5
                1223 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2473.0, gate: 1.0, pan: 0.5
                1222 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2462.0, gate: 1.0, pan: 0.5
                1221 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2451.0, gate: 1.0, pan: 0.5
                1220 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2440.0, gate: 1.0, pan: 0.5
                1219 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2429.0, gate: 1.0, pan: 0.5
                1218 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2418.0, gate: 1.0, pan: 0.5
                1217 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2407.0, gate: 1.0, pan: 0.5
                1216 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2396.0, gate: 1.0, pan: 0.5
                1215 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2385.0, gate: 1.0, pan: 0.5
                1214 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2374.0, gate: 1.0, pan: 0.5
                1213 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2363.0, gate: 1.0, pan: 0.5
                1212 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2352.0, gate: 1.0, pan: 0.5
                1211 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2341.0, gate: 1.0, pan: 0.5
                1210 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2330.0, gate: 1.0, pan: 0.5
                1209 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2319.0, gate: 1.0, pan: 0.5
                1208 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2308.0, gate: 1.0, pan: 0.5
                1207 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2297.0, gate: 1.0, pan: 0.5
                1206 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2286.0, gate: 1.0, pan: 0.5
                1205 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2275.0, gate: 1.0, pan: 0.5
                1204 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2264.0, gate: 1.0, pan: 0.5
                1203 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2253.0, gate: 1.0, pan: 0.5
                1202 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2242.0, gate: 1.0, pan: 0.5
                1201 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2231.0, gate: 1.0, pan: 0.5
                1200 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2220.0, gate: 1.0, pan: 0.5
                1199 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2209.0, gate: 1.0, pan: 0.5
                1198 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2198.0, gate: 1.0, pan: 0.5
                1197 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2187.0, gate: 1.0, pan: 0.5
                1196 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2176.0, gate: 1.0, pan: 0.5
                1195 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2165.0, gate: 1.0, pan: 0.5
                1194 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2154.0, gate: 1.0, pan: 0.5
                1193 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2143.0, gate: 1.0, pan: 0.5
                1192 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2132.0, gate: 1.0, pan: 0.5
                1191 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2121.0, gate: 1.0, pan: 0.5
                1190 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2110.0, gate: 1.0, pan: 0.5
                1189 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2099.0, gate: 1.0, pan: 0.5
                1188 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2088.0, gate: 1.0, pan: 0.5
                1187 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2077.0, gate: 1.0, pan: 0.5
                1186 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2066.0, gate: 1.0, pan: 0.5
                1185 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2055.0, gate: 1.0, pan: 0.5
                1184 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2044.0, gate: 1.0, pan: 0.5
                1183 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2033.0, gate: 1.0, pan: 0.5
                1182 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2022.0, gate: 1.0, pan: 0.5
                1181 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2011.0, gate: 1.0, pan: 0.5
                1180 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 2000.0, gate: 1.0, pan: 0.5
                1179 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1989.0, gate: 1.0, pan: 0.5
                1178 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1978.0, gate: 1.0, pan: 0.5
                1177 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1967.0, gate: 1.0, pan: 0.5
                1176 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1956.0, gate: 1.0, pan: 0.5
                1175 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1945.0, gate: 1.0, pan: 0.5
                1174 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1934.0, gate: 1.0, pan: 0.5
                1173 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1923.0, gate: 1.0, pan: 0.5
                1172 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1912.0, gate: 1.0, pan: 0.5
                1171 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1901.0, gate: 1.0, pan: 0.5
                1170 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1890.0, gate: 1.0, pan: 0.5
                1169 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1879.0, gate: 1.0, pan: 0.5
                1168 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1868.0, gate: 1.0, pan: 0.5
                1167 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1857.0, gate: 1.0, pan: 0.5
                1166 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1846.0, gate: 1.0, pan: 0.5
                1165 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1835.0, gate: 1.0, pan: 0.5
                1164 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1824.0, gate: 1.0, pan: 0.5
                1163 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1813.0, gate: 1.0, pan: 0.5
                1162 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1802.0, gate: 1.0, pan: 0.5
                1161 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1791.0, gate: 1.0, pan: 0.5
                1160 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1780.0, gate: 1.0, pan: 0.5
                1159 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1769.0, gate: 1.0, pan: 0.5
                1158 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1758.0, gate: 1.0, pan: 0.5
                1157 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1747.0, gate: 1.0, pan: 0.5
                1156 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1736.0, gate: 1.0, pan: 0.5
                1155 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1725.0, gate: 1.0, pan: 0.5
                1154 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1714.0, gate: 1.0, pan: 0.5
                1153 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1703.0, gate: 1.0, pan: 0.5
                1152 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1692.0, gate: 1.0, pan: 0.5
                1151 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1681.0, gate: 1.0, pan: 0.5
                1150 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1670.0, gate: 1.0, pan: 0.5
                1149 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1659.0, gate: 1.0, pan: 0.5
                1148 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1648.0, gate: 1.0, pan: 0.5
                1147 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1637.0, gate: 1.0, pan: 0.5
                1146 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1626.0, gate: 1.0, pan: 0.5
                1145 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1615.0, gate: 1.0, pan: 0.5
                1144 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1604.0, gate: 1.0, pan: 0.5
                1143 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1593.0, gate: 1.0, pan: 0.5
                1142 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1582.0, gate: 1.0, pan: 0.5
                1141 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1571.0, gate: 1.0, pan: 0.5
                1140 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1560.0, gate: 1.0, pan: 0.5
                1139 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1549.0, gate: 1.0, pan: 0.5
                1138 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1538.0, gate: 1.0, pan: 0.5
                1137 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1527.0, gate: 1.0, pan: 0.5
                1136 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1516.0, gate: 1.0, pan: 0.5
                1135 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1505.0, gate: 1.0, pan: 0.5
                1134 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1494.0, gate: 1.0, pan: 0.5
                1133 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1483.0, gate: 1.0, pan: 0.5
                1132 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1472.0, gate: 1.0, pan: 0.5
                1131 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1461.0, gate: 1.0, pan: 0.5
                1130 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1450.0, gate: 1.0, pan: 0.5
                1129 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1439.0, gate: 1.0, pan: 0.5
                1128 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1428.0, gate: 1.0, pan: 0.5
                1127 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1417.0, gate: 1.0, pan: 0.5
                1126 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1406.0, gate: 1.0, pan: 0.5
                1125 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1395.0, gate: 1.0, pan: 0.5
                1124 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1384.0, gate: 1.0, pan: 0.5
                1123 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1373.0, gate: 1.0, pan: 0.5
                1122 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1362.0, gate: 1.0, pan: 0.5
                1121 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1351.0, gate: 1.0, pan: 0.5
                1120 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1340.0, gate: 1.0, pan: 0.5
                1119 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1329.0, gate: 1.0, pan: 0.5
                1118 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1318.0, gate: 1.0, pan: 0.5
                1117 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1307.0, gate: 1.0, pan: 0.5
                1116 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1296.0, gate: 1.0, pan: 0.5
                1115 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1285.0, gate: 1.0, pan: 0.5
                1114 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1274.0, gate: 1.0, pan: 0.5
                1113 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1263.0, gate: 1.0, pan: 0.5
                1112 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1252.0, gate: 1.0, pan: 0.5
                1111 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1241.0, gate: 1.0, pan: 0.5
                1110 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1230.0, gate: 1.0, pan: 0.5
                1109 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1219.0, gate: 1.0, pan: 0.5
                1108 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1208.0, gate: 1.0, pan: 0.5
                1107 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1197.0, gate: 1.0, pan: 0.5
                1106 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1186.0, gate: 1.0, pan: 0.5
                1105 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1175.0, gate: 1.0, pan: 0.5
                1104 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1164.0, gate: 1.0, pan: 0.5
                1103 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1153.0, gate: 1.0, pan: 0.5
                1102 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1142.0, gate: 1.0, pan: 0.5
                1101 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1131.0, gate: 1.0, pan: 0.5
                1100 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1120.0, gate: 1.0, pan: 0.5
                1099 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1109.0, gate: 1.0, pan: 0.5
                1098 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1098.0, gate: 1.0, pan: 0.5
                1097 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1087.0, gate: 1.0, pan: 0.5
                1096 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1076.0, gate: 1.0, pan: 0.5
                1095 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1065.0, gate: 1.0, pan: 0.5
                1094 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1054.0, gate: 1.0, pan: 0.5
                1093 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1043.0, gate: 1.0, pan: 0.5
                1092 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1032.0, gate: 1.0, pan: 0.5
                1091 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1021.0, gate: 1.0, pan: 0.5
                1090 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 1010.0, gate: 1.0, pan: 0.5
                1089 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 999.0, gate: 1.0, pan: 0.5
                1088 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 988.0, gate: 1.0, pan: 0.5
                1087 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 977.0, gate: 1.0, pan: 0.5
                1086 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 966.0, gate: 1.0, pan: 0.5
                1085 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 955.0, gate: 1.0, pan: 0.5
                1084 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 944.0, gate: 1.0, pan: 0.5
                1083 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 933.0, gate: 1.0, pan: 0.5
                1082 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 922.0, gate: 1.0, pan: 0.5
                1081 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 911.0, gate: 1.0, pan: 0.5
                1080 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 900.0, gate: 1.0, pan: 0.5
                1079 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 889.0, gate: 1.0, pan: 0.5
                1078 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 878.0, gate: 1.0, pan: 0.5
                1077 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 867.0, gate: 1.0, pan: 0.5
                1076 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 856.0, gate: 1.0, pan: 0.5
                1075 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 845.0, gate: 1.0, pan: 0.5
                1074 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 834.0, gate: 1.0, pan: 0.5
                1073 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 823.0, gate: 1.0, pan: 0.5
                1072 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 812.0, gate: 1.0, pan: 0.5
                1071 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 801.0, gate: 1.0, pan: 0.5
                1070 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 790.0, gate: 1.0, pan: 0.5
                1069 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 779.0, gate: 1.0, pan: 0.5
                1068 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 768.0, gate: 1.0, pan: 0.5
                1067 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 757.0, gate: 1.0, pan: 0.5
                1066 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 746.0, gate: 1.0, pan: 0.5
                1065 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 735.0, gate: 1.0, pan: 0.5
                1064 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 724.0, gate: 1.0, pan: 0.5
                1063 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 713.0, gate: 1.0, pan: 0.5
                1062 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 702.0, gate: 1.0, pan: 0.5
                1061 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 691.0, gate: 1.0, pan: 0.5
                1060 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 680.0, gate: 1.0, pan: 0.5
                1059 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 669.0, gate: 1.0, pan: 0.5
                1058 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 658.0, gate: 1.0, pan: 0.5
                1057 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 647.0, gate: 1.0, pan: 0.5
                1056 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 636.0, gate: 1.0, pan: 0.5
                1055 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 625.0, gate: 1.0, pan: 0.5
                1054 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 614.0, gate: 1.0, pan: 0.5
                1053 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 603.0, gate: 1.0, pan: 0.5
                1052 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 592.0, gate: 1.0, pan: 0.5
                1051 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 581.0, gate: 1.0, pan: 0.5
                1050 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 570.0, gate: 1.0, pan: 0.5
                1049 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 559.0, gate: 1.0, pan: 0.5
                1048 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 548.0, gate: 1.0, pan: 0.5
                1047 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 537.0, gate: 1.0, pan: 0.5
                1046 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 526.0, gate: 1.0, pan: 0.5
                1045 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 515.0, gate: 1.0, pan: 0.5
                1044 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 504.0, gate: 1.0, pan: 0.5
                1043 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 493.0, gate: 1.0, pan: 0.5
                1042 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 482.0, gate: 1.0, pan: 0.5
                1041 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 471.0, gate: 1.0, pan: 0.5
                1040 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 460.0, gate: 1.0, pan: 0.5
                1039 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 449.0, gate: 1.0, pan: 0.5
                1038 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 438.0, gate: 1.0, pan: 0.5
                1037 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 427.0, gate: 1.0, pan: 0.5
                1036 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 416.0, gate: 1.0, pan: 0.5
                1035 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 405.0, gate: 1.0, pan: 0.5
                1034 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 394.0, gate: 1.0, pan: 0.5
                1033 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 383.0, gate: 1.0, pan: 0.5
                1032 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 372.0, gate: 1.0, pan: 0.5
                1031 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 361.0, gate: 1.0, pan: 0.5
                1030 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 350.0, gate: 1.0, pan: 0.5
                1029 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 339.0, gate: 1.0, pan: 0.5
                1028 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 328.0, gate: 1.0, pan: 0.5
                1027 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 317.0, gate: 1.0, pan: 0.5
                1026 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 306.0, gate: 1.0, pan: 0.5
                1025 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 295.0, gate: 1.0, pan: 0.5
                1024 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 284.0, gate: 1.0, pan: 0.5
                1023 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 273.0, gate: 1.0, pan: 0.5
                1022 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 262.0, gate: 1.0, pan: 0.5
                1021 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 251.0, gate: 1.0, pan: 0.5
                1020 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 240.0, gate: 1.0, pan: 0.5
                1019 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 229.0, gate: 1.0, pan: 0.5
                1018 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 218.0, gate: 1.0, pan: 0.5
                1017 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 207.0, gate: 1.0, pan: 0.5
                1016 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 196.0, gate: 1.0, pan: 0.5
                1015 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 185.0, gate: 1.0, pan: 0.5
                1014 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 174.0, gate: 1.0, pan: 0.5
                1013 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 163.0, gate: 1.0, pan: 0.5
                1012 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 152.0, gate: 1.0, pan: 0.5
                1011 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 141.0, gate: 1.0, pan: 0.5
                1010 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 130.0, gate: 1.0, pan: 0.5
                1009 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 119.0, gate: 1.0, pan: 0.5
                1008 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 108.0, gate: 1.0, pan: 0.5
                1007 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 97.0, gate: 1.0, pan: 0.5
                1006 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 86.0, gate: 1.0, pan: 0.5
                1005 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 75.0, gate: 1.0, pan: 0.5
                1004 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 64.0, gate: 1.0, pan: 0.5
                1003 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 53.0, gate: 1.0, pan: 0.5
                1002 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 42.0, gate: 1.0, pan: 0.5
                1001 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 31.0, gate: 1.0, pan: 0.5
                1000 supriya:default
                    out: 0.0, amplitude: 0.5, frequency: 20.0, gate: 1.0, pan: 0.5
        """
    )


@pytest.mark.asyncio
async def test_query_status(context: AsyncServer | Server) -> None:
    assert isinstance(await get(context.query_status()), StatusInfo)
    # unsync
    with context.osc_protocol.capture() as transcript:
        assert await get(context.query_status(sync=False)) is None
    assert transcript.filtered(received=False, status=True) == [OscMessage("/status")]


@pytest.mark.asyncio
async def test_query_tree(context: AsyncServer | Server) -> None:
    with context.at():
        group_a = context.add_group()
        group_b = context.add_group()
        group_a.add_synth(default, frequency=111)
        group_b.add_synth(default, frequency=222)
        synth = group_b.add_synth(default, add_action="ADD_TO_TAIL", frequency=333)
        synth.add_group(add_action="ADD_AFTER")
    await get(context.sync())
    with context.osc_protocol.capture() as transcript:
        tree = await get(context.query_tree())
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/g_queryTree", 0, 1)
    ]
    assert str(tree) == normalize(
        """
        NODE TREE 0 group
            1 group
                1001 group
                    1003 supriya:default
                        out: 0.0, amplitude: 0.1, frequency: 222.0, gate: 1.0, pan: 0.5
                    1004 supriya:default
                        out: 0.0, amplitude: 0.1, frequency: 333.0, gate: 1.0, pan: 0.5
                    1005 group
                1000 group
                    1002 supriya:default
                        out: 0.0, amplitude: 0.1, frequency: 111.0, gate: 1.0, pan: 0.5
        """
    )
    # unsync
    with context.osc_protocol.capture() as transcript:
        assert await get(context.query_tree(sync=False)) is None
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/g_queryTree", 0, 1)
    ]


@pytest.mark.asyncio
async def test_query_version(context: AsyncServer | Server) -> None:
    completed_subprocess = subprocess.run(
        [scsynth.find("scsynth"), "-v"], capture_output=True, text=True
    )
    stdout = completed_subprocess.stdout
    line = completed_subprocess.stdout.splitlines()[0]
    print(stdout, line)
    assert (
        match := re.match(
            r"(\w+) (\d+)\.(\d+)(\.[\w-]+) \(Built from (?:branch|tag) '([\W\w]+)' \[([\W\w]+)\]\)",
            line,
        )
    ) is not None
    program_name, major, minor, patch, ref, commit = match.groups()
    expected_info = VersionInfo(
        program_name=program_name,
        major=int(major),
        minor=int(minor),
        patch=patch,
        branch=ref,
        commit=commit,
    )
    assert await get(context.query_version()) == expected_info
    # unsync
    with context.osc_protocol.capture() as transcript:
        assert await get(context.query_version(sync=False)) is None
    assert transcript.filtered(received=False, status=False) == [OscMessage("/version")]


@pytest.mark.asyncio
async def test_reboot(context: AsyncServer | Server) -> None:
    # TODO: expand this

    def callback(event: ServerLifecycleEvent) -> None:
        events.append(event)

    events: list[ServerLifecycleEvent] = []
    for event in ServerLifecycleEvent:
        context.register_lifecycle_callback(event, callback)
    with context.osc_protocol.capture() as transcript:
        await get(context.reboot())
    assert events == [
        ServerLifecycleEvent.QUITTING,
        ServerLifecycleEvent.DISCONNECTING,
        ServerLifecycleEvent.OSC_DISCONNECTED,
        ServerLifecycleEvent.DISCONNECTED,
        ServerLifecycleEvent.PROCESS_QUIT,
        ServerLifecycleEvent.QUIT,
        ServerLifecycleEvent.BOOTING,
        ServerLifecycleEvent.PROCESS_BOOTED,
        ServerLifecycleEvent.CONNECTING,
        ServerLifecycleEvent.OSC_CONNECTED,
        ServerLifecycleEvent.CONNECTED,
        ServerLifecycleEvent.BOOTED,
    ]
    assert transcript.filtered(received=False, sent=True, status=False) == [
        OscMessage("/quit"),
        OscMessage("/notify", 1),
        OscMessage("/g_new", 1, 1, 0),
        *(
            OscMessage("/d_recv", synthdef.compile())
            for synthdef in SYSTEM_SYNTHDEFS.values()
        ),
        OscMessage("/sync", 0),
    ]


@pytest.mark.asyncio
async def test_register_lifecycle_callback(context: AsyncServer | Server) -> None:
    def procedure(event: ServerLifecycleEvent) -> None:
        events.append(event)

    events: list[ServerLifecycleEvent] = []
    callback = context.register_lifecycle_callback(ServerLifecycleEvent.QUIT, procedure)
    assert isinstance(callback, ServerLifecycleCallback)
    await get(context.quit())
    assert events == [ServerLifecycleEvent.QUIT]


@pytest.mark.asyncio
async def test_register_osc_callback(context: AsyncServer | Server) -> None:
    def procedure(osc_message: OscMessage) -> None:
        osc_messages.append(osc_message)

    osc_messages: list[OscMessage] = []
    callback = context.register_osc_callback("/synced", procedure)
    assert isinstance(callback, OscCallback)
    await get(context.sync())
    assert osc_messages == [OscMessage("/synced", 2)]


@pytest.mark.asyncio
async def test_reset(context: AsyncServer | Server) -> None:
    # TODO: expand this
    def callback(event: ServerLifecycleEvent) -> None:
        events.append(event)

    events: list[ServerLifecycleEvent] = []
    for event in ServerLifecycleEvent:
        context.register_lifecycle_callback(event, callback)
    with context.osc_protocol.capture() as transcript:
        await get(context.reset())
    assert events == []
    assert transcript.filtered(received=False, sent=True, status=False) == [
        OscBundle(
            contents=[
                OscMessage("/clearSched"),
                OscMessage("/g_freeAll", 0),
                OscMessage("/d_freeAll"),
            ]
        ),
        OscMessage("/sync", 2),
        OscMessage("/g_new", 1, 1, 0),
        *(
            OscMessage("/d_recv", synthdef.compile())
            for synthdef in SYSTEM_SYNTHDEFS.values()
        ),
        OscMessage("/sync", 0),
    ]


@pytest.mark.asyncio
async def test_root_node(context: AsyncServer | Server) -> None:
    assert isinstance(context.root_node, Group)
    assert context.root_node.context is context
    assert context.root_node.id_ == 0


@pytest.mark.asyncio
async def test_sync(context: AsyncServer | Server) -> None:
    with context.osc_protocol.capture() as transcript:
        await get(context.sync())
        await get(context.sync())
        await get(context.sync())
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/sync", 2),
        OscMessage("/sync", 3),
        OscMessage("/sync", 4),
    ]
    await get(context.quit())
    with pytest.raises(ServerOffline):
        await get(context.sync())


@pytest.mark.asyncio
async def test_unregister_lifecycle_callback(context: AsyncServer | Server) -> None:
    def procedure(event: ServerLifecycleEvent) -> None:
        events.append(event)

    events: list[ServerLifecycleEvent] = []
    callback = context.register_lifecycle_callback(ServerLifecycleEvent.QUIT, procedure)
    assert isinstance(callback, ServerLifecycleCallback)
    callback.unregister()
    await get(context.quit())
    assert events == []


@pytest.mark.asyncio
async def test_unregister_osc_callback(context: AsyncServer | Server) -> None:
    def procedure(osc_message: OscMessage) -> None:
        osc_messages.append(osc_message)

    osc_messages: list[OscMessage] = []
    callback = context.register_osc_callback("/synced", procedure)
    assert isinstance(callback, OscCallback)
    callback.unregister()
    await get(context.sync())
    assert osc_messages == []
