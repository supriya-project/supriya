class ContextError(Exception):
    pass


class InvalidCalculationRate(ContextError):
    pass


class InvalidMoment(ContextError):
    pass


class MomentClosed(ContextError):
    pass
