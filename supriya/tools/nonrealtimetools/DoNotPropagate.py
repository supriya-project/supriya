# -*- encoding: utf-8 -*-


class DoNotPropagate(object):
    """
    Context manager which prevents propagation of node hierarchy changes across
    states.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Session Internals'

    _stack = []

    ### SPECIAL METHODS ###

    def __enter__(self):
        self._stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._stack.pop()
