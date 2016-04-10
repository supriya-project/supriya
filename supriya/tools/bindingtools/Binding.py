# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Binding(SupriyaObject):
    r'''A binding.

    ::

        >>> source = bindingtools.BindingInput()
        >>> target = bindingtools.BindingOutput()

    ..  container:: example

        ::

            >>> binding = bind(source, target)
            >>> binding
            Binding()

        ::

            >>> source._send_bound_event('An event!')
            Received 'An event!' @ supriya.tools.bindingtools.BindingOutput()

        ::

            >>> binding.unbind()

    ..  container:: example

        ::

            >>> binding = bind(source, target, range_=(0., 127.))
            >>> for i in range(11):
            ...     source._send_bound_event(float(i) / 10.)
            ...
            Received 0.0 @ supriya.tools.bindingtools.BindingOutput()
            Received 12.7... @ supriya.tools.bindingtools.BindingOutput()
            Received 25.4... @ supriya.tools.bindingtools.BindingOutput()
            Received 38.1 @ supriya.tools.bindingtools.BindingOutput()
            Received 50.8... @ supriya.tools.bindingtools.BindingOutput()
            Received 63.5 @ supriya.tools.bindingtools.BindingOutput()
            Received 76.2 @ supriya.tools.bindingtools.BindingOutput()
            Received 88.899... @ supriya.tools.bindingtools.BindingOutput()
            Received 101.6... @ supriya.tools.bindingtools.BindingOutput()
            Received 114.3 @ supriya.tools.bindingtools.BindingOutput()
            Received 127.0 @ supriya.tools.bindingtools.BindingOutput()

        ::

            >>> binding.unbind()

    ..  container:: example

        ::

            >>> binding = bind(source, target, range_=(0., 127.), exponent=2.)
            >>> for i in range(11):
            ...     source._send_bound_event(float(i) / 10.)
            ...
            Received 0.0 @ supriya.tools.bindingtools.BindingOutput()
            Received 1.27... @ supriya.tools.bindingtools.BindingOutput()
            Received 5.08... @ supriya.tools.bindingtools.BindingOutput()
            Received 11.43 @ supriya.tools.bindingtools.BindingOutput()
            Received 20.32... @ supriya.tools.bindingtools.BindingOutput()
            Received 31.75 @ supriya.tools.bindingtools.BindingOutput()
            Received 45.72 @ supriya.tools.bindingtools.BindingOutput()
            Received 62.2299... @ supriya.tools.bindingtools.BindingOutput()
            Received 81.28... @ supriya.tools.bindingtools.BindingOutput()
            Received 102.87 @ supriya.tools.bindingtools.BindingOutput()
            Received 127.0 @ supriya.tools.bindingtools.BindingOutput()

        ::

            >>> binding.unbind()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_target_range',
        '_source_range',
        '_exponent',
        '_source',
        '_target',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._exponent = None
        self._source = None
        self._source_range = None
        self._target = None
        self._target_range = None

    ### SPECIAL METHODS ###

    def __call__(self, event=None):
        from supriya.tools import synthdeftools
        if self._source_range is not None and self._target_range is not None:
            event = float(event)
            exponent = self._exponent
            if exponent is None:
                exponent = 1.0
            event = synthdeftools.Range.scale(
                event,
                self._source_range,
                self._target_range,
                exponent=exponent,
                )
        self._target._receive_bound_event(event)

    ### PUBLIC METHODS ###

    def bind(
        self,
        source,
        target,
        source_range=None,
        target_range=None,
        exponent=None,
        ):
        from supriya.tools import synthdeftools
        self.unbind()
        assert hasattr(source, '_binding_targets')
        assert hasattr(target, '_binding_sources')
        target._binding_sources.add(self)
        source._binding_targets.add(self)
        self._target = target
        self._source = source
        source_range = source_range or getattr(self.source, '_range', None)
        if source_range is not None:
            source_range = synthdeftools.Range(source_range)
        self._source_range = source_range
        target_range = target_range or getattr(self.target, '_range', None)
        if target_range is not None:
            target_range = synthdeftools.Range(target_range)
        self._target_range = target_range
        if exponent is not None:
            exponent = float(exponent)
        self._exponent = exponent

    def unbind(self):
        if self._source is not None:
            self._source._binding_targets.remove(self)
        if self._target is not None:
            self._target._binding_sources.remove(self)
        self._exponent = None
        self._target_range = None
        self._source_range = None
        self._source = None
        self._target = None

    ### PUBLIC PROPERTIES ###

    @property
    def exponent(self):
        return self._exponent

    @property
    def source(self):
        return self._source

    @property
    def source_range(self):
        return self._source_range

    @property
    def target(self):
        return self._target

    @property
    def target_range(self):
        return self._target_range
