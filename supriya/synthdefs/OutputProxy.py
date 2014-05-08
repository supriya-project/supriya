class OutputProxy(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_output_index',
        '_ugen',
        )

    ### INITIALIZER ###

    def __init__(self, ugen, output_index):
        self._ugen = ugen
        self._output_index = output_index

    ### PRIVATE METHODS ###

    def _get_ugen(self):
        return self._ugen

    def _get_output_number(self):
        return self._output_index

    ### PUBLIC PROPERTIES ###

    @property
    def ugen(self):
        return self._ugen

    @property
    def output_index(self):
        return self._output_index
