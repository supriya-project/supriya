# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Binding(SupriyaObject):
    r'''A binding.

    ::

        >>> source = bindingtools.BindingSource()
        >>> target = bindingtools.BindingTarget()
        >>> binding = bind(source, target)
        >>> binding
        Binding()

    ::

        >>> source._send_bound_event('An event!')
        Received 'An event!' @ supriya.tools.bindingtools.BindingTarget()

    '''

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

    def __call__(self, event=None):
        self._target._receive_bound_event(event)

    ### PUBLIC METHODS ###

    def bind(self, source, target):
        self.unbind()
        assert hasattr(source, '_binding_targets')
        assert hasattr(target, '_binding_sources')
        target._binding_sources.add(self)
        source._binding_targets.add(self)
        self._target = target
        self._source = source

    def unbind(self):
        if self._source is not None:
            self._source._binding_targets.remove(self)
        if self._target is not None:
            self._target._binding_sources.remove(self)
        self._source = None
        self._target = None

    ### PUBLIC PROPERTIES ###

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target