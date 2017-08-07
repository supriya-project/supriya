import inspect


def get_object_signature(expr):
    if hasattr(expr, '__init__'):
        return inspect.signature(expr.__init__)
    elif hasattr(expr, '__new__'):
        return inspect.signature(expr.__new__)
    raise TypeError(type(expr))
