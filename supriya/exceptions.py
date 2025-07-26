"""
Exceptions.
"""


class AllocationError(Exception):
    pass


class ContextError(Exception):
    pass


class InvalidCalculationRate(ContextError):
    pass


class InvalidMoment(ContextError):
    pass


class MomentClosed(ContextError):
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
