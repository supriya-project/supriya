import contextlib
import difflib
import os
import platform
import pprint
from typing import Generator

import pytest
import pytest_asyncio
from pytest_mock import MockerFixture
from uqbar.strings import normalize

from supriya import AsyncServer, OscBundle, OscMessage
from supriya.mixers import Session
from supriya.ugens import decompile_synthdefs


@contextlib.contextmanager
def capture(
    context: AsyncServer | None,
) -> Generator[list[OscBundle | OscMessage], None, None]:
    entries: list[OscBundle | OscMessage] = []
    if context is None:
        yield entries
    else:
        with context.osc_protocol.capture() as transcript:
            yield entries
        entries.extend(transcript.filtered(received=False, status=False))


def format_messages(messages: list[OscBundle | OscMessage]) -> str:
    def sanitize(list_):
        for i, x in enumerate(list_):
            if isinstance(x, bytes):
                try:
                    decompiled = decompile_synthdefs(x)
                    list_[i] = decompiled[0] if len(decompiled) == 1 else decompiled
                except Exception:
                    pass
            elif isinstance(x, list):
                sanitize(x)
        return list_

    lines: list[str] = []
    for message in messages:
        sanitized = sanitize(message.to_list())
        formatted = pprint.pformat(sanitized, width=120)
        for i, line in enumerate(formatted.splitlines()):
            if i == 0:
                prefix = "-"
            else:
                prefix = " "
            lines.append(f"{prefix} {line}")
    return "\n".join(lines)


def debug_components(session: Session) -> str:
    components = normalize(session.dump_components())
    for i, context in enumerate(session.contexts):
        components = components.replace(repr(context), f"<session.contexts[{i}]>")
    return components


async def debug_tree(
    session: Session, label: str = "initial tree", annotated: bool = True
) -> str:
    if not session.contexts:
        return "<empty>"
    tree = normalize(str(await session.dump_tree(annotated=annotated)))
    for i, context in enumerate(session.contexts):
        tree = tree.replace(repr(context), f"<session.contexts[{i}]>")
    # print(f"{label}:\n{tree}")
    return tree


def compute_diff(initial: str, actual: str) -> str:
    return normalize(
        "".join(
            difflib.unified_diff(
                (normalize(initial) + "\n").splitlines(True),
                (normalize(actual) + "\n").splitlines(True),
                fromfile="initial",
                tofile="mutation",
            )
        )
    )


def assert_components_diff(
    session: Session,
    expected_diff: str,
    initial_components: str,
) -> None:
    initial_components = normalize(initial_components) + "\n"
    actual_components = normalize(debug_components(session)) + "\n"
    actual_diff = "".join(
        difflib.unified_diff(
            initial_components.splitlines(True),
            actual_components.splitlines(True),
            tofile="mutation",
            fromfile="initial",
        )
    )
    assert normalize(expected_diff) == normalize(actual_diff)


async def compute_tree_diff(
    session: Session,
    initial_tree: str,
    annotated: bool = True,
) -> str:
    actual_tree = await debug_tree(session, "actual tree", annotated=annotated)
    return compute_diff(initial_tree, actual_tree)


async def assert_tree_diff(
    session: Session,
    expected_diff: str,
    expected_initial_tree: str,
    annotated: bool = True,
) -> None:
    actual_diff = await compute_tree_diff(
        session=session, initial_tree=expected_initial_tree, annotated=annotated
    )
    assert normalize(expected_diff) == actual_diff


does_not_raise = contextlib.nullcontext()


@pytest_asyncio.fixture
async def bare_session() -> tuple[Session, str, str]:
    session = Session()
    assert not session.contexts
    assert not session.mixers
    await session.boot()
    initial_tree = await debug_tree(session)
    assert initial_tree == "<empty>"
    initial_components = debug_components(session)
    assert initial_components == normalize(
        """
        <Session 0>
        """
    )
    await session.quit()
    # for component in session._walk():
    #     print(component.address, component.graph_order)
    return session, initial_components, initial_tree


@pytest_asyncio.fixture
async def basic_session() -> tuple[Session, str, str]:
    session = Session()
    mixer = await session.add_mixer(name="P")
    await mixer.add_track(name="A")
    with capture(session.contexts[0]) as messages:
        await session.boot()
    assert format_messages(messages) == normalize(
        # TODO: These should be consolidated properly
        """
        - ['/notify', 1]
        - ['/g_new', 1, 1, 0]
        - ['/d_recv', <SynthDef: system_link_audio_1>]
        - ['/d_recv', <SynthDef: system_link_audio_10>]
        - ['/d_recv', <SynthDef: system_link_audio_11>]
        - ['/d_recv', <SynthDef: system_link_audio_12>]
        - ['/d_recv', <SynthDef: system_link_audio_13>]
        - ['/d_recv', <SynthDef: system_link_audio_14>]
        - ['/d_recv', <SynthDef: system_link_audio_15>]
        - ['/d_recv', <SynthDef: system_link_audio_16>]
        - ['/d_recv', <SynthDef: system_link_audio_2>]
        - ['/d_recv', <SynthDef: system_link_audio_3>]
        - ['/d_recv', <SynthDef: system_link_audio_4>]
        - ['/d_recv', <SynthDef: system_link_audio_5>]
        - ['/d_recv', <SynthDef: system_link_audio_6>]
        - ['/d_recv', <SynthDef: system_link_audio_7>]
        - ['/d_recv', <SynthDef: system_link_audio_8>]
        - ['/d_recv', <SynthDef: system_link_audio_9>]
        - ['/d_recv', <SynthDef: system_link_control_1>]
        - ['/d_recv', <SynthDef: system_link_control_10>]
        - ['/d_recv', <SynthDef: system_link_control_11>]
        - ['/d_recv', <SynthDef: system_link_control_12>]
        - ['/d_recv', <SynthDef: system_link_control_13>]
        - ['/d_recv', <SynthDef: system_link_control_14>]
        - ['/d_recv', <SynthDef: system_link_control_15>]
        - ['/d_recv', <SynthDef: system_link_control_16>]
        - ['/d_recv', <SynthDef: system_link_control_2>]
        - ['/d_recv', <SynthDef: system_link_control_3>]
        - ['/d_recv', <SynthDef: system_link_control_4>]
        - ['/d_recv', <SynthDef: system_link_control_5>]
        - ['/d_recv', <SynthDef: system_link_control_6>]
        - ['/d_recv', <SynthDef: system_link_control_7>]
        - ['/d_recv', <SynthDef: system_link_control_8>]
        - ['/d_recv', <SynthDef: system_link_control_9>]
        - ['/sync', 0]
        - ['/d_recv', <SynthDef: supriya:channel-strip:2>]
        - ['/sync', 1]
        - ['/d_recv', <SynthDef: supriya:meters:2>]
        - ['/sync', 2]
        - ['/d_recv', <SynthDef: supriya:patch-cable:2x2>]
        - ['/sync', 3]
        - ['/c_set', 0, 0.0]
        - ['/c_fill', 1, 2, 0.0]
        - ['/c_fill', 3, 2, 0.0]
        - ['/g_new', 1000, 0, 1]
        - ['/g_new', 1001, 0, 1000]
        - ['/g_new', 1002, 1, 1000]
        - ['/s_new', 'supriya:channel-strip:2', 1003, 1, 1000, 'gain', 'c0', 'out', 16.0]
        - ['/s_new', 'supriya:meters:2', 1004, 3, 1001, 'in_', 16.0, 'out', 1.0]
        - ['/s_new', 'supriya:meters:2', 1005, 3, 1003, 'in_', 16.0, 'out', 3.0]
        - ['/s_new', 'supriya:patch-cable:2x2', 1006, 1, 1000, 'in_', 16.0]
        - ['/c_set', 5, 1.0]
        - ['/c_set', 6, 0.0]
        - ['/c_fill', 7, 2, 0.0]
        - ['/c_fill', 9, 2, 0.0]
        - ['/g_new', 1007, 1, 1001]
        - ['/g_new', 1008, 0, 1007]
        - ['/g_new', 1009, 1, 1007]
        - ['/s_new', 'supriya:channel-strip:2', 1010, 1, 1007, 'active', 'c5', 'gain', 'c6', 'out', 18.0]
        - ['/s_new', 'supriya:meters:2', 1011, 3, 1008, 'in_', 18.0, 'out', 7.0]
        - ['/s_new', 'supriya:meters:2', 1012, 3, 1010, 'in_', 18.0, 'out', 9.0]
        - ['/s_new', 'supriya:patch-cable:2x2', 1013, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 16.0]
        """
    )
    initial_tree = await debug_tree(session)
    assert initial_tree == normalize(
        """
        <session.contexts[0]>
            NODE TREE 1000 group (session.mixers[0]:group)
                1001 group (session.mixers[0]:tracks)
                    1007 group (session.mixers[0].tracks[0]:group)
                        1008 group (session.mixers[0].tracks[0]:tracks)
                        1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                            in_: 18.0, out: 7.0
                        1009 group (session.mixers[0].tracks[0]:devices)
                        1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                            active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                        1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                            in_: 18.0, out: 9.0
                        1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                1004 supriya:meters:2 (session.mixers[0]:input-levels)
                    in_: 16.0, out: 1.0
                1002 group (session.mixers[0]:devices)
                1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                    active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                1005 supriya:meters:2 (session.mixers[0]:output-levels)
                    in_: 16.0, out: 3.0
                1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
        """
    )
    initial_components = debug_components(session)
    assert initial_components == normalize(
        """
        <Session 0>
            <session.contexts[0]>
                <Mixer 1 'P' session.mixers[0]>
                    <Track 2 'A' session.mixers[0].tracks[0]>
        """
    )
    await session.quit()
    # for component in session._walk():
    #     print(component.address, component.graph_order)
    return session, initial_components, initial_tree


@pytest_asyncio.fixture
async def complex_session() -> tuple[Session, str, str]:
    session = Session()
    mixer_one = await session.add_mixer(name="P")
    mixer_two = await session.add_mixer(name="Q")
    # tracks
    track_one = await mixer_one.add_track(name="A")  # track_one
    track_two = await mixer_one.add_track(name="B")  # track_two
    await mixer_one.add_track(name="C")  # track_three
    track_one_one = await track_one.add_track(name="A1")  # track_one_one
    await track_one.add_track(name="A2")  # track_one_two
    await track_one_one.add_track(name="A11")  # track_one_one_one
    await mixer_two.add_track(name="D")
    # add sends
    # TODO: Reimplement these
    await track_one.add_send(track_two)
    await track_two.add_send(track_one_one)
    # record initial tree
    await session.boot()
    initial_tree = await debug_tree(session)
    assert initial_tree == normalize(
        """
        <session.contexts[0]>
            NODE TREE 1000 group (session.mixers[0]:group)
                1001 group (session.mixers[0]:tracks)
                    1007 group (session.mixers[0].tracks[0]:group)
                        1008 group (session.mixers[0].tracks[0]:tracks)
                            1014 group (session.mixers[0].tracks[0].tracks[0]:group)
                                1015 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                    1021 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
                                        1022 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
                                        1025 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:input-levels)
                                            in_: 22.0, out: 19.0
                                        1023 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:devices)
                                        1024 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:channel-strip)
                                            active: c17, done_action: 2.0, gain: c18, gate: 1.0, out: 22.0
                                        1026 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output-levels)
                                            in_: 22.0, out: 21.0
                                        1027 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output)
                                            active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                1018 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
                                    in_: 20.0, out: 13.0
                                1016 group (session.mixers[0].tracks[0].tracks[0]:devices)
                                1017 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0]:channel-strip)
                                    active: c11, done_action: 2.0, gain: c12, gate: 1.0, out: 20.0
                                1019 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                    in_: 20.0, out: 15.0
                                1020 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0]:output)
                                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
                            1028 group (session.mixers[0].tracks[0].tracks[1]:group)
                                1029 group (session.mixers[0].tracks[0].tracks[1]:tracks)
                                1032 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:input-levels)
                                    in_: 24.0, out: 25.0
                                1030 group (session.mixers[0].tracks[0].tracks[1]:devices)
                                1031 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[1]:channel-strip)
                                    active: c23, done_action: 2.0, gain: c24, gate: 1.0, out: 24.0
                                1033 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:output-levels)
                                    in_: 24.0, out: 27.0
                                1034 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[1]:output)
                                    active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 18.0
                        1011 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                            in_: 18.0, out: 7.0
                        1009 group (session.mixers[0].tracks[0]:devices)
                        1010 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                            active: c5, done_action: 2.0, gain: c6, gate: 1.0, out: 18.0
                        1012 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                            in_: 18.0, out: 9.0
                        1013 supriya:patch-cable:2x2 (session.mixers[0].tracks[0]:output)
                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                    1035 group (session.mixers[0].tracks[1]:group)
                        1036 group (session.mixers[0].tracks[1]:tracks)
                        1039 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                            in_: 26.0, out: 31.0
                        1037 group (session.mixers[0].tracks[1]:devices)
                        1038 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                            active: c29, done_action: 2.0, gain: c30, gate: 1.0, out: 26.0
                        1040 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
                            in_: 26.0, out: 33.0
                        1041 supriya:patch-cable:2x2 (session.mixers[0].tracks[1]:output)
                            active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                    1042 group (session.mixers[0].tracks[2]:group)
                        1043 group (session.mixers[0].tracks[2]:tracks)
                        1046 supriya:meters:2 (session.mixers[0].tracks[2]:input-levels)
                            in_: 28.0, out: 37.0
                        1044 group (session.mixers[0].tracks[2]:devices)
                        1045 supriya:channel-strip:2 (session.mixers[0].tracks[2]:channel-strip)
                            active: c35, done_action: 2.0, gain: c36, gate: 1.0, out: 28.0
                        1047 supriya:meters:2 (session.mixers[0].tracks[2]:output-levels)
                            in_: 28.0, out: 39.0
                        1048 supriya:patch-cable:2x2 (session.mixers[0].tracks[2]:output)
                            active: c35, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 16.0
                1004 supriya:meters:2 (session.mixers[0]:input-levels)
                    in_: 16.0, out: 1.0
                1002 group (session.mixers[0]:devices)
                1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                    active: 1.0, done_action: 2.0, gain: c0, gate: 1.0, out: 16.0
                1005 supriya:meters:2 (session.mixers[0]:output-levels)
                    in_: 16.0, out: 3.0
                1006 supriya:patch-cable:2x2 (session.mixers[0]:output)
                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            NODE TREE 1049 group (session.mixers[1]:group)
                1050 group (session.mixers[1]:tracks)
                    1056 group (session.mixers[1].tracks[0]:group)
                        1057 group (session.mixers[1].tracks[0]:tracks)
                        1060 supriya:meters:2 (session.mixers[1].tracks[0]:input-levels)
                            in_: 32.0, out: 48.0
                        1058 group (session.mixers[1].tracks[0]:devices)
                        1059 supriya:channel-strip:2 (session.mixers[1].tracks[0]:channel-strip)
                            active: c46, done_action: 2.0, gain: c47, gate: 1.0, out: 32.0
                        1061 supriya:meters:2 (session.mixers[1].tracks[0]:output-levels)
                            in_: 32.0, out: 50.0
                        1062 supriya:patch-cable:2x2 (session.mixers[1].tracks[0]:output)
                            active: c46, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 32.0, out: 30.0
                1053 supriya:meters:2 (session.mixers[1]:input-levels)
                    in_: 30.0, out: 42.0
                1051 group (session.mixers[1]:devices)
                1052 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
                    active: 1.0, done_action: 2.0, gain: c41, gate: 1.0, out: 30.0
                1054 supriya:meters:2 (session.mixers[1]:output-levels)
                    in_: 30.0, out: 44.0
                1055 supriya:patch-cable:2x2 (session.mixers[1]:output)
                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 30.0, out: 0.0
        """
    )
    initial_components = debug_components(session)
    assert initial_components == normalize(
        """
        <Session 0>
            <session.contexts[0]>
                <Mixer 1 'P' session.mixers[0]>
                    <Track 3 'A' session.mixers[0].tracks[0]>
                        <Track 6 'A1' session.mixers[0].tracks[0].tracks[0]>
                            <Track 8 'A11' session.mixers[0].tracks[0].tracks[0].tracks[0]>
                        <Track 7 'A2' session.mixers[0].tracks[0].tracks[1]>
                    <Track 4 'B' session.mixers[0].tracks[1]>
                    <Track 5 'C' session.mixers[0].tracks[2]>
                <Mixer 2 'Q' session.mixers[1]>
                    <Track 9 'D' session.mixers[1].tracks[0]>
        """
    )
    await session.quit()
    # for component in session._walk():
    #     print(component.address, component.graph_order)
    return session, initial_components, initial_tree


@pytest.fixture(autouse=True)
def lag_time(mocker: MockerFixture):
    if platform.system() == "Windows" and os.environ.get("CI"):
        mocker.patch("supriya.mixers.synthdefs._get_lag_time", return_value=0.25)
