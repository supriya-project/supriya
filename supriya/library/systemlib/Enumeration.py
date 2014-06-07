# -*- encoding: utf-8 -*-
import enum


class Enumeration(enum.IntEnum):

    ### PUBLIC METHODS ###

    @classmethod
    def new(cls, expr):
        if isinstance(expr, int):
            return cls(expr)
        elif isinstance(expr, str):
            expr = expr.upper()
            return cls[expr]
        message = 'Cannot instantiate {} from {}.'.format(cls.__name__, expr)
        raise ValueError(message)
