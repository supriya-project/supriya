"""
Exceptions.
"""


class AlreadyAllocated(Exception):
    pass


class NotAllocated(Exception):
    pass


class BufferAlreadyAllocated(AlreadyAllocated):
    pass


class BufferNotAllocated(NotAllocated):
    pass


class BusAlreadyAllocated(AlreadyAllocated):
    pass


class BusNotAllocated(NotAllocated):
    pass


class IncompatibleRate(Exception):
    pass


class NodeAlreadyAllocated(AlreadyAllocated):
    pass


class NodeNotAllocated(NotAllocated):
    pass


class NonrealtimeOutputMissing(Exception):
    pass


class NonrealtimeRenderError(Exception):
    pass


class RequestTimeout(Exception):
    pass


class ServerCannotBoot(Exception):
    pass


class ServerOnline(Exception):
    pass


class ServerOffline(Exception):
    pass


class OwnedServerShutdown(Exception):
    pass


class UnownedServerShutdown(Exception):
    pass


class TooManyClients(Exception):
    pass
