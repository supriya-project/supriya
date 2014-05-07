class ArgumentSpecification(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default',
        '_name',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        name,
        default=None,
        ):
        self._default = default
        self._name = name

    ### PUBLIC METHODS ###

    def configure(self, ugen, value):
        if value is None:
            if self.default is None:
                raise Exception('no default value for argspec', self)
            ugen._add_constant_input(self.default)
        elif type(value) == float or type(value) == int:
            ugen._add_constant_input(value)
        else:
            ugen._add_ugen_input(
                value._get_ugen(),
                value._get_output_number(),
                )

    ### PUBLIC PROPERTIES ###

    @property
    def default(self):
        return self._default

    @property
    def name(self):
        return self._name
