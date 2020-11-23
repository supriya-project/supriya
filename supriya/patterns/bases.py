import abc
import collections
import inspect
import itertools
import re
import uuid
from typing import Dict, Generator, Iterator

import uqbar.objects
from uqbar.enums import IntEnumeration
from uqbar.objects import new

from supriya.system import SupriyaValueObject


class Event(SupriyaValueObject):
    """
    An abstract event.

    ::

        >>> supriya.patterns.NoteEvent(
        ...     amplitude=0.9,
        ...     duration=10.5,
        ...     frequency=443,
        ...     panning=0.75,
        ...     )
        NoteEvent(
            amplitude=0.9,
            delta=10.5,
            duration=10.5,
            frequency=443,
            panning=0.75,
            )

    """

    ### INITIALIZER ###

    def __init__(self, delta=None, **settings):
        self._delta = delta
        self._settings = {
            key: value
            for key, value in settings.items()
            if not (key.startswith("_") and value is None)
        }

    ### SPECIAL METHODS ###

    def __getitem__(self, item):
        return self._settings.__getitem__(item)

    ### PRIVATE METHODS ###

    def _expand(
        self, settings, synthdef, uuids, realtime=True, synth_parameters_only=False
    ):
        settings = settings.copy()
        for key, value in settings.items():
            if isinstance(value, uuid.UUID) and value in uuids:
                value = uuids[value]
                if isinstance(value, dict):
                    value = sorted(value)[0]
                if not isinstance(value, collections.Sequence):
                    value = [value]
                settings[key] = value
        maximum_length = 1
        unexpanded_settings = {}
        for key, value in settings.items():
            if isinstance(value, collections.Sequence):
                maximum_length = max(len(value), maximum_length)
                unexpanded_settings[key] = value
            else:
                unexpanded_settings[key] = [value]
        expanded_settings = []
        for i in range(maximum_length):
            settings = {}
            for key, value in unexpanded_settings.items():
                settings[key] = value[i % len(value)]
            expanded_settings.append(settings)
        if synth_parameters_only:
            for i, dictionary in enumerate(expanded_settings):
                expanded_settings[i] = {
                    key: value
                    for key, value in dictionary.items()
                    if key in synthdef.parameter_names
                }
        return expanded_settings

    @abc.abstractmethod
    def _perform_nonrealtime(self, session, uuids, offset):
        raise NotImplementedError

    @abc.abstractmethod
    def _perform_realtime(
        self, index=0, node_id_allocator=None, timestamp=0, uuids=None
    ):
        raise NotImplementedError

    ### PUBLIC METHODS ###

    def as_dict(self):
        _, _, kwargs = uqbar.objects.get_vars(self)
        return kwargs

    def get(self, item, default=None):
        return self._settings.get(item, default)

    ### PUBLIC PROPERTIES ###

    @property
    def delta(self):
        if self._delta is None:
            return self.get("duration")
        return self._delta

    @property
    def settings(self):
        return self._settings


class Pattern(SupriyaValueObject):
    """
    Pattern base class.
    """

    ### CLASS VARIABLES ###

    _rngs: Dict[int, Iterator[float]] = {}

    class PatternState(IntEnumeration):
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

            >>> pattern = supriya.patterns.Pseq([1, 2, 3])
            >>> expr = supriya.patterns.Pseq([0, 10])
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

            >>> pattern = supriya.patterns.Pseq([[1, [2, 3]], [[4, 5], 6, 7]])
            >>> expr = [10, [100, 1000]]
            >>> for x in (pattern + expr):
            ...     x
            ...
            [11, [102, 1003]]
            [[14, 15], [106, 1006], 17]

        """
        import supriya.patterns

        return supriya.patterns.Pbinop(self, "+", expr)

    def __div__(self, expr):
        import supriya.patterns

        return supriya.patterns.Pbinop(self, "/", expr)

    def __mul__(self, expr):
        import supriya.patterns

        return supriya.patterns.Pbinop(self, "*", expr)

    def __pow__(self, expr):
        import supriya.patterns

        return supriya.patterns.Pbinop(self, "**", expr)

    def __radd__(self, expr):
        import supriya.patterns

        return supriya.patterns.Pbinop(expr, "+", self)

    def __rdiv__(self, expr):
        import supriya.patterns

        return supriya.patterns.Pbinop(expr, "/", self)

    def __rmul__(self, expr):
        import supriya.patterns

        return supriya.patterns.Pbinop(expr, "*", self)

    def __rpow__(self, expr):
        import supriya.patterns

        return supriya.patterns.Pbinop(expr, "**", self)

    def __rsub__(self, expr):
        import supriya.patterns

        return supriya.patterns.Pbinop(expr, "-", self)

    def __sub__(self, expr):
        import supriya.patterns

        return supriya.patterns.Pbinop(self, "-", expr)

    def __iter__(self) -> Generator:
        import supriya.patterns

        should_stop = self.PatternState.CONTINUE
        state = self._setup_state()
        iterator = self._iterate(state)
        try:
            initial_expr = next(iterator)
            initial_expr = self._coerce_iterator_output_recursively(initial_expr, state)
        except StopIteration:
            return
        peripheral_starts, peripheral_stops = self._setup_peripherals(
            initial_expr, state
        )
        if peripheral_starts:
            peripheral_starts = supriya.patterns.CompositeEvent(
                delta=0.0, events=peripheral_starts
            )
            self._debug("PERIPHERAL_STARTS", peripheral_starts)
            should_stop = yield peripheral_starts
        if not should_stop:
            should_stop = yield initial_expr
            while True:
                try:
                    expr = iterator.send(should_stop)
                    expr = self._coerce_iterator_output_recursively(expr, state)
                    should_stop = yield expr
                except StopIteration:
                    break
        if peripheral_stops:
            peripheral_stops = supriya.patterns.CompositeEvent(
                delta=0.0, events=peripheral_stops, is_stop=True
            )
            self._debug("PERIPHERAL_STOPS", peripheral_stops)
            yield peripheral_stops

    ### PRIVATE METHODS ###

    def _coerce_iterator_output(self, expr, state=None):
        return expr

    def _coerce_iterator_output_recursively(self, expr, state=None):
        import supriya.patterns

        if isinstance(expr, supriya.patterns.CompositeEvent):
            coerced_events = [
                self._coerce_iterator_output(child_event, state=state)
                for child_event in expr.get("events") or ()
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
        print(
            "{}[{}] {}".format(
                (self._indent_level or 0) * "    ",
                self._name,
                " ".join(str(arg) for arg in args),
            )
        )

    @classmethod
    def _freeze_recursive(cls, value):
        if isinstance(value, str):
            return value
        elif isinstance(value, collections.Sequence) and not isinstance(value, Pattern):
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
        from supriya.patterns import Pseed, RandomNumberGenerator

        identifier = None
        try:
            frame = inspect.currentframe()
            while frame is not None:
                if (
                    isinstance(frame.f_locals.get("self"), Pseed)
                    and frame.f_code.co_name == "_iterate"
                ):
                    identifier = id(frame)
                    break
                frame = frame.f_back
        finally:
            del frame
        if identifier in cls._rngs:
            print("YES")
            rng = cls._rngs[identifier]
        else:
            print("NO")
            rng = RandomNumberGenerator.get_stdlib_rng()
        return rng

    @abc.abstractmethod
    def _iterate(self, state=None):
        raise NotImplementedError

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
        if not isinstance(one, collections.Sequence) and not isinstance(
            two, collections.Sequence
        ):
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
        import supriya.patterns

        namespaces = namespaces or {}
        class_name = dict_["type"]
        class_ = getattr(supriya.patterns, class_name)
        kwargs = {}
        for key, value in dict_.items():
            if key == "type":
                continue
            if isinstance(value, str) and re.match(r"\$\w+\.\w+", value):
                namespace, name = value.split(".")
                namespace = namespaces[namespace[1:]]
                value = namespace[name]
            elif isinstance(value, dict) and "type" in value:
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


class EventPattern(Pattern):

    ### SPECIAL METHODS ###

    def _coerce_iterator_output(self, expr, state=None):
        import supriya.patterns

        if not isinstance(expr, supriya.patterns.Event):
            expr = supriya.patterns.NoteEvent(**expr)
        if expr.get("uuid") is None:
            expr = new(expr, uuid=uuid.uuid4())
        return expr

    ### PUBLIC METHODS ###

    def play(self, clock=None, server=None):
        import supriya.patterns
        import supriya.realtime

        event_player = supriya.patterns.EventPlayer(
            self, clock=clock, server=server or supriya.realtime.Server.default()
        )
        event_player.start()
        return event_player

    def with_bus(self, calculation_rate="audio", channel_count=None, release_time=0.25):
        import supriya.patterns

        return supriya.patterns.Pbus(
            self,
            calculation_rate=calculation_rate,
            channel_count=channel_count,
            release_time=release_time,
        )

    def with_effect(self, synthdef, release_time=0.25, **settings):
        import supriya.patterns

        return supriya.patterns.Pfx(
            self, synthdef=synthdef, release_time=release_time, **settings
        )

    def with_group(self, release_time=0.25):
        import supriya.patterns

        return supriya.patterns.Pgroup(self, release_time=release_time)
