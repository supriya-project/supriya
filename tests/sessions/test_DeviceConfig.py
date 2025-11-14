import dataclasses

import pytest

from supriya.sessions import DeviceConfig, DeviceContainer

from .conftest import Scenario, apply_commands

COMMANDS: list[tuple[str | None, str, dict | None]] = [
    (None, "add_mixer", {"name": "Mixer"}),
    ("mixers[0]", "add_track", {"name": "Track One"}),
    ("mixers[0]", "add_track", {"name": "Track Two"}),
]


@dataclasses.dataclass(frozen=True)
class DeviceConfigScenario(Scenario):
    actions: list[tuple[str | None, str, dict | None]] = dataclasses.field(
        default_factory=list, kw_only=True
    )
    device_config: DeviceConfig = dataclasses.field(kw_only=True)


@pytest.mark.parametrize(
    "scenario",
    [
        DeviceConfigScenario(
            id="empty device",
            commands=COMMANDS,
            device_config=DeviceConfig(),
            subject="mixers[0].tracks[0]",
            expected_components_diff="""
            --- initial
            +++ mutation
            @@ -2,4 +2,5 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Track 2 'Track One'>
            +                <Device 4>
                         <Track 3 'Track Two'>
            """,
            expected_messages="""
            - ['/c_fill', 17, 2, 0.0]
            - [None, [['/g_new', 1021, 0, 1009], ['/s_new', 'supriya:meters:2', 1022, 1, 1021, 'in_', 18.0, 'out', 17.0]]]
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -6,6 +6,9 @@
                             1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                                 in_: 18.0, out: 7.0
                             1009 group (session.mixers[0].tracks[0]:devices)
            +                    1021 group (session.mixers[0].tracks[0].devices[0]:group)
            +                        1022 supriya:meters:2 (session.mixers[0].tracks[0].devices[0]:output-levels)
            +                            in_: 18.0, out: 17.0
                             1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                                 active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                             1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
            """,
        ),
    ],
    ids=lambda scenario: scenario.id,
)
@pytest.mark.asyncio
async def test_DeviceConfig(scenario: DeviceConfigScenario) -> None:
    async with scenario.run(online=True) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, DeviceContainer)
        await subject.add_device(scenario.device_config)
        await apply_commands(session, scenario.actions)
