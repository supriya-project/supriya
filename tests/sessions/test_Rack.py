import pytest

from supriya.sessions import Chain, Rack, Session

from .conftest import Scenario


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.parametrize(
    "scenario",
    [
        Scenario(
            id="add chain to rack w/ 1 chain",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
            ],
            subject="mixers[0].devices[0]",
            expected_components_diff=lambda session: """
            --- initial
            +++ mutation
            @@ -3,3 +3,4 @@
                     <Mixer 1 'Mixer'>
                         <Rack 2 'Self'>
                             <Chain 3>
            +                <Chain 4>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -18,6 +18,18 @@
                                         active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
                                     1015 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
                                         in_: 18.0, out: 10.0
            +                    1017 group (session.mixers[0].devices[0].chains[1]:group)
            +                        1019 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0].chains[1]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                        1020 supriya:meters:2 (session.mixers[0].devices[0].chains[1]:input-levels)
            +                            in_: 18.0, out: 14.0
            +                        1018 group (session.mixers[0].devices[0].chains[1]:devices)
            +                        1021 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[1]:channel-strip)
            +                            active: c12, done_action: 2.0, gain: c13, gate: 1.0, out: 18.0
            +                        1023 supriya:patch-cable:2x2 (session.mixers[0].devices[0].chains[1]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1022 supriya:meters:2 (session.mixers[0].devices[0].chains[1]:output-levels)
            +                            in_: 18.0, out: 16.0
                             1009 supriya:patch-cable:2x2 (session.mixers[0].devices[0]:output)
                                 active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
            """,
            expected_messages="""
            - [None, [['/c_set', 12, 1.0, 13, 0.0], ['/c_fill', 14, 2, 0.0, 16, 2, 0.0]]]
            - [None,
               [['/g_new', 1017, 3, 1010, 1018, 1, 1017],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1019, 2, 1018, 'in_', 16.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1020, 3, 1019, 'in_', 18.0, 'out', 14.0],
                ['/s_new', 'supriya:channel-strip:2', 1021, 3, 1018, 'active', 'c12', 'gain', 'c13', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1022, 3, 1021, 'in_', 18.0, 'out', 16.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1023, 3, 1021, 'in_', 18.0, 'out', 20.0]]]
            """,
        ),
        Scenario(
            id="add chain to rack w/ 0 chains",
            commands=[
                (None, "add_mixer", {"name": "Mixer"}),
                ("mixers[0]", "add_rack", {"name": "Self"}),
                ("mixers[0].devices[0].chains[0]", "delete", {}),
            ],
            subject="mixers[0].devices[0]",
            expected_components_diff=lambda session: """
            --- initial
            +++ mutation
            @@ -2,3 +2,4 @@
                 <session.contexts[0]>
                     <Mixer 1 'Mixer'>
                         <Rack 2 'Self'>
            +                <Chain 4>
            """,
            expected_tree_diff="""
            --- initial
            +++ mutation
            @@ -4,6 +4,22 @@
                     1004 supriya:meters:2 (session.mixers[0]:input-levels)
                         in_: 16.0, out: 1.0
                     1002 group (session.mixers[0]:devices)
            +            1007 group (session.mixers[0].devices[0]:group)
            +                1008 group (session.mixers[0].devices[0]:chains)
            +                    1010 group (session.mixers[0].devices[0].chains[0]:group)
            +                        1012 supriya:patch-cable:2x2:replace (session.mixers[0].devices[0].chains[0]:input)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 18.0
            +                        1013 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:input-levels)
            +                            in_: 18.0, out: 7.0
            +                        1011 group (session.mixers[0].devices[0].chains[0]:devices)
            +                        1014 supriya:channel-strip:2 (session.mixers[0].devices[0].chains[0]:channel-strip)
            +                            active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
            +                        1016 supriya:patch-cable:2x2 (session.mixers[0].devices[0].chains[0]:output)
            +                            active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 20.0
            +                        1015 supriya:meters:2 (session.mixers[0].devices[0].chains[0]:output-levels)
            +                            in_: 18.0, out: 9.0
            +                1009 supriya:patch-cable:2x2 (session.mixers[0].devices[0]:output)
            +                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 16.0
                     1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                         active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                     1005 supriya:meters:2 (session.mixers[0]:output-levels)
            """,
            expected_messages="""
            - ['/d_recv', <SynthDef: supriya:patch-cable:2x2:replace>]
            - ['/sync', 3]
            - [None, [['/c_set', 5, 1.0, 6, 0.0], ['/c_fill', 7, 2, 0.0, 9, 2, 0.0]]]
            - ['/c_set', 11, 1.0]
            - [None,
               [['/g_new', 1007, 0, 1002, 1008, 0, 1007],
                ['/s_new', 'supriya:patch-cable:2x2', 1009, 3, 1008, 'in_', 20.0, 'out', 16.0]]]
            - [None,
               [['/g_new', 1010, 0, 1008, 1011, 1, 1010],
                ['/s_new', 'supriya:patch-cable:2x2:replace', 1012, 2, 1011, 'in_', 16.0, 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1013, 3, 1012, 'in_', 18.0, 'out', 7.0],
                ['/s_new', 'supriya:channel-strip:2', 1014, 3, 1011, 'active', 'c5', 'gain', 'c6', 'out', 18.0],
                ['/s_new', 'supriya:meters:2', 1015, 3, 1014, 'in_', 18.0, 'out', 9.0],
                ['/s_new', 'supriya:patch-cable:2x2', 1016, 3, 1014, 'in_', 18.0, 'out', 20.0]]]
            """,
        ),
    ],
    ids=lambda value: value.id,
)
@pytest.mark.asyncio
async def test_Rack_add_chain(scenario: Scenario, online: bool) -> None:
    async with scenario.run(online=online) as session:
        subject = session[scenario.subject]
        assert isinstance(subject, Rack)
        chain = await subject.add_chain()
    assert isinstance(chain, Chain)
    assert chain in subject.chains
    assert chain.parent is subject
    assert subject.chains[-1] is chain


@pytest.mark.xfail
@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Rack_set_channel_count(online: bool) -> None:
    raise RuntimeError


@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Rack_set_name(online: bool) -> None:
    session = Session()
    mixer = await session.add_mixer()
    rack = await mixer.add_rack()
    if online:
        await session.boot()
    assert rack.name is None
    for name in ("Foo", "Bar", "Baz"):
        rack.set_name(name=name)
        assert rack.name == name
    rack.set_name(name=None)
    assert rack.name is None


@pytest.mark.xfail
@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Rack_set_read_mode(online: bool) -> None:
    raise RuntimeError


@pytest.mark.xfail
@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Rack_set_write_mode(online: bool) -> None:
    raise RuntimeError


@pytest.mark.xfail
@pytest.mark.parametrize("online", [False, True])
@pytest.mark.asyncio
async def test_Rack_ungroup(online: bool) -> None:
    raise RuntimeError
