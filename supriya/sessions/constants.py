from typing import Literal, TypeAlias

try:
    from enum import StrEnum
except ImportError:
    from backports.strenum import StrEnum  # type: ignore

Address: TypeAlias = str

ChannelCount: TypeAlias = Literal[1, 2, 4, 8]


class IO(StrEnum):
    """
    What type of IO a connection between components is performing.
    """

    READ = "read"
    WRITE = "write"


class Names(StrEnum):
    """
    Standard names for component context artifacts.
    """

    ACTIVE = "active"
    AUDIO_BUSSES = "audio-buses"
    BUFFERS = "buffers"
    CHANNEL_STRIP = "channel-strip"
    CONTROL_BUSSES = "control-buses"
    DEVICES = "devices"
    FEEDBACK = "feedback"
    GAIN = "gain"
    GROUP = "group"
    INPUT = "input"
    INPUT_LEVELS = "input-levels"
    MAIN = "main"
    NODES = "nodes"
    OUTPUT = "output"
    OUTPUT_LEVELS = "output-levels"
    SYNTH = "synth"
    SYNTHDEFS = "synthdefs"
    TRACKS = "tracks"


class Reconciliation(StrEnum):
    """
    Types of component reconciliation.

    There are multiple types of ``DESTROY`` because the reconciliation needs to
    know if component destruction is happening against the root of a subtree,
    or an inner node or leaf, e.g. only the top-most group needs to get a
    ``[/n_set, <node-id>, gate, 0]`` message because the synthesis server will
    propagate that to child nodes server-side.
    """

    CREATE = "create"
    RECREATE = "recreate"
    MUTATE = "mutate"
    DESTROY = "destroy"
    DESTROY_SHALLOW = "destroy-shallow"
    DESTROY_ROOT = "destroy-root"
