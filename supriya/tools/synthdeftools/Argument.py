# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Argument(SupriyaObject):

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
        from supriya import synthdeftools
        if value is None:
            if self.default is None:
                raise Exception('no default value for argument {} in {}.'.format(
                    self.name, type(ugen).__name__))
            ugen._add_constant_input(self.default)
        elif isinstance(value, (int, float)):
            ugen._add_constant_input(value)
        elif isinstance(value, (synthdeftools.OutputProxy, synthdeftools.UGen)):
            ugen._add_ugen_input(
                value._get_source(),
                value._get_output_number(),
                )
        elif isinstance(value, tuple) and \
            all(isinstance(_, (int, float)) for _ in value):
            assert ugen._unexpanded_argument_names
            assert self.name in ugen._unexpanded_argument_names
            for x in value:
                ugen._add_constant_input(x)
        else:
            raise Exception(value)

    ### PUBLIC PROPERTIES ###

    @property
    def default(self):
        return self._default

    @property
    def name(self):
        return self._name
