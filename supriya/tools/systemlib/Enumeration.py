# -*- encoding: utf-8 -*-
import enum


class Enumeration(enum.IntEnum):

    ### PUBLIC METHODS ###

    @classmethod
    def from_expr(cls, expr):
        if isinstance(expr, cls):
            return expr
        elif isinstance(expr, int):
            return cls(expr)
        elif isinstance(expr, str):
            expr = expr.upper()
            expr = expr.strip()
            expr = expr.replace(' ', '_')
            return cls[expr]
        message = 'Cannot instantiate {} from {}.'.format(cls.__name__, expr)
        raise ValueError(message)
