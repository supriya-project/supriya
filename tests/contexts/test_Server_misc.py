import asyncio
import logging
import re
import subprocess

import pytest
import pytest_asyncio
from uqbar.strings import normalize

from supriya import default, scsynth
from supriya.contexts.entities import Group
from supriya.contexts.realtime import AsyncServer, Server
from supriya.contexts.responses import StatusInfo, VersionInfo
from supriya.exceptions import ServerOffline
from supriya.osc import OscMessage


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
                        out: 0.0, amplitude: 0.1, frequency: 222.0, gate: 1.0, pan: 0.5
                    1004 default
                        out: 0.0, amplitude: 0.1, frequency: 333.0, gate: 1.0, pan: 0.5
                    1005 group
                1000 group
                    1002 default
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
async def test_query_version(context):
    completed_subprocess = subprocess.run(
        [scsynth.find("scsynth"), "-v"], capture_output=True, text=True
    )
    stdout = completed_subprocess.stdout
    line = completed_subprocess.stdout.splitlines()[0]
    print(stdout, line)
    (program_name, major, minor, patch, branch, commit) = re.match(
        r"(\w+) (\d+)\.(\d+)(\.[\w-]+) \(Built from branch '([\W\w]+)' \[([\W\w]+)\]\)",
        line,
    ).groups()
    expected_info = VersionInfo(
        program_name=program_name,
        major=int(major),
        minor=int(minor),
        patch=patch,
        branch=branch,
        commit=commit,
    )
    assert await get(context.query_version()) == expected_info
    # unsync
    with context.osc_protocol.capture() as transcript:
        assert await get(context.query_version(sync=False)) is None
    assert transcript.filtered(received=False, status=False) == [OscMessage("/version")]


@pytest.mark.asyncio
async def test_reboot(context):
    await get(context.reboot())


@pytest.mark.asyncio
async def test_reset(context):
    await get(context.reset())


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


@pytest.mark.asyncio
async def test_root_node(context):
    assert isinstance(context.root_node, Group)
    assert context.root_node.context is context
    assert context.root_node.id_ == 0
