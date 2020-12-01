from typing import Optional, Union

from uqbar.objects import get_repr, new

from supriya.system import SupriyaValueObject


class Interval(SupriyaValueObject):
    """
    An interval (typically of time).

    ::

        >>> from supriya.intervals import Interval
        >>> Interval(0, 10)
        Interval(start_offset=0.0, stop_offset=10.0)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_start_offset", "_stop_offset")

    ### INITIALIZER ###

    def __init__(
        self, start_offset: float = float("-inf"), stop_offset: float = float("inf")
    ):
        if start_offset is None:
            start_offset = float("-inf")
        if stop_offset is None:
            stop_offset = float("inf")
        start_offset, stop_offset = float(start_offset), float(stop_offset)
        assert start_offset <= stop_offset
        self._start_offset = start_offset
        self._stop_offset = stop_offset

    ### SPECIAL METHODS ###

    def __and__(self, interval: "Interval"):
        """
        Logical AND of two intervals:

        ::

            >>> from supriya.intervals import Interval
            >>> interval_1 = Interval(0, 10)
            >>> interval_2 = Interval(5, 12)
            >>> interval_3 = Interval(-2, 2)
            >>> interval_4 = Interval(10, 20)

        ::

            >>> interval_1 & interval_2
            IntervalTree(
                intervals=[
                    Interval(start_offset=5.0, stop_offset=10.0),
                ],
            )

        ::

            >>> interval_1 & interval_3
            IntervalTree(
                intervals=[
                    Interval(start_offset=0.0, stop_offset=2.0),
                ],
            )

        ::

            >>> interval_1 & interval_4
            IntervalTree(intervals=[])

        ::

            >>> interval_2 & interval_3
            IntervalTree(intervals=[])

        ::

            >>> interval_2 & interval_4
            IntervalTree(
                intervals=[
                    Interval(start_offset=10.0, stop_offset=12.0),
                ],
            )

        ::

            >>> interval_3 & interval_4
            IntervalTree(intervals=[])

        """
        from .IntervalTree import IntervalTree

        result = IntervalTree()
        if self.intersects(interval):
            new_interval = self.new(
                start_offset=max(self.start_offset, interval.start_offset),
                stop_offset=min(self.stop_offset, interval.stop_offset),
            )
            result.add(new_interval)
        return result

    def __contains__(self, interval: "Interval"):
        pass

    def __ge__(self, expr: Union["Interval", float]):
        if isinstance(expr, Interval):
            if self.start_offset > expr.start_offset:
                return True
            return (
                self.start_offset == expr.start_offset
                and self.stop_offset >= expr.stop_offset
            )
        return self.start_offset >= expr

    def __gt__(self, expr: Union["Interval", float]):
        if isinstance(expr, Interval):
            if self.start_offset > expr.start_offset:
                return True
            return (
                self.start_offset == expr.start_offset
                and self.stop_offset > expr.stop_offset
            )
        return self.start_offset > expr

    def __le__(self, expr: Union["Interval", float]):
        if isinstance(expr, Interval):
            if self.start_offset <= expr.start_offset:
                return True
            return (
                self.start_offset == expr.start_offset
                and self.stop_offset <= expr.stop_offset
            )
        return self.start_offset <= expr

    def __lt__(self, expr: Union["Interval", float]):
        if isinstance(expr, Interval):
            if self.start_offset < expr.start_offset:
                return True
            return (
                self.start_offset == expr.start_offset
                and self.stop_offset < expr.stop_offset
            )
        return self.start_offset < expr

    def __or__(self, interval: "Interval"):
        """
        Logical OR of two intervals:

        ::

            >>> from supriya.intervals import Interval
            >>> interval_1 = Interval(0, 10)
            >>> interval_2 = Interval(5, 12)
            >>> interval_3 = Interval(-2, 2)
            >>> interval_4 = Interval(10, 20)

        ::

            >>> interval_1 | interval_2
            IntervalTree(
                intervals=[
                    Interval(start_offset=0.0, stop_offset=12.0),
                ],
            )

        ::

            >>> interval_1 | interval_3
            IntervalTree(
                intervals=[
                    Interval(start_offset=-2.0, stop_offset=10.0),
                ],
            )

        ::

            >>> interval_1 | interval_4
            IntervalTree(
                intervals=[
                    Interval(start_offset=0.0, stop_offset=20.0),
                ],
            )

        ::

            >>> interval_2 | interval_3
            IntervalTree(
                intervals=[
                    Interval(start_offset=-2.0, stop_offset=2.0),
                    Interval(start_offset=5.0, stop_offset=12.0),
                ],
            )

        ::

            >>> interval_2 | interval_4
            IntervalTree(
                intervals=[
                    Interval(start_offset=5.0, stop_offset=20.0),
                ],
            )

        ::

            >>> interval_3 | interval_4
            IntervalTree(
                intervals=[
                    Interval(start_offset=-2.0, stop_offset=2.0),
                    Interval(start_offset=10.0, stop_offset=20.0),
                ],
            )

        """
        from .IntervalTree import IntervalTree

        result = IntervalTree()
        if (
            self.stop_offset < interval.start_offset
            or self.start_offset > interval.stop_offset
        ):
            result.update([self, interval])
            return result
        new_interval = self.new(
            start_offset=min(self.start_offset, interval.start_offset),
            stop_offset=max(self.stop_offset, interval.stop_offset),
        )
        result.add(new_interval)
        return result

    def __repr__(self):
        return get_repr(self, multiline=False)

    def __sub__(self, interval: "Interval"):
        """
        Subtract ``interval`` from interval:

        ::

            >>> from supriya.intervals import Interval
            >>> interval_1 = Interval(0, 10)
            >>> interval_2 = Interval(5, 12)
            >>> interval_3 = Interval(8, 11)
            >>> interval_4 = Interval(10, 20)

        ::

            >>> interval_1 - interval_1
            IntervalTree(intervals=[])

        ::

            >>> interval_1 - interval_2
            IntervalTree(
                intervals=[
                    Interval(start_offset=0.0, stop_offset=5.0),
                ],
            )

        ::

            >>> interval_1 - interval_3
            IntervalTree(
                intervals=[
                    Interval(start_offset=0.0, stop_offset=8.0),
                ],
            )

        ::

            >>> interval_1 - interval_4
            IntervalTree(
                intervals=[
                    Interval(start_offset=0.0, stop_offset=10.0),
                ],
            )

        ::

            >>> interval_2 - interval_1
            IntervalTree(
                intervals=[
                    Interval(start_offset=10.0, stop_offset=12.0),
                ],
            )

        ::

            >>> interval_2 - interval_2
            IntervalTree(intervals=[])

        ::

            >>> interval_2 - interval_3
            IntervalTree(
                intervals=[
                    Interval(start_offset=5.0, stop_offset=8.0),
                    Interval(start_offset=11.0, stop_offset=12.0),
                ],
            )

        ::

            >>> interval_2 - interval_4
            IntervalTree(
                intervals=[
                    Interval(start_offset=5.0, stop_offset=10.0),
                ],
            )

        ::

            >>> interval_3 - interval_1
            IntervalTree(
                intervals=[
                    Interval(start_offset=10.0, stop_offset=11.0),
                ],
            )

        ::

            >>> interval_3 - interval_2
            IntervalTree(intervals=[])

        ::

            >>> interval_3 - interval_3
            IntervalTree(intervals=[])

        ::

            >>> interval_3 - interval_4
            IntervalTree(
                intervals=[
                    Interval(start_offset=8.0, stop_offset=10.0),
                ],
            )

        ::

            >>> interval_4 - interval_1
            IntervalTree(
                intervals=[
                    Interval(start_offset=10.0, stop_offset=20.0),
                ],
            )

        ::

            >>> interval_4 - interval_2
            IntervalTree(
                intervals=[
                    Interval(start_offset=12.0, stop_offset=20.0),
                ],
            )

        ::

            >>> interval_4 - interval_3
            IntervalTree(
                intervals=[
                    Interval(start_offset=11.0, stop_offset=20.0),
                ],
            )

        ::

            >>> interval_4 - interval_4
            IntervalTree(intervals=[])

        """
        from .IntervalTree import IntervalTree

        result = IntervalTree()
        if self.start_offset < interval.start_offset:
            if self.stop_offset <= interval.start_offset:
                result.add(self)
            elif self.stop_offset <= interval.stop_offset:
                new_interval = self.new(stop_offset=interval.start_offset)
                result.add(new_interval)
            else:
                interval_one = self.new(stop_offset=interval.start_offset)
                interval_two = self.new(start_offset=interval.stop_offset)
                result.update([interval_one, interval_two])
        elif self.stop_offset > interval.stop_offset:
            new_interval = self.new(
                start_offset=max(self.start_offset, interval.stop_offset),
                stop_offset=self.stop_offset,
            )
            result.add(new_interval)
        return result

    def __xor__(self, interval: "Interval"):
        """
        Logical XOR of two intervals:

        ::

            >>> from supriya.intervals import Interval
            >>> interval_1 = Interval(0, 10)
            >>> interval_2 = Interval(5, 12)
            >>> interval_3 = Interval(-2, 2)
            >>> interval_4 = Interval(10, 20)

        ::

            >>> interval_1 ^ interval_2
            IntervalTree(
                intervals=[
                    Interval(start_offset=0.0, stop_offset=5.0),
                    Interval(start_offset=10.0, stop_offset=12.0),
                ],
            )

        ::

            >>> interval_1 ^ interval_3
            IntervalTree(
                intervals=[
                    Interval(start_offset=-2.0, stop_offset=0.0),
                    Interval(start_offset=2.0, stop_offset=10.0),
                ],
            )

        ::

            >>> interval_1 ^ interval_4
            IntervalTree(
                intervals=[
                    Interval(start_offset=0.0, stop_offset=10.0),
                    Interval(start_offset=10.0, stop_offset=20.0),
                ],
            )

        ::

            >>> interval_2 ^ interval_3
            IntervalTree(
                intervals=[
                    Interval(start_offset=-2.0, stop_offset=2.0),
                    Interval(start_offset=5.0, stop_offset=12.0),
                ],
            )

        ::

            >>> interval_2 ^ interval_4
            IntervalTree(
                intervals=[
                    Interval(start_offset=5.0, stop_offset=10.0),
                    Interval(start_offset=12.0, stop_offset=20.0),
                ],
            )

        ::

            >>> interval_3 ^ interval_4
            IntervalTree(
                intervals=[
                    Interval(start_offset=-2.0, stop_offset=2.0),
                    Interval(start_offset=10.0, stop_offset=20.0),
                ],
            )

        """
        from .IntervalTree import IntervalTree

        result = IntervalTree()
        if (
            self.stop_offset <= interval.start_offset
            or self.start_offset >= interval.stop_offset
        ):
            result.update([self, interval])
            return result
        starts = sorted([self.start_offset, interval.start_offset])
        stops = sorted([self.stop_offset, interval.stop_offset])
        if starts[0] < starts[1]:
            result.add(self.new(start_offset=starts[0], stop_offset=starts[1]))
        if stops[0] < stops[1]:
            result.add(self.new(start_offset=stops[0], stop_offset=stops[1]))
        return result

    ### PUBLIC METHODS ###

    def intersects(self, expr: Union["Interval", float]) -> bool:
        """
        True when interval intersects ``expr``, another interval or offset:

        ::

            >>> from supriya.intervals import Interval
            >>> interval_1 = Interval(0, 10)
            >>> interval_2 = Interval(5, 15)
            >>> interval_3 = Interval(10, 15)
            >>> interval_4 = Interval(15, 25)

        ::

            >>> interval_1.intersects(interval_1)
            True
            >>> interval_1.intersects(interval_2)
            True
            >>> interval_1.intersects(interval_3)
            False
            >>> interval_1.intersects(interval_4)
            False

        ::

            >>> for offset in [-5, 0, 5, 10, 15]:
            ...     print(offset, interval_1.intersects(offset))
            ...
            -5 False
            0 True
            5 True
            10 False
            15 False

        """
        if isinstance(expr, Interval):
            return (
                expr.start_offset <= self.start_offset
                and self.start_offset < expr.stop_offset
            ) or (
                self.start_offset <= expr.start_offset
                and expr.start_offset < self.stop_offset
            )
        return self.start_offset <= expr < self.stop_offset

    def is_tangent_to(self, expr: Union["Interval", float]) -> bool:
        """
        True when interval is tangent to ``expr``, another interval or offset:

        ::

            >>> from supriya.intervals import Interval
            >>> interval_1 = Interval(0, 10)
            >>> interval_2 = Interval(5, 15)
            >>> interval_3 = Interval(10, 15)
            >>> interval_4 = Interval(15, 25)

        ::

            >>> interval_1.is_tangent_to(interval_1)
            False
            >>> interval_1.is_tangent_to(interval_2)
            False
            >>> interval_1.is_tangent_to(interval_3)
            True
            >>> interval_1.is_tangent_to(interval_4)
            False

        ::

            >>> for offset in [-5, 0, 5, 10, 15]:
            ...     print(offset, interval_1.is_tangent_to(offset))
            ...
            -5 False
            0 True
            5 False
            10 True
            15 False

        """
        if isinstance(expr, Interval):
            return (
                self.start_offset == expr.stop_offset
                or self.stop_offset == expr.start_offset
            )
        return self.start_offset == expr or self.stop_offset == expr

    def new(self, start_offset=None, stop_offset=None, **kwargs):
        """
        Template a new interval:

        ::

            >>> from supriya.intervals import Interval
            >>> interval_one = Interval(0, 10)

            >>> interval_two = interval_one.new()
            >>> interval_two
            Interval(start_offset=0.0, stop_offset=10.0)
            >>> interval_two is not interval_one
            True

        ::

            >>> interval_two.new(start_offset=5.0)
            Interval(start_offset=5.0, stop_offset=10.0)

        """
        if start_offset is not None:
            kwargs["start_offset"] = start_offset
        if stop_offset is not None:
            kwargs["stop_offset"] = stop_offset
        return new(self, **kwargs)

    def split(self, *offsets):
        """
        Split at ``offsets``:

        ::

            >>> from supriya.intervals import Interval
            >>> interval = Interval(0, 10)
            >>> for split_interval in interval.split(1, 3, 7):
            ...     split_interval
            ...
            Interval(start_offset=0.0, stop_offset=1.0)
            Interval(start_offset=1.0, stop_offset=3.0)
            Interval(start_offset=3.0, stop_offset=7.0)
            Interval(start_offset=7.0, stop_offset=10.0)

        """
        from .IntervalTree import IntervalTree

        split_offsets = sorted(
            float(offset)
            for offset in offsets
            if self._start_offset < offset < self._stop_offset
        )
        result = IntervalTree()
        right_interval = self
        for offset in split_offsets:
            left_interval = new(right_interval, stop_offset=offset)
            right_interval = new(right_interval, start_offset=offset)
            result.add(left_interval)
        result.add(right_interval)
        return result

    def translate(self, translation: float, stop_translation: Optional[float] = None):
        """
        Translate offsets by ``translation``, and optionally translate independently when
        specifying ``stop_translation``:

        ::

            >>> from supriya.intervals import Interval
            >>> interval = Interval(0, 10)

        ::

            >>> interval.translate(5)
            Interval(start_offset=5.0, stop_offset=15.0)

        ::

            >>> interval.translate(5, 7.5)
            Interval(start_offset=5.0, stop_offset=17.5)

        """

        start_translation = float(translation)
        stop_translation = (
            float(stop_translation)
            if stop_translation is not None
            else start_translation
        )
        return self.new(
            start_offset=self._start_offset + start_translation,
            stop_offset=self._stop_offset + stop_translation,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return self.size

    @property
    def size(self) -> float:
        return self._stop_offset - self._start_offset

    @property
    def start_offset(self) -> float:
        return self._start_offset

    @property
    def stop_offset(self) -> float:
        return self._stop_offset

    @property
    def wellformed(self) -> bool:
        return self._start_offset < self._stop_offset
