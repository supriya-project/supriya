class DoNotPropagate(object):

    ### CLASS VARIABLES ###

    _stack = []

    ### SPECIAL METHODS ###

    def __enter__(self):
        self._stack.append(self)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._stack.pop()
