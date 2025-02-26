import asyncio
import logging
import re
import subprocess
import sys

import pytest
import pytest_asyncio
from uqbar.strings import normalize

from supriya import (
    AsyncServer,
    Group,
    OscBundle,
    OscMessage,
    Server,
    ServerLifecycleEvent,
    default,
    scsynth,
)
from supriya.assets import synthdefs
from supriya.contexts.responses import StatusInfo, VersionInfo
from supriya.exceptions import ServerOffline


async def get(x):
    if asyncio.iscoroutine(x):
        return await x
    return x


@pytest.fixture(autouse=True)
def use_caplog(caplog):
    caplog.set_level(logging.INFO)


@pytest_asyncio.fixture(autouse=True, params=[AsyncServer, Server])
async def context(request):
    context = request.param()
    await get(context.boot())
    context.add_synthdefs(default)
    await get(context.sync())
    yield context


@pytest.mark.asyncio
async def test_clear_schedule(context):
    with context.osc_protocol.capture() as transcript:
        context.clear_schedule()
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/clearSched")
    ]


@pytest.mark.asyncio
async def test_default_group(context):
    assert isinstance(context.default_group, Group)
    assert context.default_group.context is context
    assert context.default_group.id_ == context.client_id + 1


# Under 3.10/11 we often see the server not receive the sync response,
# so this will time-out.
@pytest.mark.flaky(reruns=5, conditions=sys.version_info[:2] in [(3, 10), (3, 11)])
@pytest.mark.asyncio
async def test_dump_tree(context):
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
                1499 default
                    amplitude: 0.5, frequency: 5509.0, gate: 1.0, pan: 0.5, out: 0.0
                1498 default
                    amplitude: 0.5, frequency: 5498.0, gate: 1.0, pan: 0.5, out: 0.0
                1497 default
                    amplitude: 0.5, frequency: 5487.0, gate: 1.0, pan: 0.5, out: 0.0
                1496 default
                    amplitude: 0.5, frequency: 5476.0, gate: 1.0, pan: 0.5, out: 0.0
                1495 default
                    amplitude: 0.5, frequency: 5465.0, gate: 1.0, pan: 0.5, out: 0.0
                1494 default
                    amplitude: 0.5, frequency: 5454.0, gate: 1.0, pan: 0.5, out: 0.0
                1493 default
                    amplitude: 0.5, frequency: 5443.0, gate: 1.0, pan: 0.5, out: 0.0
                1492 default
                    amplitude: 0.5, frequency: 5432.0, gate: 1.0, pan: 0.5, out: 0.0
                1491 default
                    amplitude: 0.5, frequency: 5421.0, gate: 1.0, pan: 0.5, out: 0.0
                1490 default
                    amplitude: 0.5, frequency: 5410.0, gate: 1.0, pan: 0.5, out: 0.0
                1489 default
                    amplitude: 0.5, frequency: 5399.0, gate: 1.0, pan: 0.5, out: 0.0
                1488 default
                    amplitude: 0.5, frequency: 5388.0, gate: 1.0, pan: 0.5, out: 0.0
                1487 default
                    amplitude: 0.5, frequency: 5377.0, gate: 1.0, pan: 0.5, out: 0.0
                1486 default
                    amplitude: 0.5, frequency: 5366.0, gate: 1.0, pan: 0.5, out: 0.0
                1485 default
                    amplitude: 0.5, frequency: 5355.0, gate: 1.0, pan: 0.5, out: 0.0
                1484 default
                    amplitude: 0.5, frequency: 5344.0, gate: 1.0, pan: 0.5, out: 0.0
                1483 default
                    amplitude: 0.5, frequency: 5333.0, gate: 1.0, pan: 0.5, out: 0.0
                1482 default
                    amplitude: 0.5, frequency: 5322.0, gate: 1.0, pan: 0.5, out: 0.0
                1481 default
                    amplitude: 0.5, frequency: 5311.0, gate: 1.0, pan: 0.5, out: 0.0
                1480 default
                    amplitude: 0.5, frequency: 5300.0, gate: 1.0, pan: 0.5, out: 0.0
                1479 default
                    amplitude: 0.5, frequency: 5289.0, gate: 1.0, pan: 0.5, out: 0.0
                1478 default
                    amplitude: 0.5, frequency: 5278.0, gate: 1.0, pan: 0.5, out: 0.0
                1477 default
                    amplitude: 0.5, frequency: 5267.0, gate: 1.0, pan: 0.5, out: 0.0
                1476 default
                    amplitude: 0.5, frequency: 5256.0, gate: 1.0, pan: 0.5, out: 0.0
                1475 default
                    amplitude: 0.5, frequency: 5245.0, gate: 1.0, pan: 0.5, out: 0.0
                1474 default
                    amplitude: 0.5, frequency: 5234.0, gate: 1.0, pan: 0.5, out: 0.0
                1473 default
                    amplitude: 0.5, frequency: 5223.0, gate: 1.0, pan: 0.5, out: 0.0
                1472 default
                    amplitude: 0.5, frequency: 5212.0, gate: 1.0, pan: 0.5, out: 0.0
                1471 default
                    amplitude: 0.5, frequency: 5201.0, gate: 1.0, pan: 0.5, out: 0.0
                1470 default
                    amplitude: 0.5, frequency: 5190.0, gate: 1.0, pan: 0.5, out: 0.0
                1469 default
                    amplitude: 0.5, frequency: 5179.0, gate: 1.0, pan: 0.5, out: 0.0
                1468 default
                    amplitude: 0.5, frequency: 5168.0, gate: 1.0, pan: 0.5, out: 0.0
                1467 default
                    amplitude: 0.5, frequency: 5157.0, gate: 1.0, pan: 0.5, out: 0.0
                1466 default
                    amplitude: 0.5, frequency: 5146.0, gate: 1.0, pan: 0.5, out: 0.0
                1465 default
                    amplitude: 0.5, frequency: 5135.0, gate: 1.0, pan: 0.5, out: 0.0
                1464 default
                    amplitude: 0.5, frequency: 5124.0, gate: 1.0, pan: 0.5, out: 0.0
                1463 default
                    amplitude: 0.5, frequency: 5113.0, gate: 1.0, pan: 0.5, out: 0.0
                1462 default
                    amplitude: 0.5, frequency: 5102.0, gate: 1.0, pan: 0.5, out: 0.0
                1461 default
                    amplitude: 0.5, frequency: 5091.0, gate: 1.0, pan: 0.5, out: 0.0
                1460 default
                    amplitude: 0.5, frequency: 5080.0, gate: 1.0, pan: 0.5, out: 0.0
                1459 default
                    amplitude: 0.5, frequency: 5069.0, gate: 1.0, pan: 0.5, out: 0.0
                1458 default
                    amplitude: 0.5, frequency: 5058.0, gate: 1.0, pan: 0.5, out: 0.0
                1457 default
                    amplitude: 0.5, frequency: 5047.0, gate: 1.0, pan: 0.5, out: 0.0
                1456 default
                    amplitude: 0.5, frequency: 5036.0, gate: 1.0, pan: 0.5, out: 0.0
                1455 default
                    amplitude: 0.5, frequency: 5025.0, gate: 1.0, pan: 0.5, out: 0.0
                1454 default
                    amplitude: 0.5, frequency: 5014.0, gate: 1.0, pan: 0.5, out: 0.0
                1453 default
                    amplitude: 0.5, frequency: 5003.0, gate: 1.0, pan: 0.5, out: 0.0
                1452 default
                    amplitude: 0.5, frequency: 4992.0, gate: 1.0, pan: 0.5, out: 0.0
                1451 default
                    amplitude: 0.5, frequency: 4981.0, gate: 1.0, pan: 0.5, out: 0.0
                1450 default
                    amplitude: 0.5, frequency: 4970.0, gate: 1.0, pan: 0.5, out: 0.0
                1449 default
                    amplitude: 0.5, frequency: 4959.0, gate: 1.0, pan: 0.5, out: 0.0
                1448 default
                    amplitude: 0.5, frequency: 4948.0, gate: 1.0, pan: 0.5, out: 0.0
                1447 default
                    amplitude: 0.5, frequency: 4937.0, gate: 1.0, pan: 0.5, out: 0.0
                1446 default
                    amplitude: 0.5, frequency: 4926.0, gate: 1.0, pan: 0.5, out: 0.0
                1445 default
                    amplitude: 0.5, frequency: 4915.0, gate: 1.0, pan: 0.5, out: 0.0
                1444 default
                    amplitude: 0.5, frequency: 4904.0, gate: 1.0, pan: 0.5, out: 0.0
                1443 default
                    amplitude: 0.5, frequency: 4893.0, gate: 1.0, pan: 0.5, out: 0.0
                1442 default
                    amplitude: 0.5, frequency: 4882.0, gate: 1.0, pan: 0.5, out: 0.0
                1441 default
                    amplitude: 0.5, frequency: 4871.0, gate: 1.0, pan: 0.5, out: 0.0
                1440 default
                    amplitude: 0.5, frequency: 4860.0, gate: 1.0, pan: 0.5, out: 0.0
                1439 default
                    amplitude: 0.5, frequency: 4849.0, gate: 1.0, pan: 0.5, out: 0.0
                1438 default
                    amplitude: 0.5, frequency: 4838.0, gate: 1.0, pan: 0.5, out: 0.0
                1437 default
                    amplitude: 0.5, frequency: 4827.0, gate: 1.0, pan: 0.5, out: 0.0
                1436 default
                    amplitude: 0.5, frequency: 4816.0, gate: 1.0, pan: 0.5, out: 0.0
                1435 default
                    amplitude: 0.5, frequency: 4805.0, gate: 1.0, pan: 0.5, out: 0.0
                1434 default
                    amplitude: 0.5, frequency: 4794.0, gate: 1.0, pan: 0.5, out: 0.0
                1433 default
                    amplitude: 0.5, frequency: 4783.0, gate: 1.0, pan: 0.5, out: 0.0
                1432 default
                    amplitude: 0.5, frequency: 4772.0, gate: 1.0, pan: 0.5, out: 0.0
                1431 default
                    amplitude: 0.5, frequency: 4761.0, gate: 1.0, pan: 0.5, out: 0.0
                1430 default
                    amplitude: 0.5, frequency: 4750.0, gate: 1.0, pan: 0.5, out: 0.0
                1429 default
                    amplitude: 0.5, frequency: 4739.0, gate: 1.0, pan: 0.5, out: 0.0
                1428 default
                    amplitude: 0.5, frequency: 4728.0, gate: 1.0, pan: 0.5, out: 0.0
                1427 default
                    amplitude: 0.5, frequency: 4717.0, gate: 1.0, pan: 0.5, out: 0.0
                1426 default
                    amplitude: 0.5, frequency: 4706.0, gate: 1.0, pan: 0.5, out: 0.0
                1425 default
                    amplitude: 0.5, frequency: 4695.0, gate: 1.0, pan: 0.5, out: 0.0
                1424 default
                    amplitude: 0.5, frequency: 4684.0, gate: 1.0, pan: 0.5, out: 0.0
                1423 default
                    amplitude: 0.5, frequency: 4673.0, gate: 1.0, pan: 0.5, out: 0.0
                1422 default
                    amplitude: 0.5, frequency: 4662.0, gate: 1.0, pan: 0.5, out: 0.0
                1421 default
                    amplitude: 0.5, frequency: 4651.0, gate: 1.0, pan: 0.5, out: 0.0
                1420 default
                    amplitude: 0.5, frequency: 4640.0, gate: 1.0, pan: 0.5, out: 0.0
                1419 default
                    amplitude: 0.5, frequency: 4629.0, gate: 1.0, pan: 0.5, out: 0.0
                1418 default
                    amplitude: 0.5, frequency: 4618.0, gate: 1.0, pan: 0.5, out: 0.0
                1417 default
                    amplitude: 0.5, frequency: 4607.0, gate: 1.0, pan: 0.5, out: 0.0
                1416 default
                    amplitude: 0.5, frequency: 4596.0, gate: 1.0, pan: 0.5, out: 0.0
                1415 default
                    amplitude: 0.5, frequency: 4585.0, gate: 1.0, pan: 0.5, out: 0.0
                1414 default
                    amplitude: 0.5, frequency: 4574.0, gate: 1.0, pan: 0.5, out: 0.0
                1413 default
                    amplitude: 0.5, frequency: 4563.0, gate: 1.0, pan: 0.5, out: 0.0
                1412 default
                    amplitude: 0.5, frequency: 4552.0, gate: 1.0, pan: 0.5, out: 0.0
                1411 default
                    amplitude: 0.5, frequency: 4541.0, gate: 1.0, pan: 0.5, out: 0.0
                1410 default
                    amplitude: 0.5, frequency: 4530.0, gate: 1.0, pan: 0.5, out: 0.0
                1409 default
                    amplitude: 0.5, frequency: 4519.0, gate: 1.0, pan: 0.5, out: 0.0
                1408 default
                    amplitude: 0.5, frequency: 4508.0, gate: 1.0, pan: 0.5, out: 0.0
                1407 default
                    amplitude: 0.5, frequency: 4497.0, gate: 1.0, pan: 0.5, out: 0.0
                1406 default
                    amplitude: 0.5, frequency: 4486.0, gate: 1.0, pan: 0.5, out: 0.0
                1405 default
                    amplitude: 0.5, frequency: 4475.0, gate: 1.0, pan: 0.5, out: 0.0
                1404 default
                    amplitude: 0.5, frequency: 4464.0, gate: 1.0, pan: 0.5, out: 0.0
                1403 default
                    amplitude: 0.5, frequency: 4453.0, gate: 1.0, pan: 0.5, out: 0.0
                1402 default
                    amplitude: 0.5, frequency: 4442.0, gate: 1.0, pan: 0.5, out: 0.0
                1401 default
                    amplitude: 0.5, frequency: 4431.0, gate: 1.0, pan: 0.5, out: 0.0
                1400 default
                    amplitude: 0.5, frequency: 4420.0, gate: 1.0, pan: 0.5, out: 0.0
                1399 default
                    amplitude: 0.5, frequency: 4409.0, gate: 1.0, pan: 0.5, out: 0.0
                1398 default
                    amplitude: 0.5, frequency: 4398.0, gate: 1.0, pan: 0.5, out: 0.0
                1397 default
                    amplitude: 0.5, frequency: 4387.0, gate: 1.0, pan: 0.5, out: 0.0
                1396 default
                    amplitude: 0.5, frequency: 4376.0, gate: 1.0, pan: 0.5, out: 0.0
                1395 default
                    amplitude: 0.5, frequency: 4365.0, gate: 1.0, pan: 0.5, out: 0.0
                1394 default
                    amplitude: 0.5, frequency: 4354.0, gate: 1.0, pan: 0.5, out: 0.0
                1393 default
                    amplitude: 0.5, frequency: 4343.0, gate: 1.0, pan: 0.5, out: 0.0
                1392 default
                    amplitude: 0.5, frequency: 4332.0, gate: 1.0, pan: 0.5, out: 0.0
                1391 default
                    amplitude: 0.5, frequency: 4321.0, gate: 1.0, pan: 0.5, out: 0.0
                1390 default
                    amplitude: 0.5, frequency: 4310.0, gate: 1.0, pan: 0.5, out: 0.0
                1389 default
                    amplitude: 0.5, frequency: 4299.0, gate: 1.0, pan: 0.5, out: 0.0
                1388 default
                    amplitude: 0.5, frequency: 4288.0, gate: 1.0, pan: 0.5, out: 0.0
                1387 default
                    amplitude: 0.5, frequency: 4277.0, gate: 1.0, pan: 0.5, out: 0.0
                1386 default
                    amplitude: 0.5, frequency: 4266.0, gate: 1.0, pan: 0.5, out: 0.0
                1385 default
                    amplitude: 0.5, frequency: 4255.0, gate: 1.0, pan: 0.5, out: 0.0
                1384 default
                    amplitude: 0.5, frequency: 4244.0, gate: 1.0, pan: 0.5, out: 0.0
                1383 default
                    amplitude: 0.5, frequency: 4233.0, gate: 1.0, pan: 0.5, out: 0.0
                1382 default
                    amplitude: 0.5, frequency: 4222.0, gate: 1.0, pan: 0.5, out: 0.0
                1381 default
                    amplitude: 0.5, frequency: 4211.0, gate: 1.0, pan: 0.5, out: 0.0
                1380 default
                    amplitude: 0.5, frequency: 4200.0, gate: 1.0, pan: 0.5, out: 0.0
                1379 default
                    amplitude: 0.5, frequency: 4189.0, gate: 1.0, pan: 0.5, out: 0.0
                1378 default
                    amplitude: 0.5, frequency: 4178.0, gate: 1.0, pan: 0.5, out: 0.0
                1377 default
                    amplitude: 0.5, frequency: 4167.0, gate: 1.0, pan: 0.5, out: 0.0
                1376 default
                    amplitude: 0.5, frequency: 4156.0, gate: 1.0, pan: 0.5, out: 0.0
                1375 default
                    amplitude: 0.5, frequency: 4145.0, gate: 1.0, pan: 0.5, out: 0.0
                1374 default
                    amplitude: 0.5, frequency: 4134.0, gate: 1.0, pan: 0.5, out: 0.0
                1373 default
                    amplitude: 0.5, frequency: 4123.0, gate: 1.0, pan: 0.5, out: 0.0
                1372 default
                    amplitude: 0.5, frequency: 4112.0, gate: 1.0, pan: 0.5, out: 0.0
                1371 default
                    amplitude: 0.5, frequency: 4101.0, gate: 1.0, pan: 0.5, out: 0.0
                1370 default
                    amplitude: 0.5, frequency: 4090.0, gate: 1.0, pan: 0.5, out: 0.0
                1369 default
                    amplitude: 0.5, frequency: 4079.0, gate: 1.0, pan: 0.5, out: 0.0
                1368 default
                    amplitude: 0.5, frequency: 4068.0, gate: 1.0, pan: 0.5, out: 0.0
                1367 default
                    amplitude: 0.5, frequency: 4057.0, gate: 1.0, pan: 0.5, out: 0.0
                1366 default
                    amplitude: 0.5, frequency: 4046.0, gate: 1.0, pan: 0.5, out: 0.0
                1365 default
                    amplitude: 0.5, frequency: 4035.0, gate: 1.0, pan: 0.5, out: 0.0
                1364 default
                    amplitude: 0.5, frequency: 4024.0, gate: 1.0, pan: 0.5, out: 0.0
                1363 default
                    amplitude: 0.5, frequency: 4013.0, gate: 1.0, pan: 0.5, out: 0.0
                1362 default
                    amplitude: 0.5, frequency: 4002.0, gate: 1.0, pan: 0.5, out: 0.0
                1361 default
                    amplitude: 0.5, frequency: 3991.0, gate: 1.0, pan: 0.5, out: 0.0
                1360 default
                    amplitude: 0.5, frequency: 3980.0, gate: 1.0, pan: 0.5, out: 0.0
                1359 default
                    amplitude: 0.5, frequency: 3969.0, gate: 1.0, pan: 0.5, out: 0.0
                1358 default
                    amplitude: 0.5, frequency: 3958.0, gate: 1.0, pan: 0.5, out: 0.0
                1357 default
                    amplitude: 0.5, frequency: 3947.0, gate: 1.0, pan: 0.5, out: 0.0
                1356 default
                    amplitude: 0.5, frequency: 3936.0, gate: 1.0, pan: 0.5, out: 0.0
                1355 default
                    amplitude: 0.5, frequency: 3925.0, gate: 1.0, pan: 0.5, out: 0.0
                1354 default
                    amplitude: 0.5, frequency: 3914.0, gate: 1.0, pan: 0.5, out: 0.0
                1353 default
                    amplitude: 0.5, frequency: 3903.0, gate: 1.0, pan: 0.5, out: 0.0
                1352 default
                    amplitude: 0.5, frequency: 3892.0, gate: 1.0, pan: 0.5, out: 0.0
                1351 default
                    amplitude: 0.5, frequency: 3881.0, gate: 1.0, pan: 0.5, out: 0.0
                1350 default
                    amplitude: 0.5, frequency: 3870.0, gate: 1.0, pan: 0.5, out: 0.0
                1349 default
                    amplitude: 0.5, frequency: 3859.0, gate: 1.0, pan: 0.5, out: 0.0
                1348 default
                    amplitude: 0.5, frequency: 3848.0, gate: 1.0, pan: 0.5, out: 0.0
                1347 default
                    amplitude: 0.5, frequency: 3837.0, gate: 1.0, pan: 0.5, out: 0.0
                1346 default
                    amplitude: 0.5, frequency: 3826.0, gate: 1.0, pan: 0.5, out: 0.0
                1345 default
                    amplitude: 0.5, frequency: 3815.0, gate: 1.0, pan: 0.5, out: 0.0
                1344 default
                    amplitude: 0.5, frequency: 3804.0, gate: 1.0, pan: 0.5, out: 0.0
                1343 default
                    amplitude: 0.5, frequency: 3793.0, gate: 1.0, pan: 0.5, out: 0.0
                1342 default
                    amplitude: 0.5, frequency: 3782.0, gate: 1.0, pan: 0.5, out: 0.0
                1341 default
                    amplitude: 0.5, frequency: 3771.0, gate: 1.0, pan: 0.5, out: 0.0
                1340 default
                    amplitude: 0.5, frequency: 3760.0, gate: 1.0, pan: 0.5, out: 0.0
                1339 default
                    amplitude: 0.5, frequency: 3749.0, gate: 1.0, pan: 0.5, out: 0.0
                1338 default
                    amplitude: 0.5, frequency: 3738.0, gate: 1.0, pan: 0.5, out: 0.0
                1337 default
                    amplitude: 0.5, frequency: 3727.0, gate: 1.0, pan: 0.5, out: 0.0
                1336 default
                    amplitude: 0.5, frequency: 3716.0, gate: 1.0, pan: 0.5, out: 0.0
                1335 default
                    amplitude: 0.5, frequency: 3705.0, gate: 1.0, pan: 0.5, out: 0.0
                1334 default
                    amplitude: 0.5, frequency: 3694.0, gate: 1.0, pan: 0.5, out: 0.0
                1333 default
                    amplitude: 0.5, frequency: 3683.0, gate: 1.0, pan: 0.5, out: 0.0
                1332 default
                    amplitude: 0.5, frequency: 3672.0, gate: 1.0, pan: 0.5, out: 0.0
                1331 default
                    amplitude: 0.5, frequency: 3661.0, gate: 1.0, pan: 0.5, out: 0.0
                1330 default
                    amplitude: 0.5, frequency: 3650.0, gate: 1.0, pan: 0.5, out: 0.0
                1329 default
                    amplitude: 0.5, frequency: 3639.0, gate: 1.0, pan: 0.5, out: 0.0
                1328 default
                    amplitude: 0.5, frequency: 3628.0, gate: 1.0, pan: 0.5, out: 0.0
                1327 default
                    amplitude: 0.5, frequency: 3617.0, gate: 1.0, pan: 0.5, out: 0.0
                1326 default
                    amplitude: 0.5, frequency: 3606.0, gate: 1.0, pan: 0.5, out: 0.0
                1325 default
                    amplitude: 0.5, frequency: 3595.0, gate: 1.0, pan: 0.5, out: 0.0
                1324 default
                    amplitude: 0.5, frequency: 3584.0, gate: 1.0, pan: 0.5, out: 0.0
                1323 default
                    amplitude: 0.5, frequency: 3573.0, gate: 1.0, pan: 0.5, out: 0.0
                1322 default
                    amplitude: 0.5, frequency: 3562.0, gate: 1.0, pan: 0.5, out: 0.0
                1321 default
                    amplitude: 0.5, frequency: 3551.0, gate: 1.0, pan: 0.5, out: 0.0
                1320 default
                    amplitude: 0.5, frequency: 3540.0, gate: 1.0, pan: 0.5, out: 0.0
                1319 default
                    amplitude: 0.5, frequency: 3529.0, gate: 1.0, pan: 0.5, out: 0.0
                1318 default
                    amplitude: 0.5, frequency: 3518.0, gate: 1.0, pan: 0.5, out: 0.0
                1317 default
                    amplitude: 0.5, frequency: 3507.0, gate: 1.0, pan: 0.5, out: 0.0
                1316 default
                    amplitude: 0.5, frequency: 3496.0, gate: 1.0, pan: 0.5, out: 0.0
                1315 default
                    amplitude: 0.5, frequency: 3485.0, gate: 1.0, pan: 0.5, out: 0.0
                1314 default
                    amplitude: 0.5, frequency: 3474.0, gate: 1.0, pan: 0.5, out: 0.0
                1313 default
                    amplitude: 0.5, frequency: 3463.0, gate: 1.0, pan: 0.5, out: 0.0
                1312 default
                    amplitude: 0.5, frequency: 3452.0, gate: 1.0, pan: 0.5, out: 0.0
                1311 default
                    amplitude: 0.5, frequency: 3441.0, gate: 1.0, pan: 0.5, out: 0.0
                1310 default
                    amplitude: 0.5, frequency: 3430.0, gate: 1.0, pan: 0.5, out: 0.0
                1309 default
                    amplitude: 0.5, frequency: 3419.0, gate: 1.0, pan: 0.5, out: 0.0
                1308 default
                    amplitude: 0.5, frequency: 3408.0, gate: 1.0, pan: 0.5, out: 0.0
                1307 default
                    amplitude: 0.5, frequency: 3397.0, gate: 1.0, pan: 0.5, out: 0.0
                1306 default
                    amplitude: 0.5, frequency: 3386.0, gate: 1.0, pan: 0.5, out: 0.0
                1305 default
                    amplitude: 0.5, frequency: 3375.0, gate: 1.0, pan: 0.5, out: 0.0
                1304 default
                    amplitude: 0.5, frequency: 3364.0, gate: 1.0, pan: 0.5, out: 0.0
                1303 default
                    amplitude: 0.5, frequency: 3353.0, gate: 1.0, pan: 0.5, out: 0.0
                1302 default
                    amplitude: 0.5, frequency: 3342.0, gate: 1.0, pan: 0.5, out: 0.0
                1301 default
                    amplitude: 0.5, frequency: 3331.0, gate: 1.0, pan: 0.5, out: 0.0
                1300 default
                    amplitude: 0.5, frequency: 3320.0, gate: 1.0, pan: 0.5, out: 0.0
                1299 default
                    amplitude: 0.5, frequency: 3309.0, gate: 1.0, pan: 0.5, out: 0.0
                1298 default
                    amplitude: 0.5, frequency: 3298.0, gate: 1.0, pan: 0.5, out: 0.0
                1297 default
                    amplitude: 0.5, frequency: 3287.0, gate: 1.0, pan: 0.5, out: 0.0
                1296 default
                    amplitude: 0.5, frequency: 3276.0, gate: 1.0, pan: 0.5, out: 0.0
                1295 default
                    amplitude: 0.5, frequency: 3265.0, gate: 1.0, pan: 0.5, out: 0.0
                1294 default
                    amplitude: 0.5, frequency: 3254.0, gate: 1.0, pan: 0.5, out: 0.0
                1293 default
                    amplitude: 0.5, frequency: 3243.0, gate: 1.0, pan: 0.5, out: 0.0
                1292 default
                    amplitude: 0.5, frequency: 3232.0, gate: 1.0, pan: 0.5, out: 0.0
                1291 default
                    amplitude: 0.5, frequency: 3221.0, gate: 1.0, pan: 0.5, out: 0.0
                1290 default
                    amplitude: 0.5, frequency: 3210.0, gate: 1.0, pan: 0.5, out: 0.0
                1289 default
                    amplitude: 0.5, frequency: 3199.0, gate: 1.0, pan: 0.5, out: 0.0
                1288 default
                    amplitude: 0.5, frequency: 3188.0, gate: 1.0, pan: 0.5, out: 0.0
                1287 default
                    amplitude: 0.5, frequency: 3177.0, gate: 1.0, pan: 0.5, out: 0.0
                1286 default
                    amplitude: 0.5, frequency: 3166.0, gate: 1.0, pan: 0.5, out: 0.0
                1285 default
                    amplitude: 0.5, frequency: 3155.0, gate: 1.0, pan: 0.5, out: 0.0
                1284 default
                    amplitude: 0.5, frequency: 3144.0, gate: 1.0, pan: 0.5, out: 0.0
                1283 default
                    amplitude: 0.5, frequency: 3133.0, gate: 1.0, pan: 0.5, out: 0.0
                1282 default
                    amplitude: 0.5, frequency: 3122.0, gate: 1.0, pan: 0.5, out: 0.0
                1281 default
                    amplitude: 0.5, frequency: 3111.0, gate: 1.0, pan: 0.5, out: 0.0
                1280 default
                    amplitude: 0.5, frequency: 3100.0, gate: 1.0, pan: 0.5, out: 0.0
                1279 default
                    amplitude: 0.5, frequency: 3089.0, gate: 1.0, pan: 0.5, out: 0.0
                1278 default
                    amplitude: 0.5, frequency: 3078.0, gate: 1.0, pan: 0.5, out: 0.0
                1277 default
                    amplitude: 0.5, frequency: 3067.0, gate: 1.0, pan: 0.5, out: 0.0
                1276 default
                    amplitude: 0.5, frequency: 3056.0, gate: 1.0, pan: 0.5, out: 0.0
                1275 default
                    amplitude: 0.5, frequency: 3045.0, gate: 1.0, pan: 0.5, out: 0.0
                1274 default
                    amplitude: 0.5, frequency: 3034.0, gate: 1.0, pan: 0.5, out: 0.0
                1273 default
                    amplitude: 0.5, frequency: 3023.0, gate: 1.0, pan: 0.5, out: 0.0
                1272 default
                    amplitude: 0.5, frequency: 3012.0, gate: 1.0, pan: 0.5, out: 0.0
                1271 default
                    amplitude: 0.5, frequency: 3001.0, gate: 1.0, pan: 0.5, out: 0.0
                1270 default
                    amplitude: 0.5, frequency: 2990.0, gate: 1.0, pan: 0.5, out: 0.0
                1269 default
                    amplitude: 0.5, frequency: 2979.0, gate: 1.0, pan: 0.5, out: 0.0
                1268 default
                    amplitude: 0.5, frequency: 2968.0, gate: 1.0, pan: 0.5, out: 0.0
                1267 default
                    amplitude: 0.5, frequency: 2957.0, gate: 1.0, pan: 0.5, out: 0.0
                1266 default
                    amplitude: 0.5, frequency: 2946.0, gate: 1.0, pan: 0.5, out: 0.0
                1265 default
                    amplitude: 0.5, frequency: 2935.0, gate: 1.0, pan: 0.5, out: 0.0
                1264 default
                    amplitude: 0.5, frequency: 2924.0, gate: 1.0, pan: 0.5, out: 0.0
                1263 default
                    amplitude: 0.5, frequency: 2913.0, gate: 1.0, pan: 0.5, out: 0.0
                1262 default
                    amplitude: 0.5, frequency: 2902.0, gate: 1.0, pan: 0.5, out: 0.0
                1261 default
                    amplitude: 0.5, frequency: 2891.0, gate: 1.0, pan: 0.5, out: 0.0
                1260 default
                    amplitude: 0.5, frequency: 2880.0, gate: 1.0, pan: 0.5, out: 0.0
                1259 default
                    amplitude: 0.5, frequency: 2869.0, gate: 1.0, pan: 0.5, out: 0.0
                1258 default
                    amplitude: 0.5, frequency: 2858.0, gate: 1.0, pan: 0.5, out: 0.0
                1257 default
                    amplitude: 0.5, frequency: 2847.0, gate: 1.0, pan: 0.5, out: 0.0
                1256 default
                    amplitude: 0.5, frequency: 2836.0, gate: 1.0, pan: 0.5, out: 0.0
                1255 default
                    amplitude: 0.5, frequency: 2825.0, gate: 1.0, pan: 0.5, out: 0.0
                1254 default
                    amplitude: 0.5, frequency: 2814.0, gate: 1.0, pan: 0.5, out: 0.0
                1253 default
                    amplitude: 0.5, frequency: 2803.0, gate: 1.0, pan: 0.5, out: 0.0
                1252 default
                    amplitude: 0.5, frequency: 2792.0, gate: 1.0, pan: 0.5, out: 0.0
                1251 default
                    amplitude: 0.5, frequency: 2781.0, gate: 1.0, pan: 0.5, out: 0.0
                1250 default
                    amplitude: 0.5, frequency: 2770.0, gate: 1.0, pan: 0.5, out: 0.0
                1249 default
                    amplitude: 0.5, frequency: 2759.0, gate: 1.0, pan: 0.5, out: 0.0
                1248 default
                    amplitude: 0.5, frequency: 2748.0, gate: 1.0, pan: 0.5, out: 0.0
                1247 default
                    amplitude: 0.5, frequency: 2737.0, gate: 1.0, pan: 0.5, out: 0.0
                1246 default
                    amplitude: 0.5, frequency: 2726.0, gate: 1.0, pan: 0.5, out: 0.0
                1245 default
                    amplitude: 0.5, frequency: 2715.0, gate: 1.0, pan: 0.5, out: 0.0
                1244 default
                    amplitude: 0.5, frequency: 2704.0, gate: 1.0, pan: 0.5, out: 0.0
                1243 default
                    amplitude: 0.5, frequency: 2693.0, gate: 1.0, pan: 0.5, out: 0.0
                1242 default
                    amplitude: 0.5, frequency: 2682.0, gate: 1.0, pan: 0.5, out: 0.0
                1241 default
                    amplitude: 0.5, frequency: 2671.0, gate: 1.0, pan: 0.5, out: 0.0
                1240 default
                    amplitude: 0.5, frequency: 2660.0, gate: 1.0, pan: 0.5, out: 0.0
                1239 default
                    amplitude: 0.5, frequency: 2649.0, gate: 1.0, pan: 0.5, out: 0.0
                1238 default
                    amplitude: 0.5, frequency: 2638.0, gate: 1.0, pan: 0.5, out: 0.0
                1237 default
                    amplitude: 0.5, frequency: 2627.0, gate: 1.0, pan: 0.5, out: 0.0
                1236 default
                    amplitude: 0.5, frequency: 2616.0, gate: 1.0, pan: 0.5, out: 0.0
                1235 default
                    amplitude: 0.5, frequency: 2605.0, gate: 1.0, pan: 0.5, out: 0.0
                1234 default
                    amplitude: 0.5, frequency: 2594.0, gate: 1.0, pan: 0.5, out: 0.0
                1233 default
                    amplitude: 0.5, frequency: 2583.0, gate: 1.0, pan: 0.5, out: 0.0
                1232 default
                    amplitude: 0.5, frequency: 2572.0, gate: 1.0, pan: 0.5, out: 0.0
                1231 default
                    amplitude: 0.5, frequency: 2561.0, gate: 1.0, pan: 0.5, out: 0.0
                1230 default
                    amplitude: 0.5, frequency: 2550.0, gate: 1.0, pan: 0.5, out: 0.0
                1229 default
                    amplitude: 0.5, frequency: 2539.0, gate: 1.0, pan: 0.5, out: 0.0
                1228 default
                    amplitude: 0.5, frequency: 2528.0, gate: 1.0, pan: 0.5, out: 0.0
                1227 default
                    amplitude: 0.5, frequency: 2517.0, gate: 1.0, pan: 0.5, out: 0.0
                1226 default
                    amplitude: 0.5, frequency: 2506.0, gate: 1.0, pan: 0.5, out: 0.0
                1225 default
                    amplitude: 0.5, frequency: 2495.0, gate: 1.0, pan: 0.5, out: 0.0
                1224 default
                    amplitude: 0.5, frequency: 2484.0, gate: 1.0, pan: 0.5, out: 0.0
                1223 default
                    amplitude: 0.5, frequency: 2473.0, gate: 1.0, pan: 0.5, out: 0.0
                1222 default
                    amplitude: 0.5, frequency: 2462.0, gate: 1.0, pan: 0.5, out: 0.0
                1221 default
                    amplitude: 0.5, frequency: 2451.0, gate: 1.0, pan: 0.5, out: 0.0
                1220 default
                    amplitude: 0.5, frequency: 2440.0, gate: 1.0, pan: 0.5, out: 0.0
                1219 default
                    amplitude: 0.5, frequency: 2429.0, gate: 1.0, pan: 0.5, out: 0.0
                1218 default
                    amplitude: 0.5, frequency: 2418.0, gate: 1.0, pan: 0.5, out: 0.0
                1217 default
                    amplitude: 0.5, frequency: 2407.0, gate: 1.0, pan: 0.5, out: 0.0
                1216 default
                    amplitude: 0.5, frequency: 2396.0, gate: 1.0, pan: 0.5, out: 0.0
                1215 default
                    amplitude: 0.5, frequency: 2385.0, gate: 1.0, pan: 0.5, out: 0.0
                1214 default
                    amplitude: 0.5, frequency: 2374.0, gate: 1.0, pan: 0.5, out: 0.0
                1213 default
                    amplitude: 0.5, frequency: 2363.0, gate: 1.0, pan: 0.5, out: 0.0
                1212 default
                    amplitude: 0.5, frequency: 2352.0, gate: 1.0, pan: 0.5, out: 0.0
                1211 default
                    amplitude: 0.5, frequency: 2341.0, gate: 1.0, pan: 0.5, out: 0.0
                1210 default
                    amplitude: 0.5, frequency: 2330.0, gate: 1.0, pan: 0.5, out: 0.0
                1209 default
                    amplitude: 0.5, frequency: 2319.0, gate: 1.0, pan: 0.5, out: 0.0
                1208 default
                    amplitude: 0.5, frequency: 2308.0, gate: 1.0, pan: 0.5, out: 0.0
                1207 default
                    amplitude: 0.5, frequency: 2297.0, gate: 1.0, pan: 0.5, out: 0.0
                1206 default
                    amplitude: 0.5, frequency: 2286.0, gate: 1.0, pan: 0.5, out: 0.0
                1205 default
                    amplitude: 0.5, frequency: 2275.0, gate: 1.0, pan: 0.5, out: 0.0
                1204 default
                    amplitude: 0.5, frequency: 2264.0, gate: 1.0, pan: 0.5, out: 0.0
                1203 default
                    amplitude: 0.5, frequency: 2253.0, gate: 1.0, pan: 0.5, out: 0.0
                1202 default
                    amplitude: 0.5, frequency: 2242.0, gate: 1.0, pan: 0.5, out: 0.0
                1201 default
                    amplitude: 0.5, frequency: 2231.0, gate: 1.0, pan: 0.5, out: 0.0
                1200 default
                    amplitude: 0.5, frequency: 2220.0, gate: 1.0, pan: 0.5, out: 0.0
                1199 default
                    amplitude: 0.5, frequency: 2209.0, gate: 1.0, pan: 0.5, out: 0.0
                1198 default
                    amplitude: 0.5, frequency: 2198.0, gate: 1.0, pan: 0.5, out: 0.0
                1197 default
                    amplitude: 0.5, frequency: 2187.0, gate: 1.0, pan: 0.5, out: 0.0
                1196 default
                    amplitude: 0.5, frequency: 2176.0, gate: 1.0, pan: 0.5, out: 0.0
                1195 default
                    amplitude: 0.5, frequency: 2165.0, gate: 1.0, pan: 0.5, out: 0.0
                1194 default
                    amplitude: 0.5, frequency: 2154.0, gate: 1.0, pan: 0.5, out: 0.0
                1193 default
                    amplitude: 0.5, frequency: 2143.0, gate: 1.0, pan: 0.5, out: 0.0
                1192 default
                    amplitude: 0.5, frequency: 2132.0, gate: 1.0, pan: 0.5, out: 0.0
                1191 default
                    amplitude: 0.5, frequency: 2121.0, gate: 1.0, pan: 0.5, out: 0.0
                1190 default
                    amplitude: 0.5, frequency: 2110.0, gate: 1.0, pan: 0.5, out: 0.0
                1189 default
                    amplitude: 0.5, frequency: 2099.0, gate: 1.0, pan: 0.5, out: 0.0
                1188 default
                    amplitude: 0.5, frequency: 2088.0, gate: 1.0, pan: 0.5, out: 0.0
                1187 default
                    amplitude: 0.5, frequency: 2077.0, gate: 1.0, pan: 0.5, out: 0.0
                1186 default
                    amplitude: 0.5, frequency: 2066.0, gate: 1.0, pan: 0.5, out: 0.0
                1185 default
                    amplitude: 0.5, frequency: 2055.0, gate: 1.0, pan: 0.5, out: 0.0
                1184 default
                    amplitude: 0.5, frequency: 2044.0, gate: 1.0, pan: 0.5, out: 0.0
                1183 default
                    amplitude: 0.5, frequency: 2033.0, gate: 1.0, pan: 0.5, out: 0.0
                1182 default
                    amplitude: 0.5, frequency: 2022.0, gate: 1.0, pan: 0.5, out: 0.0
                1181 default
                    amplitude: 0.5, frequency: 2011.0, gate: 1.0, pan: 0.5, out: 0.0
                1180 default
                    amplitude: 0.5, frequency: 2000.0, gate: 1.0, pan: 0.5, out: 0.0
                1179 default
                    amplitude: 0.5, frequency: 1989.0, gate: 1.0, pan: 0.5, out: 0.0
                1178 default
                    amplitude: 0.5, frequency: 1978.0, gate: 1.0, pan: 0.5, out: 0.0
                1177 default
                    amplitude: 0.5, frequency: 1967.0, gate: 1.0, pan: 0.5, out: 0.0
                1176 default
                    amplitude: 0.5, frequency: 1956.0, gate: 1.0, pan: 0.5, out: 0.0
                1175 default
                    amplitude: 0.5, frequency: 1945.0, gate: 1.0, pan: 0.5, out: 0.0
                1174 default
                    amplitude: 0.5, frequency: 1934.0, gate: 1.0, pan: 0.5, out: 0.0
                1173 default
                    amplitude: 0.5, frequency: 1923.0, gate: 1.0, pan: 0.5, out: 0.0
                1172 default
                    amplitude: 0.5, frequency: 1912.0, gate: 1.0, pan: 0.5, out: 0.0
                1171 default
                    amplitude: 0.5, frequency: 1901.0, gate: 1.0, pan: 0.5, out: 0.0
                1170 default
                    amplitude: 0.5, frequency: 1890.0, gate: 1.0, pan: 0.5, out: 0.0
                1169 default
                    amplitude: 0.5, frequency: 1879.0, gate: 1.0, pan: 0.5, out: 0.0
                1168 default
                    amplitude: 0.5, frequency: 1868.0, gate: 1.0, pan: 0.5, out: 0.0
                1167 default
                    amplitude: 0.5, frequency: 1857.0, gate: 1.0, pan: 0.5, out: 0.0
                1166 default
                    amplitude: 0.5, frequency: 1846.0, gate: 1.0, pan: 0.5, out: 0.0
                1165 default
                    amplitude: 0.5, frequency: 1835.0, gate: 1.0, pan: 0.5, out: 0.0
                1164 default
                    amplitude: 0.5, frequency: 1824.0, gate: 1.0, pan: 0.5, out: 0.0
                1163 default
                    amplitude: 0.5, frequency: 1813.0, gate: 1.0, pan: 0.5, out: 0.0
                1162 default
                    amplitude: 0.5, frequency: 1802.0, gate: 1.0, pan: 0.5, out: 0.0
                1161 default
                    amplitude: 0.5, frequency: 1791.0, gate: 1.0, pan: 0.5, out: 0.0
                1160 default
                    amplitude: 0.5, frequency: 1780.0, gate: 1.0, pan: 0.5, out: 0.0
                1159 default
                    amplitude: 0.5, frequency: 1769.0, gate: 1.0, pan: 0.5, out: 0.0
                1158 default
                    amplitude: 0.5, frequency: 1758.0, gate: 1.0, pan: 0.5, out: 0.0
                1157 default
                    amplitude: 0.5, frequency: 1747.0, gate: 1.0, pan: 0.5, out: 0.0
                1156 default
                    amplitude: 0.5, frequency: 1736.0, gate: 1.0, pan: 0.5, out: 0.0
                1155 default
                    amplitude: 0.5, frequency: 1725.0, gate: 1.0, pan: 0.5, out: 0.0
                1154 default
                    amplitude: 0.5, frequency: 1714.0, gate: 1.0, pan: 0.5, out: 0.0
                1153 default
                    amplitude: 0.5, frequency: 1703.0, gate: 1.0, pan: 0.5, out: 0.0
                1152 default
                    amplitude: 0.5, frequency: 1692.0, gate: 1.0, pan: 0.5, out: 0.0
                1151 default
                    amplitude: 0.5, frequency: 1681.0, gate: 1.0, pan: 0.5, out: 0.0
                1150 default
                    amplitude: 0.5, frequency: 1670.0, gate: 1.0, pan: 0.5, out: 0.0
                1149 default
                    amplitude: 0.5, frequency: 1659.0, gate: 1.0, pan: 0.5, out: 0.0
                1148 default
                    amplitude: 0.5, frequency: 1648.0, gate: 1.0, pan: 0.5, out: 0.0
                1147 default
                    amplitude: 0.5, frequency: 1637.0, gate: 1.0, pan: 0.5, out: 0.0
                1146 default
                    amplitude: 0.5, frequency: 1626.0, gate: 1.0, pan: 0.5, out: 0.0
                1145 default
                    amplitude: 0.5, frequency: 1615.0, gate: 1.0, pan: 0.5, out: 0.0
                1144 default
                    amplitude: 0.5, frequency: 1604.0, gate: 1.0, pan: 0.5, out: 0.0
                1143 default
                    amplitude: 0.5, frequency: 1593.0, gate: 1.0, pan: 0.5, out: 0.0
                1142 default
                    amplitude: 0.5, frequency: 1582.0, gate: 1.0, pan: 0.5, out: 0.0
                1141 default
                    amplitude: 0.5, frequency: 1571.0, gate: 1.0, pan: 0.5, out: 0.0
                1140 default
                    amplitude: 0.5, frequency: 1560.0, gate: 1.0, pan: 0.5, out: 0.0
                1139 default
                    amplitude: 0.5, frequency: 1549.0, gate: 1.0, pan: 0.5, out: 0.0
                1138 default
                    amplitude: 0.5, frequency: 1538.0, gate: 1.0, pan: 0.5, out: 0.0
                1137 default
                    amplitude: 0.5, frequency: 1527.0, gate: 1.0, pan: 0.5, out: 0.0
                1136 default
                    amplitude: 0.5, frequency: 1516.0, gate: 1.0, pan: 0.5, out: 0.0
                1135 default
                    amplitude: 0.5, frequency: 1505.0, gate: 1.0, pan: 0.5, out: 0.0
                1134 default
                    amplitude: 0.5, frequency: 1494.0, gate: 1.0, pan: 0.5, out: 0.0
                1133 default
                    amplitude: 0.5, frequency: 1483.0, gate: 1.0, pan: 0.5, out: 0.0
                1132 default
                    amplitude: 0.5, frequency: 1472.0, gate: 1.0, pan: 0.5, out: 0.0
                1131 default
                    amplitude: 0.5, frequency: 1461.0, gate: 1.0, pan: 0.5, out: 0.0
                1130 default
                    amplitude: 0.5, frequency: 1450.0, gate: 1.0, pan: 0.5, out: 0.0
                1129 default
                    amplitude: 0.5, frequency: 1439.0, gate: 1.0, pan: 0.5, out: 0.0
                1128 default
                    amplitude: 0.5, frequency: 1428.0, gate: 1.0, pan: 0.5, out: 0.0
                1127 default
                    amplitude: 0.5, frequency: 1417.0, gate: 1.0, pan: 0.5, out: 0.0
                1126 default
                    amplitude: 0.5, frequency: 1406.0, gate: 1.0, pan: 0.5, out: 0.0
                1125 default
                    amplitude: 0.5, frequency: 1395.0, gate: 1.0, pan: 0.5, out: 0.0
                1124 default
                    amplitude: 0.5, frequency: 1384.0, gate: 1.0, pan: 0.5, out: 0.0
                1123 default
                    amplitude: 0.5, frequency: 1373.0, gate: 1.0, pan: 0.5, out: 0.0
                1122 default
                    amplitude: 0.5, frequency: 1362.0, gate: 1.0, pan: 0.5, out: 0.0
                1121 default
                    amplitude: 0.5, frequency: 1351.0, gate: 1.0, pan: 0.5, out: 0.0
                1120 default
                    amplitude: 0.5, frequency: 1340.0, gate: 1.0, pan: 0.5, out: 0.0
                1119 default
                    amplitude: 0.5, frequency: 1329.0, gate: 1.0, pan: 0.5, out: 0.0
                1118 default
                    amplitude: 0.5, frequency: 1318.0, gate: 1.0, pan: 0.5, out: 0.0
                1117 default
                    amplitude: 0.5, frequency: 1307.0, gate: 1.0, pan: 0.5, out: 0.0
                1116 default
                    amplitude: 0.5, frequency: 1296.0, gate: 1.0, pan: 0.5, out: 0.0
                1115 default
                    amplitude: 0.5, frequency: 1285.0, gate: 1.0, pan: 0.5, out: 0.0
                1114 default
                    amplitude: 0.5, frequency: 1274.0, gate: 1.0, pan: 0.5, out: 0.0
                1113 default
                    amplitude: 0.5, frequency: 1263.0, gate: 1.0, pan: 0.5, out: 0.0
                1112 default
                    amplitude: 0.5, frequency: 1252.0, gate: 1.0, pan: 0.5, out: 0.0
                1111 default
                    amplitude: 0.5, frequency: 1241.0, gate: 1.0, pan: 0.5, out: 0.0
                1110 default
                    amplitude: 0.5, frequency: 1230.0, gate: 1.0, pan: 0.5, out: 0.0
                1109 default
                    amplitude: 0.5, frequency: 1219.0, gate: 1.0, pan: 0.5, out: 0.0
                1108 default
                    amplitude: 0.5, frequency: 1208.0, gate: 1.0, pan: 0.5, out: 0.0
                1107 default
                    amplitude: 0.5, frequency: 1197.0, gate: 1.0, pan: 0.5, out: 0.0
                1106 default
                    amplitude: 0.5, frequency: 1186.0, gate: 1.0, pan: 0.5, out: 0.0
                1105 default
                    amplitude: 0.5, frequency: 1175.0, gate: 1.0, pan: 0.5, out: 0.0
                1104 default
                    amplitude: 0.5, frequency: 1164.0, gate: 1.0, pan: 0.5, out: 0.0
                1103 default
                    amplitude: 0.5, frequency: 1153.0, gate: 1.0, pan: 0.5, out: 0.0
                1102 default
                    amplitude: 0.5, frequency: 1142.0, gate: 1.0, pan: 0.5, out: 0.0
                1101 default
                    amplitude: 0.5, frequency: 1131.0, gate: 1.0, pan: 0.5, out: 0.0
                1100 default
                    amplitude: 0.5, frequency: 1120.0, gate: 1.0, pan: 0.5, out: 0.0
                1099 default
                    amplitude: 0.5, frequency: 1109.0, gate: 1.0, pan: 0.5, out: 0.0
                1098 default
                    amplitude: 0.5, frequency: 1098.0, gate: 1.0, pan: 0.5, out: 0.0
                1097 default
                    amplitude: 0.5, frequency: 1087.0, gate: 1.0, pan: 0.5, out: 0.0
                1096 default
                    amplitude: 0.5, frequency: 1076.0, gate: 1.0, pan: 0.5, out: 0.0
                1095 default
                    amplitude: 0.5, frequency: 1065.0, gate: 1.0, pan: 0.5, out: 0.0
                1094 default
                    amplitude: 0.5, frequency: 1054.0, gate: 1.0, pan: 0.5, out: 0.0
                1093 default
                    amplitude: 0.5, frequency: 1043.0, gate: 1.0, pan: 0.5, out: 0.0
                1092 default
                    amplitude: 0.5, frequency: 1032.0, gate: 1.0, pan: 0.5, out: 0.0
                1091 default
                    amplitude: 0.5, frequency: 1021.0, gate: 1.0, pan: 0.5, out: 0.0
                1090 default
                    amplitude: 0.5, frequency: 1010.0, gate: 1.0, pan: 0.5, out: 0.0
                1089 default
                    amplitude: 0.5, frequency: 999.0, gate: 1.0, pan: 0.5, out: 0.0
                1088 default
                    amplitude: 0.5, frequency: 988.0, gate: 1.0, pan: 0.5, out: 0.0
                1087 default
                    amplitude: 0.5, frequency: 977.0, gate: 1.0, pan: 0.5, out: 0.0
                1086 default
                    amplitude: 0.5, frequency: 966.0, gate: 1.0, pan: 0.5, out: 0.0
                1085 default
                    amplitude: 0.5, frequency: 955.0, gate: 1.0, pan: 0.5, out: 0.0
                1084 default
                    amplitude: 0.5, frequency: 944.0, gate: 1.0, pan: 0.5, out: 0.0
                1083 default
                    amplitude: 0.5, frequency: 933.0, gate: 1.0, pan: 0.5, out: 0.0
                1082 default
                    amplitude: 0.5, frequency: 922.0, gate: 1.0, pan: 0.5, out: 0.0
                1081 default
                    amplitude: 0.5, frequency: 911.0, gate: 1.0, pan: 0.5, out: 0.0
                1080 default
                    amplitude: 0.5, frequency: 900.0, gate: 1.0, pan: 0.5, out: 0.0
                1079 default
                    amplitude: 0.5, frequency: 889.0, gate: 1.0, pan: 0.5, out: 0.0
                1078 default
                    amplitude: 0.5, frequency: 878.0, gate: 1.0, pan: 0.5, out: 0.0
                1077 default
                    amplitude: 0.5, frequency: 867.0, gate: 1.0, pan: 0.5, out: 0.0
                1076 default
                    amplitude: 0.5, frequency: 856.0, gate: 1.0, pan: 0.5, out: 0.0
                1075 default
                    amplitude: 0.5, frequency: 845.0, gate: 1.0, pan: 0.5, out: 0.0
                1074 default
                    amplitude: 0.5, frequency: 834.0, gate: 1.0, pan: 0.5, out: 0.0
                1073 default
                    amplitude: 0.5, frequency: 823.0, gate: 1.0, pan: 0.5, out: 0.0
                1072 default
                    amplitude: 0.5, frequency: 812.0, gate: 1.0, pan: 0.5, out: 0.0
                1071 default
                    amplitude: 0.5, frequency: 801.0, gate: 1.0, pan: 0.5, out: 0.0
                1070 default
                    amplitude: 0.5, frequency: 790.0, gate: 1.0, pan: 0.5, out: 0.0
                1069 default
                    amplitude: 0.5, frequency: 779.0, gate: 1.0, pan: 0.5, out: 0.0
                1068 default
                    amplitude: 0.5, frequency: 768.0, gate: 1.0, pan: 0.5, out: 0.0
                1067 default
                    amplitude: 0.5, frequency: 757.0, gate: 1.0, pan: 0.5, out: 0.0
                1066 default
                    amplitude: 0.5, frequency: 746.0, gate: 1.0, pan: 0.5, out: 0.0
                1065 default
                    amplitude: 0.5, frequency: 735.0, gate: 1.0, pan: 0.5, out: 0.0
                1064 default
                    amplitude: 0.5, frequency: 724.0, gate: 1.0, pan: 0.5, out: 0.0
                1063 default
                    amplitude: 0.5, frequency: 713.0, gate: 1.0, pan: 0.5, out: 0.0
                1062 default
                    amplitude: 0.5, frequency: 702.0, gate: 1.0, pan: 0.5, out: 0.0
                1061 default
                    amplitude: 0.5, frequency: 691.0, gate: 1.0, pan: 0.5, out: 0.0
                1060 default
                    amplitude: 0.5, frequency: 680.0, gate: 1.0, pan: 0.5, out: 0.0
                1059 default
                    amplitude: 0.5, frequency: 669.0, gate: 1.0, pan: 0.5, out: 0.0
                1058 default
                    amplitude: 0.5, frequency: 658.0, gate: 1.0, pan: 0.5, out: 0.0
                1057 default
                    amplitude: 0.5, frequency: 647.0, gate: 1.0, pan: 0.5, out: 0.0
                1056 default
                    amplitude: 0.5, frequency: 636.0, gate: 1.0, pan: 0.5, out: 0.0
                1055 default
                    amplitude: 0.5, frequency: 625.0, gate: 1.0, pan: 0.5, out: 0.0
                1054 default
                    amplitude: 0.5, frequency: 614.0, gate: 1.0, pan: 0.5, out: 0.0
                1053 default
                    amplitude: 0.5, frequency: 603.0, gate: 1.0, pan: 0.5, out: 0.0
                1052 default
                    amplitude: 0.5, frequency: 592.0, gate: 1.0, pan: 0.5, out: 0.0
                1051 default
                    amplitude: 0.5, frequency: 581.0, gate: 1.0, pan: 0.5, out: 0.0
                1050 default
                    amplitude: 0.5, frequency: 570.0, gate: 1.0, pan: 0.5, out: 0.0
                1049 default
                    amplitude: 0.5, frequency: 559.0, gate: 1.0, pan: 0.5, out: 0.0
                1048 default
                    amplitude: 0.5, frequency: 548.0, gate: 1.0, pan: 0.5, out: 0.0
                1047 default
                    amplitude: 0.5, frequency: 537.0, gate: 1.0, pan: 0.5, out: 0.0
                1046 default
                    amplitude: 0.5, frequency: 526.0, gate: 1.0, pan: 0.5, out: 0.0
                1045 default
                    amplitude: 0.5, frequency: 515.0, gate: 1.0, pan: 0.5, out: 0.0
                1044 default
                    amplitude: 0.5, frequency: 504.0, gate: 1.0, pan: 0.5, out: 0.0
                1043 default
                    amplitude: 0.5, frequency: 493.0, gate: 1.0, pan: 0.5, out: 0.0
                1042 default
                    amplitude: 0.5, frequency: 482.0, gate: 1.0, pan: 0.5, out: 0.0
                1041 default
                    amplitude: 0.5, frequency: 471.0, gate: 1.0, pan: 0.5, out: 0.0
                1040 default
                    amplitude: 0.5, frequency: 460.0, gate: 1.0, pan: 0.5, out: 0.0
                1039 default
                    amplitude: 0.5, frequency: 449.0, gate: 1.0, pan: 0.5, out: 0.0
                1038 default
                    amplitude: 0.5, frequency: 438.0, gate: 1.0, pan: 0.5, out: 0.0
                1037 default
                    amplitude: 0.5, frequency: 427.0, gate: 1.0, pan: 0.5, out: 0.0
                1036 default
                    amplitude: 0.5, frequency: 416.0, gate: 1.0, pan: 0.5, out: 0.0
                1035 default
                    amplitude: 0.5, frequency: 405.0, gate: 1.0, pan: 0.5, out: 0.0
                1034 default
                    amplitude: 0.5, frequency: 394.0, gate: 1.0, pan: 0.5, out: 0.0
                1033 default
                    amplitude: 0.5, frequency: 383.0, gate: 1.0, pan: 0.5, out: 0.0
                1032 default
                    amplitude: 0.5, frequency: 372.0, gate: 1.0, pan: 0.5, out: 0.0
                1031 default
                    amplitude: 0.5, frequency: 361.0, gate: 1.0, pan: 0.5, out: 0.0
                1030 default
                    amplitude: 0.5, frequency: 350.0, gate: 1.0, pan: 0.5, out: 0.0
                1029 default
                    amplitude: 0.5, frequency: 339.0, gate: 1.0, pan: 0.5, out: 0.0
                1028 default
                    amplitude: 0.5, frequency: 328.0, gate: 1.0, pan: 0.5, out: 0.0
                1027 default
                    amplitude: 0.5, frequency: 317.0, gate: 1.0, pan: 0.5, out: 0.0
                1026 default
                    amplitude: 0.5, frequency: 306.0, gate: 1.0, pan: 0.5, out: 0.0
                1025 default
                    amplitude: 0.5, frequency: 295.0, gate: 1.0, pan: 0.5, out: 0.0
                1024 default
                    amplitude: 0.5, frequency: 284.0, gate: 1.0, pan: 0.5, out: 0.0
                1023 default
                    amplitude: 0.5, frequency: 273.0, gate: 1.0, pan: 0.5, out: 0.0
                1022 default
                    amplitude: 0.5, frequency: 262.0, gate: 1.0, pan: 0.5, out: 0.0
                1021 default
                    amplitude: 0.5, frequency: 251.0, gate: 1.0, pan: 0.5, out: 0.0
                1020 default
                    amplitude: 0.5, frequency: 240.0, gate: 1.0, pan: 0.5, out: 0.0
                1019 default
                    amplitude: 0.5, frequency: 229.0, gate: 1.0, pan: 0.5, out: 0.0
                1018 default
                    amplitude: 0.5, frequency: 218.0, gate: 1.0, pan: 0.5, out: 0.0
                1017 default
                    amplitude: 0.5, frequency: 207.0, gate: 1.0, pan: 0.5, out: 0.0
                1016 default
                    amplitude: 0.5, frequency: 196.0, gate: 1.0, pan: 0.5, out: 0.0
                1015 default
                    amplitude: 0.5, frequency: 185.0, gate: 1.0, pan: 0.5, out: 0.0
                1014 default
                    amplitude: 0.5, frequency: 174.0, gate: 1.0, pan: 0.5, out: 0.0
                1013 default
                    amplitude: 0.5, frequency: 163.0, gate: 1.0, pan: 0.5, out: 0.0
                1012 default
                    amplitude: 0.5, frequency: 152.0, gate: 1.0, pan: 0.5, out: 0.0
                1011 default
                    amplitude: 0.5, frequency: 141.0, gate: 1.0, pan: 0.5, out: 0.0
                1010 default
                    amplitude: 0.5, frequency: 130.0, gate: 1.0, pan: 0.5, out: 0.0
                1009 default
                    amplitude: 0.5, frequency: 119.0, gate: 1.0, pan: 0.5, out: 0.0
                1008 default
                    amplitude: 0.5, frequency: 108.0, gate: 1.0, pan: 0.5, out: 0.0
                1007 default
                    amplitude: 0.5, frequency: 97.0, gate: 1.0, pan: 0.5, out: 0.0
                1006 default
                    amplitude: 0.5, frequency: 86.0, gate: 1.0, pan: 0.5, out: 0.0
                1005 default
                    amplitude: 0.5, frequency: 75.0, gate: 1.0, pan: 0.5, out: 0.0
                1004 default
                    amplitude: 0.5, frequency: 64.0, gate: 1.0, pan: 0.5, out: 0.0
                1003 default
                    amplitude: 0.5, frequency: 53.0, gate: 1.0, pan: 0.5, out: 0.0
                1002 default
                    amplitude: 0.5, frequency: 42.0, gate: 1.0, pan: 0.5, out: 0.0
                1001 default
                    amplitude: 0.5, frequency: 31.0, gate: 1.0, pan: 0.5, out: 0.0
                1000 default
                    amplitude: 0.5, frequency: 20.0, gate: 1.0, pan: 0.5, out: 0.0
        """
    )


@pytest.mark.asyncio
async def test_query_status(context):
    assert isinstance(await get(context.query_status()), StatusInfo)
    # unsync
    with context.osc_protocol.capture() as transcript:
        assert await get(context.query_status(sync=False)) is None
    assert transcript.filtered(received=False, status=True) == [OscMessage("/status")]


@pytest.mark.asyncio
async def test_query_tree(context):
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
                    1003 default
                        amplitude: 0.1, frequency: 222.0, gate: 1.0, pan: 0.5, out: 0.0
                    1004 default
                        amplitude: 0.1, frequency: 333.0, gate: 1.0, pan: 0.5, out: 0.0
                    1005 group
                1000 group
                    1002 default
                        amplitude: 0.1, frequency: 111.0, gate: 1.0, pan: 0.5, out: 0.0
        """
    )
    # unsync
    with context.osc_protocol.capture() as transcript:
        assert await get(context.query_tree(sync=False)) is None
    assert transcript.filtered(received=False, status=False) == [
        OscMessage("/g_queryTree", 0, 1)
    ]


@pytest.mark.asyncio
async def test_query_version(context):
    completed_subprocess = subprocess.run(
        [scsynth.find("scsynth"), "-v"], capture_output=True, text=True
    )
    stdout = completed_subprocess.stdout
    line = completed_subprocess.stdout.splitlines()[0]
    print(stdout, line)
    groups = re.match(
        r"(\w+) (\d+)\.(\d+)(\.[\w-]+) \(Built from (?:branch|tag) '([\W\w]+)' \[([\W\w]+)\]\)",
        line,
    ).groups()
    program_name, major, minor, patch, ref, commit = groups
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
async def test_reboot(context):
    # TODO: expand this

    def callback(event: ServerLifecycleEvent) -> None:
        events.append(event)

    events = []
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
            for synthdef in [
                synthdefs.system_link_audio_1,
                synthdefs.system_link_audio_10,
                synthdefs.system_link_audio_11,
                synthdefs.system_link_audio_12,
                synthdefs.system_link_audio_13,
                synthdefs.system_link_audio_14,
                synthdefs.system_link_audio_15,
                synthdefs.system_link_audio_16,
                synthdefs.system_link_audio_2,
                synthdefs.system_link_audio_3,
                synthdefs.system_link_audio_4,
                synthdefs.system_link_audio_5,
                synthdefs.system_link_audio_6,
                synthdefs.system_link_audio_7,
                synthdefs.system_link_audio_8,
                synthdefs.system_link_audio_9,
                synthdefs.system_link_control_1,
                synthdefs.system_link_control_10,
                synthdefs.system_link_control_11,
                synthdefs.system_link_control_12,
                synthdefs.system_link_control_13,
                synthdefs.system_link_control_14,
                synthdefs.system_link_control_15,
                synthdefs.system_link_control_16,
                synthdefs.system_link_control_2,
                synthdefs.system_link_control_3,
                synthdefs.system_link_control_4,
                synthdefs.system_link_control_5,
                synthdefs.system_link_control_6,
                synthdefs.system_link_control_7,
                synthdefs.system_link_control_8,
                synthdefs.system_link_control_9,
            ]
        ),
        OscMessage("/sync", 0),
    ]


@pytest.mark.xfail
@pytest.mark.asyncio
async def test_register_lifecycle_callback(context):
    raise Exception


@pytest.mark.xfail
@pytest.mark.asyncio
async def test_register_osc_callback(context):
    raise Exception


@pytest.mark.asyncio
async def test_reset(context):
    # TODO: expand this
    def callback(event: ServerLifecycleEvent) -> None:
        events.append(event)

    events = []
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
            for synthdef in [
                synthdefs.system_link_audio_1,
                synthdefs.system_link_audio_10,
                synthdefs.system_link_audio_11,
                synthdefs.system_link_audio_12,
                synthdefs.system_link_audio_13,
                synthdefs.system_link_audio_14,
                synthdefs.system_link_audio_15,
                synthdefs.system_link_audio_16,
                synthdefs.system_link_audio_2,
                synthdefs.system_link_audio_3,
                synthdefs.system_link_audio_4,
                synthdefs.system_link_audio_5,
                synthdefs.system_link_audio_6,
                synthdefs.system_link_audio_7,
                synthdefs.system_link_audio_8,
                synthdefs.system_link_audio_9,
                synthdefs.system_link_control_1,
                synthdefs.system_link_control_10,
                synthdefs.system_link_control_11,
                synthdefs.system_link_control_12,
                synthdefs.system_link_control_13,
                synthdefs.system_link_control_14,
                synthdefs.system_link_control_15,
                synthdefs.system_link_control_16,
                synthdefs.system_link_control_2,
                synthdefs.system_link_control_3,
                synthdefs.system_link_control_4,
                synthdefs.system_link_control_5,
                synthdefs.system_link_control_6,
                synthdefs.system_link_control_7,
                synthdefs.system_link_control_8,
                synthdefs.system_link_control_9,
            ]
        ),
        OscMessage("/sync", 0),
    ]


@pytest.mark.asyncio
async def test_root_node(context):
    assert isinstance(context.root_node, Group)
    assert context.root_node.context is context
    assert context.root_node.id_ == 0


@pytest.mark.asyncio
async def test_sync(context):
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


@pytest.mark.xfail
@pytest.mark.asyncio
async def test_unregister_lifecycle_callback(context):
    raise Exception


@pytest.mark.xfail
@pytest.mark.asyncio
async def test_unregister_osc_callback(context):
    raise Exception
