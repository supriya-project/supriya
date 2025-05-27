import enum
from typing import Literal, TypeAlias

Address: TypeAlias = str

ChannelCount: TypeAlias = Literal[1, 2, 4, 8]


class IO(enum.StrEnum):
    READ = "read"
    WRITE = "write"


class Names(enum.StrEnum):
    ACTIVE = "active"
    AUDIO_BUSSES = "audio-busses"
    BUFFERS = "buffers"
    CHANNEL_STRIP = "channel-strip"
    CONTROL_BUSSES = "control-busses"
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


class Reconciliation(enum.StrEnum):
    CREATE = "create"
    DESTROY = "destroy"
    MUTATE = "mutate"
    RECREATE = "recreate"
