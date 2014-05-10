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
        from supriya import synthdefs
        if value is None:
            if self.default is None:
                raise Exception('no default value for argument {} in {}.'.format(
                    self.name, type(ugen).__name__))
            ugen._add_constant_input(self.default)
        elif isinstance(value, (int, float)):
            ugen._add_constant_input(value)
        elif isinstance(value, (synthdefs.OutputProxy, synthdefs.UGen)):
            ugen._add_ugen_input(
                value._get_source(),
                value._get_output_number(),
                )
        else:
            raise Exception(value)

    ### PUBLIC PROPERTIES ###

    @property
    def default(self):
        return self._default

    @property
    def name(self):
        return self._name
