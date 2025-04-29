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
    await session.boot()
    initial_tree = await debug_tree(session)
    assert initial_tree == normalize(
        """
        <session.contexts[0]>
            NODE TREE 1000 group (session.mixers[0]:group)
                1001 group (session.mixers[0]:tracks)
                    1006 group (session.mixers[0].tracks[0]:group)
                        1007 group (session.mixers[0].tracks[0]:tracks)
                        1010 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                            in_: 18.0, out: 7.0
                        1008 group (session.mixers[0].tracks[0]:devices)
                        1009 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                            active: c5, bus: 18.0, done_action: 2.0, gain: c6, gate: 1.0
                        1011 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                            in_: 18.0, out: 9.0
                        1012 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].output:synth)
                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                1004 supriya:meters:2 (session.mixers[0]:input-levels)
                    in_: 16.0, out: 1.0
                1002 group (session.mixers[0]:devices)
                1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                    active: 1.0, bus: 16.0, done_action: 2.0, gain: c0, gate: 1.0
                1005 supriya:meters:2 (session.mixers[0]:output-levels)
                    in_: 16.0, out: 3.0
                1013 supriya:patch-cable:2x2 (session.mixers[0].output:synth)
                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
        """
    )
    initial_components = debug_components(session)
    assert initial_components == normalize(
        """
        <Session 0>
            <session.contexts[0]>
                <Mixer 1 'P' session.mixers[0]>
                    <Track 3 'A' session.mixers[0].tracks[0]>
                        <TrackFeedback 4 session.mixers[0].tracks[0].feedback>
                        <TrackInput 5 session.mixers[0].tracks[0].input source=null>
                        <TrackOutput 6 session.mixers[0].tracks[0].output target=default>
                    <MixerOutput 2 session.mixers[0].output>
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
                    1006 group (session.mixers[0].tracks[0]:group)
                        1007 group (session.mixers[0].tracks[0]:tracks)
                            1012 group (session.mixers[0].tracks[0].tracks[0]:group)
                                1041 supriya:fb-patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].feedback:synth)
                                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 28.0, out: 20.0
                                1013 group (session.mixers[0].tracks[0].tracks[0]:tracks)
                                    1018 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:group)
                                        1019 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:tracks)
                                        1022 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:input-levels)
                                            in_: 22.0, out: 19.0
                                        1020 group (session.mixers[0].tracks[0].tracks[0].tracks[0]:devices)
                                        1021 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:channel-strip)
                                            active: c17, bus: 22.0, done_action: 2.0, gain: c18, gate: 1.0
                                        1023 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0].tracks[0]:output-levels)
                                            in_: 22.0, out: 21.0
                                        1024 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].tracks[0].output:synth)
                                            active: c17, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 22.0, out: 20.0
                                1016 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:input-levels)
                                    in_: 20.0, out: 13.0
                                1014 group (session.mixers[0].tracks[0].tracks[0]:devices)
                                1015 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[0]:channel-strip)
                                    active: c11, bus: 20.0, done_action: 2.0, gain: c12, gate: 1.0
                                1017 supriya:meters:2 (session.mixers[0].tracks[0].tracks[0]:output-levels)
                                    in_: 20.0, out: 15.0
                                1025 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[0].output:synth)
                                    active: c11, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 20.0, out: 18.0
                            1026 group (session.mixers[0].tracks[0].tracks[1]:group)
                                1027 group (session.mixers[0].tracks[0].tracks[1]:tracks)
                                1030 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:input-levels)
                                    in_: 24.0, out: 25.0
                                1028 group (session.mixers[0].tracks[0].tracks[1]:devices)
                                1029 supriya:channel-strip:2 (session.mixers[0].tracks[0].tracks[1]:channel-strip)
                                    active: c23, bus: 24.0, done_action: 2.0, gain: c24, gate: 1.0
                                1031 supriya:meters:2 (session.mixers[0].tracks[0].tracks[1]:output-levels)
                                    in_: 24.0, out: 27.0
                                1032 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].tracks[1].output:synth)
                                    active: c23, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 24.0, out: 18.0
                        1010 supriya:meters:2 (session.mixers[0].tracks[0]:input-levels)
                            in_: 18.0, out: 7.0
                        1008 group (session.mixers[0].tracks[0]:devices)
                        1009 supriya:channel-strip:2 (session.mixers[0].tracks[0]:channel-strip)
                            active: c5, bus: 18.0, done_action: 2.0, gain: c6, gate: 1.0
                        1051 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].sends[0]:synth)
                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 26.0
                        1011 supriya:meters:2 (session.mixers[0].tracks[0]:output-levels)
                            in_: 18.0, out: 9.0
                        1033 supriya:patch-cable:2x2 (session.mixers[0].tracks[0].output:synth)
                            active: c5, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 18.0, out: 16.0
                    1034 group (session.mixers[0].tracks[1]:group)
                        1035 group (session.mixers[0].tracks[1]:tracks)
                        1038 supriya:meters:2 (session.mixers[0].tracks[1]:input-levels)
                            in_: 26.0, out: 31.0
                        1036 group (session.mixers[0].tracks[1]:devices)
                        1037 supriya:channel-strip:2 (session.mixers[0].tracks[1]:channel-strip)
                            active: c29, bus: 26.0, done_action: 2.0, gain: c30, gate: 1.0
                        1042 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].sends[0]:synth)
                            active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 28.0
                        1039 supriya:meters:2 (session.mixers[0].tracks[1]:output-levels)
                            in_: 26.0, out: 33.0
                        1040 supriya:patch-cable:2x2 (session.mixers[0].tracks[1].output:synth)
                            active: c29, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 26.0, out: 16.0
                    1043 group (session.mixers[0].tracks[2]:group)
                        1044 group (session.mixers[0].tracks[2]:tracks)
                        1047 supriya:meters:2 (session.mixers[0].tracks[2]:input-levels)
                            in_: 30.0, out: 37.0
                        1045 group (session.mixers[0].tracks[2]:devices)
                        1046 supriya:channel-strip:2 (session.mixers[0].tracks[2]:channel-strip)
                            active: c35, bus: 30.0, done_action: 2.0, gain: c36, gate: 1.0
                        1048 supriya:meters:2 (session.mixers[0].tracks[2]:output-levels)
                            in_: 30.0, out: 39.0
                        1049 supriya:patch-cable:2x2 (session.mixers[0].tracks[2].output:synth)
                            active: c35, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 30.0, out: 16.0
                1004 supriya:meters:2 (session.mixers[0]:input-levels)
                    in_: 16.0, out: 1.0
                1002 group (session.mixers[0]:devices)
                1003 supriya:channel-strip:2 (session.mixers[0]:channel-strip)
                    active: 1.0, bus: 16.0, done_action: 2.0, gain: c0, gate: 1.0
                1005 supriya:meters:2 (session.mixers[0]:output-levels)
                    in_: 16.0, out: 3.0
                1050 supriya:patch-cable:2x2 (session.mixers[0].output:synth)
                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 16.0, out: 0.0
            NODE TREE 1052 group (session.mixers[1]:group)
                1053 group (session.mixers[1]:tracks)
                    1058 group (session.mixers[1].tracks[0]:group)
                        1059 group (session.mixers[1].tracks[0]:tracks)
                        1062 supriya:meters:2 (session.mixers[1].tracks[0]:input-levels)
                            in_: 34.0, out: 48.0
                        1060 group (session.mixers[1].tracks[0]:devices)
                        1061 supriya:channel-strip:2 (session.mixers[1].tracks[0]:channel-strip)
                            active: c46, bus: 34.0, done_action: 2.0, gain: c47, gate: 1.0
                        1063 supriya:meters:2 (session.mixers[1].tracks[0]:output-levels)
                            in_: 34.0, out: 50.0
                        1064 supriya:patch-cable:2x2 (session.mixers[1].tracks[0].output:synth)
                            active: c46, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 34.0, out: 32.0
                1056 supriya:meters:2 (session.mixers[1]:input-levels)
                    in_: 32.0, out: 42.0
                1054 group (session.mixers[1]:devices)
                1055 supriya:channel-strip:2 (session.mixers[1]:channel-strip)
                    active: 1.0, bus: 32.0, done_action: 2.0, gain: c41, gate: 1.0
                1057 supriya:meters:2 (session.mixers[1]:output-levels)
                    in_: 32.0, out: 44.0
                1065 supriya:patch-cable:2x2 (session.mixers[1].output:synth)
                    active: 1.0, done_action: 2.0, gain: 0.0, gate: 1.0, in_: 32.0, out: 0.0
        """
    )
    initial_components = debug_components(session)
    assert initial_components == normalize(
        """
        <Session 0>
            <session.contexts[0]>
                <Mixer 1 'P' session.mixers[0]>
                    <Track 5 'A' session.mixers[0].tracks[0]>
                        <TrackFeedback 6 session.mixers[0].tracks[0].feedback>
                        <TrackInput 7 session.mixers[0].tracks[0].input source=null>
                        <Track 17 'A1' session.mixers[0].tracks[0].tracks[0]>
                            <TrackFeedback 18 session.mixers[0].tracks[0].tracks[0].feedback>
                            <TrackInput 19 session.mixers[0].tracks[0].tracks[0].input source=null>
                            <Track 25 'A11' session.mixers[0].tracks[0].tracks[0].tracks[0]>
                                <TrackFeedback 26 session.mixers[0].tracks[0].tracks[0].tracks[0].feedback>
                                <TrackInput 27 session.mixers[0].tracks[0].tracks[0].tracks[0].input source=null>
                                <TrackOutput 28 session.mixers[0].tracks[0].tracks[0].tracks[0].output target=default>
                            <TrackOutput 20 session.mixers[0].tracks[0].tracks[0].output target=default>
                        <Track 21 'A2' session.mixers[0].tracks[0].tracks[1]>
                            <TrackFeedback 22 session.mixers[0].tracks[0].tracks[1].feedback>
                            <TrackInput 23 session.mixers[0].tracks[0].tracks[1].input source=null>
                            <TrackOutput 24 session.mixers[0].tracks[0].tracks[1].output target=default>
                        <TrackOutput 8 session.mixers[0].tracks[0].output target=default>
                        <TrackSend 33 session.mixers[0].tracks[0].sends[0] target=session.mixers[0].tracks[1]>
                    <Track 9 'B' session.mixers[0].tracks[1]>
                        <TrackFeedback 10 session.mixers[0].tracks[1].feedback>
                        <TrackInput 11 session.mixers[0].tracks[1].input source=null>
                        <TrackOutput 12 session.mixers[0].tracks[1].output target=default>
                        <TrackSend 34 session.mixers[0].tracks[1].sends[0] target=session.mixers[0].tracks[0].tracks[0]>
                    <Track 13 'C' session.mixers[0].tracks[2]>
                        <TrackFeedback 14 session.mixers[0].tracks[2].feedback>
                        <TrackInput 15 session.mixers[0].tracks[2].input source=null>
                        <TrackOutput 16 session.mixers[0].tracks[2].output target=default>
                    <MixerOutput 2 session.mixers[0].output>
                <Mixer 3 'Q' session.mixers[1]>
                    <Track 29 'D' session.mixers[1].tracks[0]>
                        <TrackFeedback 30 session.mixers[1].tracks[0].feedback>
                        <TrackInput 31 session.mixers[1].tracks[0].input source=null>
                        <TrackOutput 32 session.mixers[1].tracks[0].output target=default>
                    <MixerOutput 4 session.mixers[1].output>
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
