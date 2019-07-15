from typing import Optional, Union

from uqbar.objects import get_repr, new

from supriya.system import SupriyaValueObject


class Interval(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = ("_start", "_stop")

    ### INITIALIZER ###

    def __init__(self, start: float = float("-inf"), stop: float = float("inf")):
        start, stop = float(start), float(stop)
        assert start <= stop
        self._start = start
        self._stop = stop

    ### SPECIAL METHODS ###

    def __and__(self, interval: "Interval"):
        from .IntervalTree import IntervalTree

        result = IntervalTree()
        if self.intersects(interval):
            new_interval = self.new(
                start=max(self.start, interval.start),
                stop=min(self.stop, interval.stop),
            )
            result.add(new_interval)
        return result

    def __contains__(self, interval: "Interval"):
        pass

    def __ge__(self, expr: Union["Interval", float]):
        if isinstance(expr, Interval):
            if self.start > expr.start:
                return True
            return self.start == expr.start and self.stop >= expr.stop
        return self.start >= expr

    def __gt__(self, expr: Union["Interval", float]):
        if isinstance(expr, Interval):
            if self.start > expr.start:
                return True
            return self.start == expr.start and self.stop > expr.stop
        return self.start > expr

    def __le__(self, expr: Union["Interval", float]):
        if isinstance(expr, Interval):
            if self.start <= expr.start:
                return True
            return self.start == expr.start and self.stop <= expr.stop
        return self.start <= expr

    def __lt__(self, expr: Union["Interval", float]):
        if isinstance(expr, Interval):
            if self.start < expr.start:
                return True
            return self.start == expr.start and self.stop < expr.stop
        return self.start < expr

    def __or__(self, interval: "Interval"):
        from .IntervalTree import IntervalTree

        result = IntervalTree()
        if self.stop < interval.start or self.start > interval.stop:
            result.update([self, interval])
            return result
        new_interval = self.new(
            start=min(self.start, interval.start), stop=max(self.stop, interval.stop)
        )
        result.add(new_interval)
        return result

    def __repr__(self):
        return get_repr(self, multiline=False)

    def __sub__(self, interval: "Interval"):
        from .IntervalTree import IntervalTree

        result = IntervalTree()
        if self.start < interval.start:
            if self.stop <= interval.start:
                result.add(self)
            elif self.stop <= interval.stop:
                new_interval = self.new(stop=interval.start)
                result.add(new_interval)
            else:
                interval_one = self.new(stop=interval.start)
                interval_two = self.new(start=interval.stop)
                result.update([interval_one, interval_two])
        elif self.stop > interval.stop:
            new_interval = self.new(
                start=max(self.start, interval.stop), stop=self.stop
            )
            result.add(new_interval)
        return result

    def __xor__(self, interval: "Interval"):
        from .IntervalTree import IntervalTree

        result = IntervalTree()
        if self.stop <= interval.start or self.start >= interval.stop:
            result.update([self, interval])
            return result
        starts = sorted([self.start, interval.start])
        stops = sorted([self.stop, interval.stop])
        if starts[0] < starts[1]:
            result.add(self.new(start=starts[0], stop=starts[1]))
        if stops[0] < stops[1]:
            result.add(self.new(start=stops[0], stop=stops[1]))
        return result

    ### PUBLIC METHODS ###

    def intersects(self, expr: Union["Interval", float]) -> bool:
        if isinstance(expr, Interval):
            return (expr.start <= self.start and self.start < expr.stop) or (
                self.start <= expr.start and expr.start < self.stop
            )
        return self.start <= expr < self.stop

    def is_tangent_to(self, expr: Union["Interval", float]) -> bool:
        if isinstance(expr, Interval):
            return self.start == expr.stop or self.stop == expr.start
        return self.start == expr or self.stop == expr

    def new(self, start=None, stop=None, **kwargs):
        if start is not None:
            kwargs["start"] = start
        if stop is not None:
            kwargs["stop"] = stop
        return new(self, **kwargs)

    def split(self, *offsets):
        pass

    def translate(
        self, translation: float, *, stop_translation: Optional[float] = None
    ):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def size(self) -> float:
        return self._stop - self._start

    @property
    def start(self) -> float:
        return self._start

    @property
    def stop(self) -> float:
        return self._stop

    @property
    def wellformed(self) -> bool:
        return self._start_offset < self._stop_offset
