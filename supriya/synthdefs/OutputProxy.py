class OutputProxy(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_index',
        '_ugen',
        )

    ### INITIALIZER ###

    def __init__(self, ugen, index):
        self._ugen = ugen
        self._index = index

    ### PRIVATE METHODS ###

    def _get_ugen(self):
        return self._ugen

    def _get_output_number(self):
        return self._index

    ### PUBLIC PROPERTIES ###

    @property
    def ugen(self):
        return self._ugen

    @property
    def index(self):
        return self._index
