import dataclasses

import pytest

from supriya.sessions.device_configs import DEFAULT_SYNTH_CONFIG
from supriya.sessions.performers import NoteOff, NoteOn, PerformanceEvent, Performer

from .conftest import Scenario


@dataclasses.dataclass(frozen=True)
class PerformScenario(Scenario):
    events: list[list[PerformanceEvent]]


@pytest.mark.parametrize(
    "scenario",
    [
        PerformScenario(
            commands=[(None, "add_mixer", {"name": "Mixer"})],
            events=[[NoteOn(64, 77)]],
            expected_logs="""
            performing loop: self=<Mixer 1 'Mixer'> performer=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            """,
            subject="mixers[0]",
        ),
        PerformScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_device", {"name": "Device"}),
            ],
            events=[[NoteOn(64, 77)]],
            expected_logs="""
            performing loop: self=<Mixer 1 'Mixer'> performer=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Device 2 'Device'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Mixer 1 'Mixer'> io=write events=[NoteOn(note_number=64, velocity=77)]
            """,
            subject="mixers[0]",
        ),
        PerformScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_device", {"name": "Device 1"}),
                ("mixers[0]", "add_device", {"name": "Device 2"}),
            ],
            events=[[NoteOn(64, 77)]],
            expected_logs="""
            performing loop: self=<Mixer 1 'Mixer'> performer=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Device 2 'Device 1'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Device 3 'Device 2'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Mixer 1 'Mixer'> io=write events=[NoteOn(note_number=64, velocity=77)]
            """,
            subject="mixers[0]",
        ),
        PerformScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
            ],
            events=[[NoteOn(64, 77)]],
            expected_logs="""
            performing loop: self=<Mixer 1 'Mixer'> performer=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Rack 2 'Rack'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Chain 3 'Chain 1'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Rack 2 'Rack'> io=write events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Mixer 1 'Mixer'> io=write events=[NoteOn(note_number=64, velocity=77)]
            """,
            subject="mixers[0]",
        ),
        PerformScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Rack"}),
                ("mixers[0].devices[0].chains[0]", "add_device", {"name": "Device"}),
            ],
            events=[[NoteOn(64, 77)]],
            expected_logs="""
            performing loop: self=<Mixer 1 'Mixer'> performer=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Rack 2 'Rack'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Chain 3 'Chain 1'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Device 4 'Device'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Chain 3 'Chain 1'> io=write events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Rack 2 'Rack'> io=write events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Mixer 1 'Mixer'> io=write events=[NoteOn(note_number=64, velocity=77)]
            """,
            subject="mixers[0]",
        ),
        PerformScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"chain_count": 2, "name": "Rack"}),
            ],
            events=[[NoteOn(64, 77)]],
            expected_logs="""
            performing loop: self=<Mixer 1 'Mixer'> performer=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Mixer 1 'Mixer'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Rack 2 'Rack'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Chain 3 'Chain 1'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Chain 4 'Chain 2'> io=read events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Rack 2 'Rack'> io=write events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Rack 2 'Rack'> io=write events=[NoteOn(note_number=64, velocity=77)]
            performing: self=<Mixer 1 'Mixer'> io=write events=[NoteOn(note_number=64, velocity=77)]
            """,
            subject="mixers[0]",
        ),
        PerformScenario(
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_device", {"device_config": DEFAULT_SYNTH_CONFIG}),
            ],
            events=[
                [NoteOn(64, 127)],
                [NoteOff(0, 127)],
            ],
            expected_logs="",
            subject="mixers[0]",
        ),
    ],
)
@pytest.mark.asyncio
async def test_Performer_perform(
    caplog: pytest.LogCaptureFixture, scenario: PerformScenario
) -> None:
    async with scenario.run(caplog=caplog, online=True) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Performer)
        for events in scenario.events:
            subject.perform(events)
