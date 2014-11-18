# -*- encoding: utf-8 -*-
from supriya.tools.systemtools.SupriyaObject import SupriyaObject


class Binding(SupriyaObject):
    r'''A binding.

    ::

        >>> source = bindingtools.BindingSource()
        >>> target = bindingtools.BindingTarget()

    ..  container:: example

        ::

            >>> binding = bind(source, target)
            >>> binding
            Binding()

        ::

            >>> source._send_bound_event('An event!')
            Received 'An event!' @ supriya.tools.bindingtools.BindingTarget()

        ::

            >>> binding.unbind()

    ..  container:: example

        ::

            >>> binding = bind(source, target, range_=(0., 127.))
            >>> for i in range(11):
            ...     source._send_bound_event(float(i) / 10.)
            ...
            Received 0.0 @ supriya.tools.bindingtools.BindingTarget()
            Received 12.7... @ supriya.tools.bindingtools.BindingTarget()
            Received 25.4... @ supriya.tools.bindingtools.BindingTarget()
            Received 38.1 @ supriya.tools.bindingtools.BindingTarget()
            Received 50.8... @ supriya.tools.bindingtools.BindingTarget()
            Received 63.5 @ supriya.tools.bindingtools.BindingTarget()
            Received 76.2 @ supriya.tools.bindingtools.BindingTarget()
            Received 88.899... @ supriya.tools.bindingtools.BindingTarget()
            Received 101.6... @ supriya.tools.bindingtools.BindingTarget()
            Received 114.3 @ supriya.tools.bindingtools.BindingTarget()
            Received 127.0 @ supriya.tools.bindingtools.BindingTarget()

        ::

            >>> binding.unbind()

    ..  container:: example

        ::

            >>> binding = bind(source, target, range_=(0., 127.), exponent=2.)
            >>> for i in range(11):
            ...     source._send_bound_event(float(i) / 10.)
            ...
            Received 0.0 @ supriya.tools.bindingtools.BindingTarget()
            Received 1.27... @ supriya.tools.bindingtools.BindingTarget()
            Received 5.08... @ supriya.tools.bindingtools.BindingTarget()
            Received 11.43 @ supriya.tools.bindingtools.BindingTarget()
            Received 20.32... @ supriya.tools.bindingtools.BindingTarget()
            Received 31.75 @ supriya.tools.bindingtools.BindingTarget()
            Received 45.72 @ supriya.tools.bindingtools.BindingTarget()
            Received 62.2299... @ supriya.tools.bindingtools.BindingTarget()
            Received 81.28... @ supriya.tools.bindingtools.BindingTarget()
            Received 102.87 @ supriya.tools.bindingtools.BindingTarget()
            Received 127.0 @ supriya.tools.bindingtools.BindingTarget()

        ::

            >>> binding.unbind()

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_input_range',
        '_output_range',
        '_exponent',
        '_source',
        '_target',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._exponent = None
        self._input_range = None
        self._output_range = None
        self._source = None
        self._target = None

    ### SPECIAL METHODS ###

    def __call__(self, event=None):
        from supriya.tools import synthdeftools
        if self._output_range is not None and self._input_range is not None:
            event = float(event)
            exponent = self._exponent
            if exponent is None:
                exponent = 1.0
            event = synthdeftools.Range.scale(
                event,
                self._input_range,
                self._output_range,
                exponent=exponent,
                )
        self._target._receive_bound_event(event)

    ### PUBLIC METHODS ###

    def bind(self, source, target, range_=None, exponent=None):
        from supriya.tools import synthdeftools
        self.unbind()
        assert hasattr(source, '_binding_targets')
        assert hasattr(target, '_binding_sources')
        target._binding_sources.add(self)
        source._binding_targets.add(self)
        self._target = target
        self._source = source
        input_range = None
        if hasattr(self._source, '_output_range'):
            input_range = self._source._output_range
        if input_range is not None:
            input_range = synthdeftools.Range(input_range)
        self._input_range = input_range
        if range_ is not None:
            range_ = synthdeftools.Range(range_)
        self._output_range = range_
        if exponent is not None:
            exponent = float(exponent)
        self._exponent = exponent

    def unbind(self):
        if self._source is not None:
            self._source._binding_targets.remove(self)
        if self._target is not None:
            self._target._binding_sources.remove(self)
        self._exponent = None
        self._input_range = None
        self._output_range = None
        self._source = None
        self._target = None

    ### PUBLIC PROPERTIES ###

    @property
    def exponent(self):
        return self._exponent

    @property
    def input_range(self):
        return self._input_range

    @property
    def output_range(self):
        return self._output_range

    @property
    def source(self):
        return self._source

    @property
    def target(self):
        return self._target