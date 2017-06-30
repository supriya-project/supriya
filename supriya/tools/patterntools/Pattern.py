import abc
import collections
import inspect
import itertools
import re
from abjad import new
from supriya.tools.systemtools import BindableNamespace
from supriya.tools.systemtools import Enumeration
from supriya.tools.systemtools import SupriyaValueObject


class Pattern(SupriyaValueObject):
    """
    Pattern base class.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    _rngs = {}

    class PatternState(Enumeration):
        CONTINUE = 0
        REALTIME_STOP = 1
        NONREALTIME_STOP = 2

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        """
        Adds `expr` to pattern.

        ::

            >>> pattern = patterntools.Pseq([1, 2, 3])
            >>> expr = patterntools.Pseq([0, 10])
            >>> list(pattern + expr)
            [1, 12]

        ::

            >>> expr = 10
            >>> list(pattern + expr)
            [11, 12, 13]

        ::

            >>> expr = [10, [100, 1000]]
            >>> list(pattern + expr)
            [[11, [101, 1001]], [12, [102, 1002]], [13, [103, 1003]]]

        ::

            >>> pattern = patterntools.Pseq([[1, [2, 3]], [[4, 5], 6, 7]])
            >>> expr = [10, [100, 1000]]
            >>> for x in (pattern + expr):
            ...     x
            ...
            [11, [102, 1003]]
            [[14, 15], [106, 1006], 17]

        """
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '+', expr)

    def __div__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '/', expr)

    def __mul__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '*', expr)

    def __pow__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '**', expr)

    def __radd__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '+', self)

    def __rdiv__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '/', self)

    def __rmul__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '*', self)

    def __rpow__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '**', self)

    def __rsub__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(expr, '-', self)

    def __sub__(self, expr):
        from supriya.tools import patterntools
        return patterntools.Pbinop(self, '-', expr)

    def __iter__(self):
        from supriya.tools import patterntools
        should_stop = self.PatternState.CONTINUE
        state = self._setup_state()
        iterator = self._iterate(state)
        try:
            initial_expr = next(iterator)
            initial_expr = self._coerce_iterator_output_recursively(
                initial_expr, state)
        except StopIteration:
            return
        peripheral_starts, peripheral_stops = self._setup_peripherals(
            initial_expr, state)
        if peripheral_starts:
            peripheral_starts = patterntools.CompositeEvent(
                delta=0.0,
                events=peripheral_starts,
                )
            self._debug('PERIPHERAL_STARTS', peripheral_starts)
            should_stop = yield peripheral_starts
        if not should_stop:
            should_stop = yield initial_expr
            while True:
                try:
                    expr = iterator.send(should_stop)
                    expr = self._coerce_iterator_output_recursively(
                        expr, state)
                    should_stop = yield expr
                except StopIteration:
                    break
        if peripheral_stops:
            peripheral_stops = patterntools.CompositeEvent(
                delta=0.0,
                events=peripheral_stops,
                is_stop=True,
                )
            self._debug('PERIPHERAL_STOPS', peripheral_stops)
            yield peripheral_stops

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, expr, state=None):
        return expr

    def _coerce_iterator_output_recursively(self, expr, state=None):
        from supriya.tools import patterntools
        if isinstance(expr, patterntools.CompositeEvent):
            coerced_events = [
                self._coerce_iterator_output(child_event, state=state)
                for child_event in expr.get('events') or ()
                ]
            expr = new(expr, events=coerced_events)
        else:
            expr = self._coerce_iterator_output(expr, state=state)
        return expr

    @classmethod
    def _coerce_floats(cls, value):
        if isinstance(value, collections.Sequence):
            value = tuple(float(_) for _ in value)
            assert value
        else:
            value = float(value)
        return value

    def _debug(self, *args):
        return
        if not self._name:
            return
        print('{}[{}] {}'.format(
            (self._indent_level or 0) * '    ',
            self._name,
            ' '.join(str(arg) for arg in args),
            ))

    @classmethod
    def _freeze_recursive(cls, value):
        if isinstance(value, str):
            return value
        elif (
            isinstance(value, collections.Sequence) and
            not isinstance(value, Pattern)
            ):
            return tuple(cls._freeze_recursive(_) for _ in value)
        return value

    @classmethod
    def _get_arity(cls, value):
        if isinstance(value, Pattern):
            return value.arity
        elif isinstance(value, collections.Sequence):
            return len(value)
        return 1

    @classmethod
    def _get_rng(cls):
        from supriya.tools.patterntools import Pseed, RandomNumberGenerator
        pseed_file_path = Pseed._file_path
        identifier = None
        try:
            frame = inspect.currentframe()
            while frame is not None:
                file_path = frame.f_code.co_filename
                function_name = frame.f_code.co_name
                if (
                    file_path == pseed_file_path and
                    function_name == '_iterate'
                    ):
                    identifier = id(frame)
                    break
                frame = frame.f_back
        finally:
            del(frame)
        if identifier in cls._rngs:
            rng = cls._rngs[identifier]
        else:
            rng = RandomNumberGenerator.get_stdlib_rng()
        return rng

    @classmethod
    def _loop(cls, repetitions=None):
        if repetitions is None:
            while True:
                yield True
        else:
            for _ in range(repetitions):
                yield True

    @classmethod
    def _process_recursive(cls, one, two, procedure):
        if not isinstance(one, collections.Sequence) and \
            not isinstance(two, collections.Sequence):
            return procedure(one, two)
        if not isinstance(one, collections.Sequence):
            one = [one]
        if not isinstance(two, collections.Sequence):
            two = [two]
        length = max(len(one), len(two))
        if len(one) < length:
            cycle = itertools.cycle(one)
            one = (next(cycle) for _ in range(length))
        if len(two) < length:
            cycle = itertools.cycle(two)
            two = (next(cycle) for _ in range(length))
        result = []
        for one, two in zip(one, two):
            result.append(cls._process_recursive(one, two, procedure))
        return result

    def _setup_state(self):
        return {}

    def _setup_peripherals(self, initial_expr, state):
        return None, None

    ### PUBLIC METHODS ###

    @classmethod
    def from_dict(cls, dict_, namespaces=None):
        from supriya.tools import patterntools
        namespaces = namespaces or {}
        class_name = dict_['type']
        class_ = getattr(patterntools, class_name)
        kwargs = {}
        for key, value in dict_.items():
            if key == 'type':
                continue
            if isinstance(value, str) and re.match('\$\w+\.\w+', value):
                namespace, name = value.split('.')
                namespace = namespaces[namespace[1:]]
                if isinstance(namespace, BindableNamespace):
                    value = namespace.proxies[name]
                else:
                    value = namespace[name]
            elif isinstance(value, dict) and 'type' in value:
                value = cls.from_dict(value, namespaces=namespaces)
            kwargs[key] = value
        return class_(**kwargs)

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def arity(self):
        raise NotImplementedError

    @abc.abstractproperty
    def is_infinite(self):
        raise NotImplementedError
