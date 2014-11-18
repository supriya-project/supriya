# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Binding(SupriyaObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_source',
        '_target',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._source = None
        self._target = None

    ### SPECIAL METHODS ###

    def __call__(self, expr=None):
        self._source.handle_binding(expr)

    ### PUBLIC METHODS ###

    def bind(self, source, target):
        self.unbind()
        assert hasattr(source, '__binding_targets__')
        assert hasattr(target, '__binding_sources__')
        target.__bindings__.add(self)
        source.__bindings__.add(self)

    def unbind(self):
        if self._source is not None:
            self._source.__binding_targets__.remove(self)
        if self._target is not None:
            self._target.__binding_sources__.remove(self)
        self._source = None
        self._target = None

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target