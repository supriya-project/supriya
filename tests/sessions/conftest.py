import asyncio
import contextlib
import dataclasses
import difflib
import inspect
import pprint
from typing import AsyncGenerator, Callable, Generator, Literal, Type

import pytest
from uqbar.strings import normalize

from supriya import AsyncServer, BootStatus, OscBundle, OscMessage
from supriya.sessions import Component, Session
from supriya.sessions.components import LevelsCheckable
from supriya.ugens import (
    decompile_synthdefs,
    system,  # lookup system.LAG_TIME to support monkeypatching
)


@dataclasses.dataclass(frozen=True)
class Scenario:
    id: str | None = dataclasses.field(default=None, kw_only=True)
    commands: list[tuple[str | None, str, dict | None]] | None = dataclasses.field(
        default=None, kw_only=True
    )
    expected_exception: Type[Exception] | None = dataclasses.field(
        default=None, kw_only=True
    )
    expected_components_diff: Callable[[Session], str] | str | None = dataclasses.field(
        default=None, kw_only=True
    )
    expected_levels: list[tuple[str, list[float], list[float]]] | None = (
        dataclasses.field(default=None, kw_only=True)
    )
    expected_messages: str | None = dataclasses.field(default=None, kw_only=True)
    expected_tree_diff: str | None = dataclasses.field(default=None, kw_only=True)
    subject: str = dataclasses.field(default="", kw_only=True)

    @contextlib.asynccontextmanager
    async def run(
        self,
        *,
        annotation_style: Literal["nested", "numeric"] | None = "nested",
        context_index: int = 0,
        online: bool,
    ) -> AsyncGenerator[Session, None]:
        # print("Pre-conditions")
        session = Session()
        if self.commands:
            await apply_commands(session, self.commands)
        initial_tree: str = ""
        assert session.boot_status == BootStatus.OFFLINE
        if online:
            await session.boot()
            assert session.boot_status == BootStatus.ONLINE
            await session.sync()
            initial_tree = await debug_tree(
                session=session, annotation_style=annotation_style
            )
            fallback_annotations = session._gather_annotations_by_context(
                annotation_style=annotation_style
            )
        initial_components = debug_components(session)
        # print("Operation")
        with (
            pytest.raises(self.expected_exception)
            if self.expected_exception
            else contextlib.nullcontext()
        ):
            with capture(
                session.contexts[context_index] if session.contexts else None
            ) as messages:
                yield session
        # print("Post-conditions")
        if self.expected_components_diff is not None:
            assert_components_diff(
                session, self.expected_components_diff, initial_components
            )
        if not online:
            return
        if self.expected_messages is not None:
            assert format_messages(messages) == normalize(self.expected_messages)
        # in case of an explicit session quit
        if self.expected_tree_diff is not None:
            await assert_tree_diff(
                annotation_style=annotation_style,
                expected_diff=self.expected_tree_diff,
                expected_initial_tree=initial_tree,
                fallback_annotations=fallback_annotations,
                session=session,
            )
        if self.expected_levels is not None:
            await asyncio.sleep(system.LAG_TIME * 2)
            actual_levels = [
                (
                    component.name or component.address,
                    [round(x, 2) for x in component.input_levels],
                    [round(x, 2) for x in component.output_levels],
                )
                for component in session.walk(Component)
                if isinstance(component, LevelsCheckable)
            ]
            assert actual_levels == self.expected_levels


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
    *,
    annotation_style: Literal["nested", "numeric"] | None = "nested",
    fallback_annotations: dict[AsyncServer, dict[int, str]] | None = None,
    label: str = "initial tree",
    session: Session,
) -> str:
    if not session.contexts:
        return "<empty>"
    tree = normalize(
        str(
            await session.dump_tree(
                annotation_style=annotation_style,
                fallback_annotations=fallback_annotations,
            )
        )
    )
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
    *,
    session: Session,
    initial_tree: str,
    annotation_style: Literal["nested", "numeric"] | None = "nested",
    fallback_annotations: dict[AsyncServer, dict[int, str]] | None = None,
) -> str:
    actual_tree = await debug_tree(
        annotation_style=annotation_style,
        fallback_annotations=fallback_annotations,
        label="actual tree",
        session=session,
    )
    return compute_diff(initial_tree, actual_tree)


async def assert_tree_diff(
    *,
    session: Session,
    expected_diff: str,
    expected_initial_tree: str,
    annotation_style: Literal["nested", "numeric"] | None = "nested",
    fallback_annotations: dict[AsyncServer, dict[int, str]] | None = None,
) -> None:
    actual_diff = await compute_tree_diff(
        annotation_style=annotation_style,
        fallback_annotations=fallback_annotations,
        initial_tree=expected_initial_tree,
        session=session,
    )
    assert normalize(expected_diff) == actual_diff
