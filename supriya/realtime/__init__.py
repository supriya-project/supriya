"""
Tools for interacting with and modeling objects on the SuperCollider
``scsynth`` synthesis server.
"""
from .allocators import Block, BlockAllocator, NodeIdAllocator
from .bases import ServerObject
from .buffers import Buffer, BufferGroup, BufferProxy
from .buses import AudioInputBusGroup, AudioOutputBusGroup, Bus, BusGroup, BusProxy
from .interfaces import (
    ControlInterface,
    GroupControl,
    GroupInterface,
    SynthControl,
    SynthInterface,
)
from .meters import Meters
from .nodes import Group, Node, RootNode, Synth
from .recorder import Recorder
from .servers import AsyncServer, BaseServer, Server

__all__ = [
    "AudioInputBusGroup",
    "AudioOutputBusGroup",
    "AsyncServer",
    "BaseServer",
    "Block",
    "BlockAllocator",
    "Buffer",
    "BufferGroup",
    "BufferProxy",
    "Bus",
    "BusGroup",
    "BusProxy",
    "ControlInterface",
    "Group",
    "GroupControl",
    "GroupInterface",
    "Meters",
    "Node",
    "NodeIdAllocator",
    "Recorder",
    "RootNode",
    "Server",
    "ServerObject",
    "Synth",
    "SynthControl",
    "SynthInterface",
    "boot",
]
