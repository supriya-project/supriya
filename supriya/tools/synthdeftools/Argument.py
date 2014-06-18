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
        ugen._configure_argument(self.name, value)

    ### PUBLIC PROPERTIES ###

    @property
    def default(self):
        return self._default

    @property
    def name(self):
        return self._name
