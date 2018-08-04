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


class ServerAddressInUse(Exception):
    pass


class ServerOffline(Exception):
    pass


class ServerTimeout(Exception):
    pass
