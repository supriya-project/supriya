"""
Classes for modeling responses from :term:`scsynth`.
"""

import dataclasses
import re
from collections import deque
from typing import (
    Deque,
    Generator,
    Sequence,
    Type,
    cast,
)

from ..enums import NodeAction
from ..osc import OscMessage

# Editorial: It's annoying not having stronger (generated) type guarantees
# about OSC messages received from the server.


@dataclasses.dataclass
class Response:
    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        mapping: dict[str, Type[Response]] = {
            "/b_info": BufferInfo,
            "/b_set": GetBufferInfo,
            "/b_setn": GetBufferRangeInfo,
            "/c_set": GetControlBusInfo,
            "/c_setn": GetControlBusRangeInfo,
            "/d_removed": SynthDefRemovedInfo,
            "/done": DoneInfo,
            "/fail": FailInfo,
            "/g_queryTree.reply": QueryTreeInfo,
            "/n_end": NodeInfo,
            "/n_go": NodeInfo,
            "/n_info": NodeInfo,
            "/n_move": NodeInfo,
            "/n_off": NodeInfo,
            "/n_on": NodeInfo,
            "/n_set": GetNodeControlInfo,
            "/n_setn": GetNodeControlRangeInfo,
            "/status.reply": StatusInfo,
            "/synced": SyncedInfo,
            "/tr": TriggerInfo,
            "/version.reply": VersionInfo,
        }
        return mapping[str(osc_message.address)].from_osc(osc_message)


@dataclasses.dataclass
class BufferInfo(Response):
    """
    A ``/b_info`` response.
    """

    @dataclasses.dataclass
    class Item:
        buffer_id: int
        frame_count: int
        channel_count: int
        sample_rate: float

    items: Sequence[Item]

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        return cls(
            items=[
                cls.Item(
                    buffer_id=cast(int, osc_message.contents[i]),
                    frame_count=cast(int, osc_message.contents[i + 1]),
                    channel_count=cast(int, osc_message.contents[i + 2]),
                    sample_rate=cast(float, osc_message.contents[i + 3]),
                )
                for i in range(0, len(osc_message.contents), 4)
            ]
        )


@dataclasses.dataclass
class DoneInfo(Response):
    """
    A ``/done`` response.
    """

    command_name: str
    other: Sequence[float | str]

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        command_name = cast(str, osc_message.contents[0])
        other = cast(Sequence[float | str], osc_message.contents[1:])
        return cls(command_name=command_name, other=other)


@dataclasses.dataclass
class FailInfo(Response):
    """
    A ``/fail`` response.
    """

    command_name: str
    error: str
    other: Sequence[float | str]

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        return cls(
            command_name=cast(str, osc_message.contents[0]),
            error=cast(str, osc_message.contents[1]),
            other=cast(Sequence[float | str], osc_message.contents[2:]),
        )


@dataclasses.dataclass
class GetBufferInfo(Response):
    """
    A ``/b_set`` response.
    """

    buffer_id: int
    items: Sequence[tuple[int, float]]

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        buffer_id = cast(int, osc_message.contents[0])
        items: list[tuple[int, float]] = []
        for i in range(1, len(osc_message.contents), 2):
            index = cast(int, osc_message.contents[i])
            value = cast(float, osc_message.contents[i + 1])
            items.append((index, value))
        return cls(buffer_id=buffer_id, items=items)


@dataclasses.dataclass
class GetBufferRangeInfo(Response):
    """
    A ``/b_setn`` response.
    """

    buffer_id: int
    items: Sequence[tuple[int, Sequence[float]]]

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        buffer_id = cast(int, osc_message.contents[0])
        items: list[tuple[int, Sequence[float]]] = []
        current_index = 1
        while current_index < len(osc_message.contents):
            index = cast(int, osc_message.contents[current_index])
            count = cast(int, osc_message.contents[current_index + 1])
            current_index += 2
            values = cast(
                Sequence[float],
                osc_message.contents[current_index : current_index + count],
            )
            items.append((index, tuple(values)))
            current_index += count
        return cls(buffer_id=buffer_id, items=items)


@dataclasses.dataclass
class GetControlBusInfo(Response):
    """
    A ``/c_set`` response.
    """

    items: Sequence[tuple[int, float]]

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        items: list[tuple[int, float]] = []
        for i in range(0, len(osc_message.contents), 2):
            index = cast(int, osc_message.contents[i])
            value = cast(float, osc_message.contents[i + 1])
            items.append((index, value))
        return cls(items=items)


@dataclasses.dataclass
class GetControlBusRangeInfo(Response):
    """
    A ``/c_setn`` response.
    """

    items: Sequence[tuple[int, Sequence[float]]]

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        items: list[tuple[int, Sequence[float]]] = []
        current_index = 0
        while current_index < len(osc_message.contents):
            index = cast(int, osc_message.contents[current_index])
            count = cast(int, osc_message.contents[current_index + 1])
            current_index += 2
            values = cast(
                Sequence[float],
                osc_message.contents[current_index : current_index + count],
            )
            items.append((index, tuple(values)))
            current_index += count
        return cls(items=items)


@dataclasses.dataclass
class GetNodeControlInfo(Response):
    node_id: int
    items: Sequence[tuple[int | str, float]]

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        node_id = cast(int, osc_message.contents[0])
        items: list[tuple[int | str, float]] = []
        for i in range(1, len(osc_message.contents), 2):
            name_or_index = cast(int | str, osc_message.contents[i])
            value = cast(float, osc_message.contents[i + 1])
            items.append((name_or_index, value))
        return cls(node_id=node_id, items=items)


@dataclasses.dataclass
class GetNodeControlRangeInfo(Response):
    node_id: int
    items: Sequence[tuple[int | str, Sequence[float]]]

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        node_id = cast(int, osc_message.contents[0])
        items: list[tuple[int | str, Sequence[float]]] = []
        current_index = 1
        while current_index < len(osc_message.contents):
            name_or_index = cast(int | str, osc_message.contents[current_index])
            count = cast(int, osc_message.contents[current_index + 1])
            current_index += 2
            values = cast(
                Sequence[float],
                osc_message.contents[current_index : current_index + count],
            )
            items.append((name_or_index, values))
            current_index += count
        return cls(node_id=node_id, items=items)


@dataclasses.dataclass
class NodeInfo(Response):
    action: NodeAction
    node_id: int
    parent_id: int
    previous_id: int
    next_id: int
    is_group: bool
    head_id: int | None = None
    tail_id: int | None = None

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        node_id = cast(int, osc_message.contents[0])
        parent_id = cast(int, osc_message.contents[1])
        previous_id = cast(int, osc_message.contents[2])
        next_id = cast(int, osc_message.contents[3])
        is_group = cast(bool, osc_message.contents[4])
        if is_group:
            head_id: int | None = cast(int, osc_message.contents[5])
            tail_id: int | None = cast(int, osc_message.contents[6])
        else:
            head_id = None
            tail_id = None
        return cls(
            action=NodeAction.from_expr(osc_message.address),
            node_id=node_id,
            parent_id=parent_id,
            previous_id=previous_id,
            next_id=next_id,
            is_group=bool(is_group),
            head_id=head_id,
            tail_id=tail_id,
        )


@dataclasses.dataclass
class QueryTreeInfo(Response):
    """
    A ``/g_queryTree.reply`` response.
    """

    @dataclasses.dataclass
    class Item:
        node_id: int
        child_count: int
        synthdef_name: str | None = None
        controls: dict[int | str, float | str] | None = None

    node_id: int
    child_count: int
    items: Sequence[Item]

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        flag = bool(osc_message.contents[0])
        node_id = cast(int, osc_message.contents[1])
        child_count = cast(int, osc_message.contents[2])
        items: list["QueryTreeInfo.Item"] = []
        index = 3
        while index < len(osc_message.contents):
            child_id = cast(int, osc_message.contents[index])
            child_child_count = cast(int, osc_message.contents[index + 1])
            synthdef_name: str | None = None
            controls: dict[int | str, float | str] | None = None
            index += 2
            if child_child_count < 0:
                synthdef_name = cast(str, osc_message.contents[index])
                index += 1
                if flag:
                    controls = {}
                    control_count = cast(int, osc_message.contents[index])
                    index += 1
                    for i in range(control_count):
                        name_or_index: int | str = cast(
                            int | str, osc_message.contents[index]
                        )
                        value: float | str = cast(
                            float | str, osc_message.contents[index + 1]
                        )
                        controls[name_or_index] = value
                        index += 2
            items.append(
                cls.Item(
                    node_id=child_id,
                    child_count=child_child_count,
                    controls=controls,
                    synthdef_name=synthdef_name,
                )
            )
        return cls(node_id=node_id, child_count=child_count, items=items)


@dataclasses.dataclass
class QueryTreeControl:
    name_or_index: int | str
    value: float | str

    def __str__(self) -> str:
        if isinstance(self.value, str):
            return f"{self.name_or_index}: {self.value}"
        return f"{self.name_or_index}: {round(self.value, 6)!s}"


@dataclasses.dataclass
class QueryTreeNode:
    node_id: int
    annotation: str | None = None

    def _get_str_format_pieces(self, unindexed: bool = False) -> list[str]:
        raise NotImplementedError


@dataclasses.dataclass
class QueryTreeSynth(QueryTreeNode):
    node_id: int
    synthdef_name: str | None = None
    controls: list[QueryTreeControl] = dataclasses.field(default_factory=list)
    annotation: str | None = None

    def __format__(self, format_spec: str) -> str:
        return (
            "\n".join(self._get_str_format_pieces(unindexed=format_spec == "unindexed"))
            + "\n"
        )

    def __str__(self) -> str:
        return "\n".join(self._get_str_format_pieces()) + "\n"

    def _get_str_format_pieces(self, unindexed: bool = False) -> list[str]:
        result = []
        string = f"{'...' if unindexed else self.node_id} {self.synthdef_name}"
        if self.annotation:
            string += f" ({self.annotation})"
        result.append(string)
        if self.controls:
            result.append("    " + ", ".join(str(control) for control in self.controls))
        return result


@dataclasses.dataclass
class QueryTreeGroup(QueryTreeNode):
    node_id: int
    children: list[QueryTreeNode] = dataclasses.field(default_factory=list)
    annotation: str | None = None

    ### SPECIAL METHODS ###

    def __format__(self, format_spec: str) -> str:
        return (
            "NODE TREE "
            + "\n".join(
                self._get_str_format_pieces(unindexed=format_spec == "unindexed")
            )
            + "\n"
        )

    def __str__(self) -> str:
        return "NODE TREE " + "\n".join(self._get_str_format_pieces()) + "\n"

    ### PRIVATE METHODS ###

    def _get_str_format_pieces(self, unindexed: bool = False) -> list[str]:
        result = []
        string = f"{'...' if unindexed else self.node_id} group"
        if self.annotation:
            string += f" ({self.annotation})"
        result.append(string)
        for child in self.children:
            for line in child._get_str_format_pieces(unindexed=unindexed):
                result.append("    {}".format(line))
        return result

    ### PUBLIC METHODS ###

    def annotate(self, annotations: dict[int, str]) -> "QueryTreeGroup":
        root = self
        if root.node_id in annotations:
            root = dataclasses.replace(root, annotation=annotations[root.node_id])
        for group in root.walk():
            for i, child in enumerate(group.children):
                if child.node_id in annotations:
                    group.children[i] = dataclasses.replace(
                        child, annotation=annotations[child.node_id]
                    )
        return root

    @classmethod
    def from_query_tree_info(cls, response: QueryTreeInfo) -> "QueryTreeGroup":
        def recurse(
            item: QueryTreeInfo.Item, items: Deque[QueryTreeInfo.Item]
        ) -> QueryTreeGroup | QueryTreeSynth:
            if item.child_count < 0:
                return QueryTreeSynth(
                    node_id=item.node_id,
                    synthdef_name=item.synthdef_name,
                    controls=[
                        QueryTreeControl(name_or_index=name_or_index, value=value)
                        for name_or_index, value in (item.controls or {}).items()
                    ],
                )
            children: list[QueryTreeNode] = []
            for _ in range(item.child_count):
                children.append(recurse(items.popleft(), items))
            return QueryTreeGroup(node_id=item.node_id, children=children)

        return cast(
            QueryTreeGroup,
            recurse(
                QueryTreeInfo.Item(
                    node_id=response.node_id, child_count=response.child_count
                ),
                deque(response.items),
            ),
        )

    @classmethod
    def from_string(cls, string) -> "QueryTreeGroup":
        node_pattern = re.compile(r"^\s*(\d+) (\S+)$")
        control_pattern = re.compile(r"\w+: \S+")
        lines = string.splitlines()
        while not lines[0].startswith("NODE TREE"):
            lines.pop(0)
        if not lines:
            raise ValueError(string)
        stack: list[QueryTreeGroup] = [
            QueryTreeGroup(node_id=int(lines.pop(0).rpartition(" ")[-1]))
        ]
        for line in lines:
            indent = line.count("   ")
            if match := (node_pattern.match(line)):
                while len(stack) > indent:
                    stack.pop()
                node_id = int(match.groups()[0])
                if (name := match.groups()[1]) == "group":
                    stack[-1].children.append(group := QueryTreeGroup(node_id=node_id))
                    stack.append(group)
                else:
                    stack[-1].children.append(
                        synth := QueryTreeSynth(node_id=node_id, synthdef_name=name)
                    )
            else:
                for pair in control_pattern.findall(line):
                    name_string, _, value_string = pair.partition(": ")
                    try:
                        name_or_index: int | str = int(name_string)
                    except ValueError:
                        name_or_index = name_string
                    try:
                        value: float | str = float(value_string)
                    except ValueError:
                        value = value_string
                    synth.controls.append(
                        QueryTreeControl(name_or_index=name_or_index, value=value)
                    )
        return stack[0]

    def walk(self) -> Generator["QueryTreeGroup", None, None]:
        yield self
        for child in self.children:
            if isinstance(child, QueryTreeGroup):
                yield from child.walk()


@dataclasses.dataclass
class StatusInfo(Response):
    """
    A ``/status.reply`` response.
    """

    actual_sample_rate: float
    average_cpu_usage: float
    group_count: int
    peak_cpu_usage: float
    synth_count: int
    synthdef_count: int
    target_sample_rate: float
    ugen_count: int

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        ugen_count = cast(int, osc_message.contents[1])
        synth_count = cast(int, osc_message.contents[2])
        group_count = cast(int, osc_message.contents[3])
        synthdef_count = cast(int, osc_message.contents[4])
        average_cpu_usage = cast(float, osc_message.contents[5])
        peak_cpu_usage = cast(float, osc_message.contents[6])
        target_sample_rate = cast(float, osc_message.contents[7])
        actual_sample_rate = cast(float, osc_message.contents[8])
        return cls(
            actual_sample_rate=actual_sample_rate,
            average_cpu_usage=average_cpu_usage,
            group_count=group_count,
            peak_cpu_usage=peak_cpu_usage,
            synth_count=synth_count,
            synthdef_count=synthdef_count,
            target_sample_rate=target_sample_rate,
            ugen_count=ugen_count,
        )


@dataclasses.dataclass
class SyncedInfo(Response):
    """
    A ``/synced`` response.
    """

    sync_id: int

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        return cls(cast(int, osc_message.contents[0]))


@dataclasses.dataclass
class SynthDefRemovedInfo(Response):
    """
    A ``/d_removed`` response.
    """

    name: str

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        return cls(cast(str, osc_message.contents[0]))


@dataclasses.dataclass
class TriggerInfo(Response):
    """
    A ``/tr`` response.
    """

    node_id: int
    trigger_id: int
    value: float

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        node_id = cast(int, osc_message.contents[0])
        trigger_id = cast(int, osc_message.contents[1])
        value = cast(float, osc_message.contents[2])
        return cls(node_id, trigger_id, value)


@dataclasses.dataclass
class VersionInfo(Response):
    """
    A ``/version.reply`` response.
    """

    program_name: str
    major: int
    minor: int
    patch: str
    branch: str
    commit: str

    @classmethod
    def from_osc(cls, osc_message: OscMessage) -> "Response":
        program_name = cast(str, osc_message.contents[0])
        major = cast(int, osc_message.contents[1])
        minor = cast(int, osc_message.contents[2])
        patch = cast(str, osc_message.contents[3])
        branch = cast(str, osc_message.contents[4])
        commit = cast(str, osc_message.contents[5])
        return cls(program_name, major, minor, patch, branch, commit)
