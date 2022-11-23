from dataclasses import dataclass
from typing import List, Optional

import hypothesis
import hypothesis.strategies as st
import pytest

import supriya.assets
import supriya.realtime
import supriya.synthdefs
from supriya.osc.messages import OscMessage
from tests.proptest import get_control_test_groups, hp_global_settings


@pytest.fixture(autouse=True)
def shutdown_sync_servers(shutdown_scsynth):
    pass


@pytest.fixture
def server(persistent_server):
    persistent_server.reset()
    persistent_server.add_synthdef(supriya.assets.synthdefs.default)
    yield persistent_server


hp_settings = hypothesis.settings(
    hp_global_settings,
    suppress_health_check=[hypothesis.HealthCheck.function_scoped_fixture],
    deadline=1999,
)


@dataclass
class SampleGroup:
    group: supriya.realtime.Group
    allocate_pattern: List[bool]
    name: Optional[str] = None
    node_id_is_permanent: bool = False
    parallel: bool = False


@st.composite
def st_group_sample(draw) -> SampleGroup:

    parallel = draw(st.booleans())
    group = supriya.realtime.Group(parallel=parallel)
    allocate_pattern = draw(st.lists(st.booleans(), min_size=2, max_size=16))
    sample = SampleGroup(group, parallel=parallel, allocate_pattern=allocate_pattern)

    return sample


@get_control_test_groups(min_size=1, max_size=16)
@st.composite
def st_group(draw) -> SampleGroup:

    name = draw(st.one_of(st.text(), st.none()))
    node_id_is_permanent = draw(st.booleans())
    parallel = draw(st.booleans())
    group = supriya.realtime.Group(name=name, parallel=parallel)
    allocate_pattern = draw(st.lists(st.booleans(), min_size=8, max_size=16))
    sample = SampleGroup(
        group,
        name=name,
        node_id_is_permanent=node_id_is_permanent,
        parallel=parallel,
        allocate_pattern=allocate_pattern,
    )

    return sample


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_group())
def test_allocate_01(server, strategy):

    control, test = strategy

    for sample in control:
        assert not sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server is None
        assert not sample.group.node_id_is_permanent
        assert sample.group.name == sample.name
        assert sample.group.parallel == sample.parallel

    for sample in test:
        sample.group.allocate(server)
    server.sync()
    for sample in test:
        assert sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server == server
        assert not sample.group.node_id_is_permanent
        assert sample.group.parallel == sample.parallel
        assert sample.group.name == sample.name

    for sample in control:
        assert not sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server is None
        assert not sample.group.node_id_is_permanent
        assert sample.group.parallel == sample.parallel
        assert sample.group.name == sample.name


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_group())
def test_allocate_02(server, strategy):

    control, test = strategy

    for sample in test + control:
        sample.group.allocate(server)
    server.sync()

    for sample in control:
        assert sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server == server
        assert not sample.group.node_id_is_permanent
        assert sample.group.parallel == sample.parallel
        assert sample.group.name == sample.name

    for sample in test:
        sample.group.free()
    server.sync()
    for sample in test:
        assert not sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server is None
        assert not sample.group.node_id_is_permanent
        assert sample.group.name == sample.name
        assert sample.group.parallel == sample.parallel

    for sample in control:
        assert sample.group.is_allocated
        assert not sample.group.is_paused
        assert sample.group.server == server
        assert not sample.group.node_id_is_permanent
        assert sample.group.parallel == sample.parallel
        assert sample.group.name == sample.name


@hypothesis.settings(hp_settings)
@hypothesis.given(strategy=st_group())
def test_allocate_03(server, strategy):

    control, test = strategy

    for sample in test + control:
        sample.group.allocate(server)
    server.sync()

    for sample in control:
        assert sample.group.is_allocated

    for allocate_frame in zip(*(_.allocate_pattern for _ in test)):
        for i, should_allocate in enumerate(allocate_frame):
            sample = test[i]
            if should_allocate:
                sample.group.allocate(server)
                # Fun time! Uncomment this to listen to the test:
                # import random
                # synth_a = supriya.realtime.Synth(
                #    amplitude=0.01,
                #    frequency=random.uniform(80, 500),
                #    pan=random.random(),
                # )
                #  sample.group.append(synth_a)
            else:
                sample.group.free()
            assert test[i].group.is_allocated is should_allocate
            sample.group.free()

    for sample in control:
        assert sample.group.is_allocated
        sample.group.free()


@hypothesis.settings(hp_settings)
@hypothesis.given(sample=st_group_sample())
def test_group_allocate_04(server, sample):

    osc_tag = "/g_new"
    if sample.parallel:
        osc_tag = "/p_new"

    for should_allocate in sample.allocate_pattern:
        if should_allocate:
            with server.osc_protocol.capture() as transcript:
                sample.group.allocate(server)
            assert sample.group.is_allocated
            assert [
                _.message
                for _ in transcript
                if _.message.address not in ("/status", "/status.reply", "/sync")
                and _.label == "S"
            ] == [OscMessage(osc_tag, sample.group.node_id, 0, 1)]
            sample.group.free()
        else:
            sample.group.allocate(server)
            node_id = sample.group.node_id
            with server.osc_protocol.capture() as transcript:
                sample.group.free()
            assert not sample.group.is_allocated
            assert [
                _.message
                for _ in transcript
                if _.message.address not in ("/status", "/status.reply", "/sync")
                and _.label == "S"
            ] == [OscMessage("/n_free", node_id)]
