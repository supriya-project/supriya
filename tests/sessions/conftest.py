import contextlib
import difflib
import inspect
import pprint
from typing import AsyncGenerator, Callable, Generator, Literal

import pytest_asyncio
from uqbar.strings import normalize

from supriya import AsyncServer, BootStatus, OscBundle, OscMessage
from supriya.sessions import Session
from supriya.ugens import decompile_synthdefs


async def apply_commands(
    session: Session,
    commands: list[tuple[str | None, str, dict | None]],
) -> None:
    for command in commands:
        if command[0] is None:
            procedure = getattr(session, command[1])
        else:
            procedure = getattr(session[command[0]], command[1])
        kwargs = {}
        if command[2]:
            for key, value in command[2].items():
                if isinstance(value, str) and session._PATH_REGEX.match(value):
                    value = session[value]
                kwargs[key] = value
        if inspect.iscoroutinefunction(procedure):
            await procedure(**kwargs)
        else:
            procedure(**kwargs)


@contextlib.contextmanager
def capture(
    context: AsyncServer | None,
) -> Generator[list[OscBundle | OscMessage], None, None]:
    entries: list[OscBundle | OscMessage] = []
    if not context:
        yield entries
    else:
        with context.osc_protocol.capture() as transcript:
            yield entries
        entries.extend(
            [
                entry.message
                for entry in transcript.filtered(received=False, status=False)
            ]
        )


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
    session: Session,
    label: str = "initial tree",
    annotation: Literal["nested", "numeric"] | None = "nested",
) -> str:
    if not session.contexts:
        return "<empty>"
    tree = normalize(str(await session.dump_tree(annotation=annotation)))
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
    expected_diff: Callable[[Session], str] | str,
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
    if not isinstance(expected_diff, str):
        expected_diff = expected_diff(session)
    assert normalize(expected_diff) == normalize(actual_diff)


async def compute_tree_diff(
    session: Session,
    initial_tree: str,
    annotation: Literal["nested", "numeric"] | None = "nested",
) -> str:
    actual_tree = await debug_tree(session, "actual tree", annotation=annotation)
    return compute_diff(initial_tree, actual_tree)


async def assert_tree_diff(
    session: Session,
    expected_diff: str,
    expected_initial_tree: str,
    annotation: Literal["nested", "numeric"] | None = "nested",
) -> None:
    actual_diff = await compute_tree_diff(
        session=session,
        initial_tree=expected_initial_tree,
        annotation=annotation,
    )
    assert normalize(expected_diff) == actual_diff


does_not_raise = contextlib.nullcontext()


@contextlib.asynccontextmanager
async def run_test(
    *,
    annotation: Literal["nested", "numeric"] | None = "nested",
    commands: list[tuple[str | None, str, dict | None]] | None = None,
    context_index: int = 0,
    expected_components_diff: Callable[[Session], str] | str | None = None,
    expected_messages: str | None = "",
    expected_tree_diff: str | None = "",
    online: bool,
) -> AsyncGenerator[Session, None]:
    print("Pre-conditions")
    session = Session()
    if commands:
        await apply_commands(session, commands)
    initial_tree: str = ""
    assert session.boot_status == BootStatus.OFFLINE
    if online:
        await session.boot()
        assert session.boot_status == BootStatus.ONLINE
        await session.sync()
        initial_tree = await debug_tree(session, annotation=annotation)
    initial_components = debug_components(session)
    print("Operation")
    with capture(
        session.contexts[context_index] if session.contexts else None
    ) as messages:
        yield session
    print("Post-conditions")
    if expected_components_diff is not None:
        assert_components_diff(session, expected_components_diff, initial_components)
    if not online:
        return
    # in case of an explicit session quit
    if expected_tree_diff is not None:
        await assert_tree_diff(
            session,
            expected_tree_diff,
            expected_initial_tree=initial_tree,
            annotation=annotation,
        )
    if expected_messages is not None:
        assert format_messages(messages) == normalize(expected_messages)


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
        <Session 0 ONLINE>
        """
    )
    await session.quit()
    # for component in session._walk():
    #     print(component.address, component.graph_order)
    return session, initial_components, initial_tree


@pytest_asyncio.fixture
async def basic_session() -> tuple[Session, str, str]:
    session = Session()
    mixer = await session.add_mixer(name="Mixer")
    await mixer.add_track(name="Track")
    with capture(session.contexts[0]) as messages:
        await session.boot()
    assert format_messages(messages) == normalize(
        """
        - ['/notify', 1]
        - ['/g_new', 1, 1, 0]
        - ['/d_recv', <SynthDef: supriya:link-ar:1>]
        - ['/d_recv', <SynthDef: supriya:link-ar:2>]
        - ['/d_recv', <SynthDef: supriya:link-ar:3>]
        - ['/d_recv', <SynthDef: supriya:link-ar:4>]
        - ['/d_recv', <SynthDef: supriya:link-ar:5>]
        - ['/d_recv', <SynthDef: supriya:link-ar:6>]
        - ['/d_recv', <SynthDef: supriya:link-ar:7>]
        - ['/d_recv', <SynthDef: supriya:link-ar:8>]
        - ['/d_recv', <SynthDef: supriya:link-ar:9>]
        - ['/d_recv', <SynthDef: supriya:link-ar:10>]
        - ['/d_recv', <SynthDef: supriya:link-ar:11>]
        - ['/d_recv', <SynthDef: supriya:link-ar:12>]
        - ['/d_recv', <SynthDef: supriya:link-ar:13>]
        - ['/d_recv', <SynthDef: supriya:link-ar:14>]
        - ['/d_recv', <SynthDef: supriya:link-ar:15>]
        - ['/d_recv', <SynthDef: supriya:link-ar:16>]
        - ['/d_recv', <SynthDef: supriya:link-kr:1>]
        - ['/d_recv', <SynthDef: supriya:link-kr:2>]
        - ['/d_recv', <SynthDef: supriya:link-kr:3>]
        - ['/d_recv', <SynthDef: supriya:link-kr:4>]
        - ['/d_recv', <SynthDef: supriya:link-kr:5>]
        - ['/d_recv', <SynthDef: supriya:link-kr:6>]
        - ['/d_recv', <SynthDef: supriya:link-kr:7>]
        - ['/d_recv', <SynthDef: supriya:link-kr:8>]
        - ['/d_recv', <SynthDef: supriya:link-kr:9>]
        - ['/d_recv', <SynthDef: supriya:link-kr:10>]
        - ['/d_recv', <SynthDef: supriya:link-kr:11>]
        - ['/d_recv', <SynthDef: supriya:link-kr:12>]
        - ['/d_recv', <SynthDef: supriya:link-kr:13>]
        - ['/d_recv', <SynthDef: supriya:link-kr:14>]
        - ['/d_recv', <SynthDef: supriya:link-kr:15>]
        - ['/d_recv', <SynthDef: supriya:link-kr:16>]
        - ['/sync', 0]
        - ['/d_recv', <SynthDef: supriya:channel-strip:2>]
        - ['/d_recv', <SynthDef: supriya:meters:2>]
        - ['/d_recv', <SynthDef: supriya:patch-cable:2x2>]
        - ['/sync', 1]
        - [None, [['/c_set', 0, 0.0], ['/c_fill', 1, 2, 0.0, 3, 2, 0.0]]]
        - [None, [['/c_set', 5, 1.0, 6, 0.0], ['/c_fill', 7, 2, 0.0, 9, 2, 0.0]]]
        - [None,
           [['/g_new', 1000, 0, 1, 1001, 0, 1000, 1002, 1, 1000],
            ['/s_new', 'supriya:channel-strip:2', 1003, 1, 1000, 'gain', 'c0', 'out', 16.0],
            ['/s_new', 'supriya:meters:2', 1004, 3, 1001, 'in_', 16.0, 'out', 1.0],
            ['/s_new', 'supriya:meters:2', 1005, 3, 1003, 'in_', 16.0, 'out', 3.0],
            ['/s_new', 'supriya:patch-cable:2x2', 1006, 1, 1000, 'in_', 16.0]]]
        - [None,
           [['/g_new', 1007, 0, 1001, 1008, 0, 1007, 1009, 1, 1007],
            ['/s_new', 'supriya:channel-strip:2', 1010, 1, 1007, 'active', 'c5', 'gain', 'c6', 'out', 18.0],
            ['/s_new', 'supriya:meters:2', 1011, 3, 1008, 'in_', 18.0, 'out', 7.0],
            ['/s_new', 'supriya:meters:2', 1012, 3, 1010, 'in_', 18.0, 'out', 9.0],
            ['/s_new', 'supriya:patch-cable:2x2', 1013, 1, 1007, 'active', 'c5', 'in_', 18.0, 'out', 16.0]]]
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
        <Session 0 ONLINE>
            <session.contexts[0]>
                <Mixer 1 'Mixer'>
                    <Track 2 'Track'>
        """
    )
    await session.quit()
    # for component in session._walk():
    #     print(component.address, component.graph_order)
    return session, initial_components, initial_tree
