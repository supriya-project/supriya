# -*- encoding: utf-8 -*-
import operator
from supriya.tools.patterntools.Pattern import Pattern


class Pbinop(Pattern):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_expr_one',
        '_expr_two',
        '_operator',
        )

    ### INITIALIZER ###

    def __init__(self, expr_one, operator, expr_two):
        self._expr_one = self._freeze_recursive(expr_one)
        self._expr_two = self._freeze_recursive(expr_two)
        self._operator = operator

    ### PRIVATE METHODS ###

    def _iterate(self, state=None):
        from supriya.tools import patterntools
        expr_one = self.expr_one
        if not isinstance(expr_one, Pattern):
            expr_one = patterntools.Pseq([expr_one], None)
        expr_one = iter(expr_one)
        expr_two = self.expr_two
        if not isinstance(expr_two, Pattern):
            expr_two = patterntools.Pseq([expr_two], None)
        expr_two = iter(expr_two)
        operator = self._string_to_operator()
        for one, two in zip(expr_one, expr_two):
            yield self._process_recursive(one, two, operator)

    def _string_to_operator(self):
        operators = {
            '+': operator.__add__,
            '-': operator.__sub__,
            '*': operator.__mul__,
            '/': operator.__truediv__,
            '//': operator.__floordiv__,
        }
        return operators[self.operator]

    ### PUBLIC PROPERTIES ###

    @property
    def arity(self):
        return max(self._get_arity(x) for x in (
            self._expr_one, self._expr_two))

    @property
    def expr_one(self):
        return self._expr_one

    @property
    def expr_two(self):
        return self._expr_two

    @property
    def is_infinite(self):
        from supriya.tools import patterntools
        return (
            isinstance(self.expr_one, patterntools.Pattern) and
            isinstance(self.expr_two, patterntools.Pattern) and
            self.expr_one.is_infinite and
            self.expr_two.is_infinite
            )

    @property
    def operator(self):
        return self._operator
