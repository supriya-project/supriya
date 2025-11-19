from typing import Literal, TypeAlias

try:
    from enum import StrEnum
except ImportError:
    from backports.strenum import StrEnum  # type: ignore

Address: TypeAlias = str

ChannelCount: TypeAlias = Literal[1, 2, 4, 8]


class Entities(StrEnum):
    AUDIO_BUSES = "audio-buses"
    BUFFERS = "buffers"
    CONTROL_BUSES = "control-buses"
    NODES = "nodes"
    SYNTHDEFS = "synthdefs"


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
    CHAINS = "chains"
    CHANNEL_STRIP = "channel-strip"
    DEVICES = "devices"
    FEEDBACK = "feedback"
    GAIN = "gain"
    GROUP = "group"
    INPUT = "input"
    INPUT_LEVELS = "input-levels"
    LEVELS = "levels"
    MAIN = "main"
    MIX = "mix"
    OUTPUT = "output"
    OUTPUT_LEVELS = "output-levels"
    SIDECHAIN = "sidechain"
    SYNTH = "synth"
    SYNTHS = "synths"
    TRACKS = "tracks"


class PatchMode(StrEnum):
    SUM = "sum"
    MIX = "mix"
    REPLACE = "replace"
    IGNORE = "ignore"


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
