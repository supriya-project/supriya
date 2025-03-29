import dataclasses
from typing import Sequence, Union

from uqbar.objects import get_repr, new


@dataclasses.dataclass(frozen=True)
class Interval:
    """
    An interval (typically of time).

    ::

        >>> from supriya.utils import Interval
        >>> Interval(0, 10)
        Interval(start_offset=0.0, stop_offset=10.0)
    """

    start_offset: float = float("-inf")
    stop_offset: float = float("inf")

    def __post_init__(self):
        object.__setattr__(self, "start_offset", float(self.start_offset))
        object.__setattr__(self, "stop_offset", float(self.stop_offset))

    ### SPECIAL METHODS ###

    def __and__(self, interval: "Interval"):
        """
        Logical AND of two intervals:

        ::

            >>> from supriya.utils import Interval
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
        result = IntervalTree()
        if self.intersects(interval):
            new_interval = self.new(
                start_offset=max(self.start_offset, interval.start_offset),
                stop_offset=min(self.stop_offset, interval.stop_offset),
            )
            result.add(new_interval)
        return result

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

            >>> from supriya.utils import Interval
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

    def __sub__(self, interval: "Interval"):
        """
        Subtract ``interval`` from interval:

        ::

            >>> from supriya.utils import Interval
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

            >>> from supriya.utils import Interval
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

            >>> from supriya.utils import Interval
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

            >>> from supriya.utils import Interval
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

            >>> from supriya.utils import Interval
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

            >>> from supriya.utils import Interval
            >>> interval = Interval(0, 10)
            >>> for split_interval in interval.split(1, 3, 7):
            ...     split_interval
            ...
            Interval(start_offset=0.0, stop_offset=1.0)
            Interval(start_offset=1.0, stop_offset=3.0)
            Interval(start_offset=3.0, stop_offset=7.0)
            Interval(start_offset=7.0, stop_offset=10.0)
        """
        split_offsets = sorted(
            float(offset)
            for offset in offsets
            if self.start_offset < offset < self.stop_offset
        )
        result = IntervalTree()
        right_interval = self
        for offset in split_offsets:
            left_interval = new(right_interval, stop_offset=offset)
            right_interval = new(right_interval, start_offset=offset)
            result.add(left_interval)
        result.add(right_interval)
        return result

    def translate(self, translation: float, stop_translation: float | None = None):
        """
        Translate offsets by ``translation``, and optionally translate independently when specifying ``stop_translation``:

        ::

            >>> from supriya.utils import Interval
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
            start_offset=self.start_offset + start_translation,
            stop_offset=self.stop_offset + stop_translation,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        return self.size

    @property
    def size(self) -> float:
        return self.stop_offset - self.start_offset

    @property
    def wellformed(self) -> bool:
        return self.start_offset < self.stop_offset


@dataclasses.dataclass
class Moment:
    """
    A moment of intervals in a interval tree.
    """

    interval_tree: "IntervalTree"
    start_offset: float
    start_intervals: Sequence[Interval]
    stop_intervals: Sequence[Interval]
    overlap_intervals: Sequence[Interval]

    def __repr__(self):
        """
        Gets the repr of this moment.
        """
        return "<{}({} <<{}>>)>".format(
            type(self).__name__,
            str(self.start_offset),
            len(self.start_intervals) + len(self.overlap_intervals),
        )

    @property
    def next_moment(self):
        """
        Gets the next moment in this moment's interval collection.
        """
        # TODO: This doesn't take into account stop offsets
        tree = self.interval_tree
        if tree is None:
            return None
        start_offset = tree.get_start_offset_after(self.start_offset)
        if start_offset is None:
            return None
        return tree.get_moment_at(start_offset)

    @property
    def next_start_offset(self):
        """
        Gets the next moment start offset in this moment's interval tree.
        """
        tree = self.interval_tree
        if tree is None:
            return None
        start_offset = tree.get_start_offset_after(self.start_offset)
        return start_offset

    @property
    def previous_moment(self):
        """
        Gets the previous moment in this moment's interval collection.
        """
        # TODO: This doesn't take into account stop offsets
        tree = self.interval_tree
        if tree is None:
            return None
        start_offset = tree.get_start_offset_before(self.start_offset)
        if start_offset is None:
            return None
        return tree.get_moment_at(start_offset)

    @property
    def previous_start_offset(self):
        """
        Gets the previous moment start offset in this moment's interval tree.
        """
        tree = self.interval_tree
        if tree is None:
            return None
        start_offset = tree.get_start_offset_before(self.start_offset)
        return start_offset


class IntervalTree:
    """
    A mutable always-sorted collection of intervals.

    ::

        >>> from supriya.utils import Interval, IntervalTree
        >>> intervals = (
        ...     Interval(0, 3),
        ...     Interval(1, 3),
        ...     Interval(1, 2),
        ...     Interval(2, 5),
        ...     Interval(6, 9),
        ... )
        >>> interval_tree = IntervalTree(intervals)
    """

    def __init__(self, intervals=None, accelerated=True):
        self._driver = IntervalTreeDriver(intervals)
        self._accelerated = bool(accelerated)
        if not accelerated:
            return
        try:
            from ._intervals import IntervalTreeDriverEx

            self._driver = IntervalTreeDriverEx(intervals)
        except (ImportError, ModuleNotFoundError):
            pass

    def __and__(self, interval):
        new_intervals = []
        for current_interval in self[:]:
            result = current_interval & interval
            new_intervals.extend(result)
        self[:] = sorted(new_intervals)
        return self

    def __contains__(self, interval):
        """
        Is true if this interval tree contains `interval`. Otherwise false.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> intervals[0] in interval_tree
            True

        ::

            >>> Interval(-1, 100) in interval_tree
            False

        Returns boolean.
        """
        return interval in self._driver

    def __getitem__(self, item):
        """
        Gets interval at index `item`.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> interval_tree[-1]
            Interval(start_offset=6.0, stop_offset=9.0)

        ::

            >>> for interval in interval_tree[:3]:
            ...     interval
            ...
            Interval(start_offset=0.0, stop_offset=3.0)
            Interval(start_offset=1.0, stop_offset=2.0)
            Interval(start_offset=1.0, stop_offset=3.0)

        Returns interval or intervals.
        """
        return self._driver[item]

    def __getstate__(self):
        return self._accelerated, tuple(self)

    def __iter__(self):
        """
        Iterates intervals in this interval tree.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> for interval in interval_tree:
            ...     interval
            ...
            Interval(start_offset=0.0, stop_offset=3.0)
            Interval(start_offset=1.0, stop_offset=2.0)
            Interval(start_offset=1.0, stop_offset=3.0)
            Interval(start_offset=2.0, stop_offset=5.0)
            Interval(start_offset=6.0, stop_offset=9.0)

        Returns generator.
        """
        return iter(self._driver)

    def __len__(self):
        """
        Gets length of this interval tree.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> len(interval_tree)
            5

        Returns integer.
        """
        return len(self._driver)

    def __repr__(self) -> str:
        if not len(self):
            return get_repr(self, multiline=False)
        return get_repr(self, multiline=True)

    def __setitem__(self, i, new):
        """
        Sets intervals at index `i` to `new`.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> interval_tree[:3] = [Interval(100, 200)]

        Returns none.
        """
        if isinstance(i, int):
            self.remove(self[i])
            self.add(new)
        elif isinstance(i, slice):
            for interval in self[i]:
                self.remove(interval)
            self.update(new)
        else:
            message = "Indices must be ints or slices, got {}".format(i)
            raise TypeError(message)

    def __setstate__(self, state):
        accelerated, intervals = state
        self.__init__(intervals=intervals, accelerated=accelerated)

    def __sub__(self, interval):
        """
        Delete material that intersects `interval`:

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> interval_tree = IntervalTree(
            ...     [
            ...         Interval(0, 16),
            ...         Interval(5, 12),
            ...         Interval(-2, 8),
            ...     ]
            ... )

        ::

            >>> interval = Interval(5, 10)
            >>> result = interval_tree - interval

        ::

            >>> for interval in interval_tree:
            ...     interval
            ...
            Interval(start_offset=-2.0, stop_offset=5.0)
            Interval(start_offset=0.0, stop_offset=5.0)
            Interval(start_offset=10.0, stop_offset=12.0)
            Interval(start_offset=10.0, stop_offset=16.0)

        Operates in place and returns interval tree.
        """
        if not self._is_interval(interval):
            raise ValueError(interval)
        intersection = self.find_intersection(interval)
        to_update = []
        for intersecting_interval in intersection:
            self.remove(intersecting_interval)
            for x in intersecting_interval - interval:
                to_update.append(x)
        self.update(to_update)
        return self

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_interval(expr):
        if hasattr(expr, "start_offset") and hasattr(expr, "stop_offset"):
            return True
        return False

    ### PUBLIC METHODS ###

    def find_intersection(self, interval_or_offset):
        """
        Find intervals intersecting a interval or offset.

        .. container:: example

            Finds intervals overlapping `offset`.

            ::

                >>> from supriya.utils import Interval, IntervalTree
                >>> intervals = (
                ...     Interval(0, 3),
                ...     Interval(1, 3),
                ...     Interval(1, 2),
                ...     Interval(2, 5),
                ...     Interval(6, 9),
                ... )
                >>> interval_tree = IntervalTree(intervals)

            ::

                >>> for x in interval_tree.find_intersection(1.5):
                ...     x
                ...
                Interval(start_offset=0.0, stop_offset=3.0)
                Interval(start_offset=1.0, stop_offset=2.0)
                Interval(start_offset=1.0, stop_offset=3.0)

        .. container:: example

            Finds intervals overlapping `interval`.

            ::

                >>> intervals = (
                ...     Interval(0, 3),
                ...     Interval(1, 3),
                ...     Interval(1, 2),
                ...     Interval(2, 5),
                ...     Interval(6, 9),
                ... )
                >>> interval_tree = IntervalTree(intervals)

            ::

                >>> interval = Interval(2, 4)
                >>> for x in interval_tree.find_intersection(interval):
                ...     x
                ...
                Interval(start_offset=0.0, stop_offset=3.0)
                Interval(start_offset=1.0, stop_offset=3.0)
                Interval(start_offset=2.0, stop_offset=5.0)
        """
        if self._is_interval(interval_or_offset):
            return self._driver.find_intervals_intersecting_interval(interval_or_offset)
        return self._driver.find_intervals_intersecting_offset(interval_or_offset)

    def find_intervals_starting_at(self, offset):
        return self._driver.find_intervals_starting_at(offset)

    def find_intervals_stopping_at(self, offset):
        return self._driver.find_intervals_stopping_at(offset)

    def get_moment_at(self, offset):
        """
        Gets moment at `offset`.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> interval_tree.get_moment_at(1)
            <Moment(1 <<3>>)>

        ::

            >>> interval_tree.get_moment_at(6.5)
            <Moment(6.5 <<1>>)>
        """
        stop_intervals = self.find_intervals_stopping_at(offset)
        start_intervals, overlap_intervals = [], []
        for interval in self.find_intersection(offset):
            if interval.start_offset == offset:
                start_intervals.append(interval)
            else:
                overlap_intervals.append(interval)
        moment = Moment(
            interval_tree=self,
            overlap_intervals=overlap_intervals,
            start_intervals=start_intervals,
            start_offset=offset,
            stop_intervals=stop_intervals,
        )
        return moment

    def get_offset_after(self, offset):
        """
        Gets first start or stop offset after ``offset``, otherwise None.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> for i in range(-1, 11):
            ...     print(i, interval_tree.get_offset_after(i))
            ...
            -1 0.0
            0 1.0
            1 2.0
            2 3.0
            3 5.0
            4 5.0
            5 6.0
            6 9.0
            7 9.0
            8 9.0
            9 None
            10 None
        """
        return self._driver.get_offset_after(float(offset))

    def get_start_offset_after(self, offset):
        """
        Gets start offst in this interval tree after `offset`.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> interval_tree.get_start_offset_after(-1)
            0.0

        ::

            >>> interval_tree.get_start_offset_after(0)
            1.0

        ::

            >>> interval_tree.get_start_offset_after(1)
            2.0

        ::

            >>> interval_tree.get_start_offset_after(2)
            6.0

        ::

            >>> interval_tree.get_start_offset_after(6) is None
            True
        """
        return self._driver.get_start_offset_after(float(offset))

    def get_start_offset_before(self, offset):
        """
        Gets start offst in this interval tree before `offset`.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> interval_tree.get_start_offset_before(7)
            6.0

        ::

            >>> interval_tree.get_start_offset_before(6)
            2.0

        ::

            >>> interval_tree.get_start_offset_before(2)
            1.0

        ::

            >>> interval_tree.get_start_offset_before(1)
            0.0

        ::

            >>> interval_tree.get_start_offset_before(0) is None
            True
        """
        return self._driver.get_start_offset_before(float(offset))

    def index(self, interval):
        return self._driver.index(interval)

    def add(self, interval):
        self._driver.add(interval)

    def update(self, intervals):
        self._driver.update(intervals)

    def iterate_moments(self, reverse=False):
        """
        Iterates moments in this interval tree.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> for x in interval_tree.iterate_moments():
            ...     x
            ...
            <Moment(0.0 <<1>>)>
            <Moment(1.0 <<3>>)>
            <Moment(2.0 <<3>>)>
            <Moment(6.0 <<1>>)>

        ::

            >>> for x in interval_tree.iterate_moments(reverse=True):
            ...     x
            ...
            <Moment(6.0 <<1>>)>
            <Moment(2.0 <<3>>)>
            <Moment(1.0 <<3>>)>
            <Moment(0.0 <<1>>)>

        Returns generator.
        """

        if reverse:
            start_offset = self.latest_start_offset
            moment = self.get_moment_at(start_offset)
            yield moment
            moment = moment.previous_moment
            while moment is not None:
                yield moment
                moment = moment.previous_moment
        else:
            start_offset = self.earliest_start_offset
            moment = self.get_moment_at(start_offset)
            yield moment
            moment = moment.next_moment
            while moment is not None:
                yield moment
                moment = moment.next_moment

    def iterate_moments_nwise(self, n=3, reverse=False):
        """
        Iterates moments in this interval tree in groups of `n`.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> for x in interval_tree.iterate_moments_nwise(n=2):
            ...     x
            ...
            [<Moment(0.0 <<1>>)>, <Moment(1.0 <<3>>)>]
            [<Moment(1.0 <<3>>)>, <Moment(2.0 <<3>>)>]
            [<Moment(2.0 <<3>>)>, <Moment(6.0 <<1>>)>]

        ::

            >>> for x in interval_tree.iterate_moments_nwise(n=2, reverse=True):
            ...     x
            ...
            [<Moment(2.0 <<3>>)>, <Moment(6.0 <<1>>)>]
            [<Moment(1.0 <<3>>)>, <Moment(2.0 <<3>>)>]
            [<Moment(0.0 <<1>>)>, <Moment(1.0 <<3>>)>]

        Returns generator.
        """
        n = int(n)
        if n < 1:
            raise ValueError(n)
        if reverse:
            for moment in self.iterate_moments(reverse=True):
                moments = [moment]
                while len(moments) < n:
                    next_moment = moments[-1].next_moment
                    if next_moment is None:
                        break
                    moments.append(next_moment)
                if len(moments) == n:
                    yield moments
        else:
            for moment in self.iterate_moments():
                moments = [moment]
                while len(moments) < n:
                    previous_moment = moments[-1].previous_moment
                    if previous_moment is None:
                        break
                    moments.append(previous_moment)
                if len(moments) == n:
                    yield list(reversed(moments))

    def remove(self, interval):
        """
        Removes interval from this interval tree.

        ::

            >>> from supriya.utils import Interval, IntervalTree
            >>> intervals = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ... )
            >>> interval_tree = IntervalTree(intervals)

        ::

            >>> for interval in intervals[1:-1]:
            ...     interval_tree.remove(interval)
            ...

        ::

            >>> for interval in interval_tree:
            ...     interval
            ...
            Interval(start_offset=0.0, stop_offset=3.0)
            Interval(start_offset=6.0, stop_offset=9.0)
        """
        self._driver.remove(interval)

    ### PUBLIC PROPERTIES ###

    @property
    def all_offsets(self):
        offsets = set()
        for interval in self:
            offsets.add(interval.start_offset)
            offsets.add(interval.stop_offset)
        return tuple(sorted(offsets))

    @property
    def all_start_offsets(self):
        start_offsets = set()
        for interval in self:
            start_offsets.add(interval.start_offset)
        return tuple(sorted(start_offsets))

    @property
    def all_stop_offsets(self):
        stop_offsets = set()
        for interval in self:
            stop_offsets.add(interval.stop_offset)
        return tuple(sorted(stop_offsets))

    @property
    def earliest_start_offset(self):
        def recurse(node):
            if node.left_child is not None:
                return recurse(node.left_child)
            return node.start_offset

        if self._driver._root_node is not None:
            return recurse(self._driver._root_node)
        return float("-inf")

    @property
    def earliest_stop_offset(self):
        if self._driver._root_node is not None:
            return self._driver._root_node.stop_offset_low
        return float("inf")

    @property
    def intervals(self):
        return list(self)

    @property
    def latest_start_offset(self):
        def recurse(node):
            if node.right_child is not None:
                return recurse(node.right_child)
            return node.start_offset

        if self._driver._root_node is not None:
            return recurse(self._driver._root_node)
        return float("-inf")

    @property
    def latest_stop_offset(self):
        if self._driver._root_node is not None:
            return self._driver._root_node.stop_offset_high
        return float("inf")

    @property
    def start_offset(self):
        return self.earliest_start_offset

    @property
    def stop_offset(self):
        return self.latest_stop_offset


class _CInterval:
    def __init__(self, start_offset, stop_offset, original_interval):
        self.start_offset = float(start_offset)
        self.stop_offset = float(stop_offset)
        self.original_interval = original_interval

    def __eq__(self, cinterval):
        if not isinstance(cinterval, type(self)):
            raise ValueError(cinterval)
        if self.start_offset != cinterval.start_offset:
            return False
        if self.stop_offset != cinterval.stop_offset:
            return False
        if self.original_interval != cinterval.original_interval:
            return False
        return True

    def __ne__(self, cinterval):
        if not isinstance(cinterval, type(self)):
            raise ValueError(cinterval)
        return not self.__eq__(cinterval)

    def __lt__(self, cinterval):
        if not isinstance(cinterval, type(self)):
            raise ValueError(cinterval)
        if self.start_offset < cinterval.start_offset:
            return True
        if self.start_offset > cinterval.start_offset:
            return False
        if self.stop_offset < cinterval.stop_offset:
            return True
        return False

    @classmethod
    def from_interval(cls, interval):
        start_offset = float(interval.start_offset)
        stop_offset = float(interval.stop_offset)
        return cls(start_offset, stop_offset, interval)

    def intersects_interval(self, expr):
        return (
            expr.start_offset <= self.start_offset
            and self.start_offset < expr.stop_offset
        ) or (
            self.start_offset <= expr.start_offset
            and expr.start_offset < self.stop_offset
        )


class _CNode:
    def __init__(self, start_offset):
        self.balance = 0
        self.height = 0
        self.left_child = None
        self.node_start_index = -1
        self.node_stop_index = -1
        self.payload = []
        self.right_child = None
        self.start_offset = start_offset
        self.stop_offset_high = None
        self.stop_offset_low = None
        self.subtree_start_index = -1
        self.subtree_stop_index = -1


class IntervalTreeDriver:
    ### INITIALIZER ###

    def __init__(self, intervals=None):
        self._root_node = None
        self.update(intervals or [])

    ### SPECIAL METHODS ###

    def __contains__(self, interval):
        if not self._is_interval(interval):
            raise ValueError(interval)
        candidates = self.find_intervals_starting_at(interval.start_offset)
        result = interval in candidates
        return result

    def __getitem__(self, item):
        if isinstance(item, int):
            if self._root_node is None:
                raise IndexError
            if item < 0:
                item = self._root_node.subtree_stop_index + item
            if item < 0 or self._root_node.subtree_stop_index <= item:
                raise IndexError
            cinterval = self._recurse_getitem_by_index(self._root_node, item)
            return cinterval.original_interval
        elif isinstance(item, slice):
            if self._root_node is None:
                return []
            indices = item.indices(self._root_node.subtree_stop_index)
            start, stop = indices[0], indices[1]
            cintervals = self._recurse_getitem_by_slice(self._root_node, start, stop)
            return [cinterval.original_interval for cinterval in cintervals]
        raise TypeError("Indices must be integers or slices, got {}".format(item))

    def __iter__(self):
        stack = []
        current = self._root_node
        while True:
            while current is not None:
                stack.append(current)
                current = current.left_child
            if not stack:
                return
            current = stack.pop()
            for cinterval in current.payload:
                yield cinterval.original_interval
            while current.right_child is None and stack:
                current = stack.pop()
                for cinterval in current.payload:
                    yield cinterval.original_interval
            current = current.right_child

    def __len__(self):
        if self._root_node is None:
            return 0
        return self._root_node.subtree_stop_index

    ### PRIVATE METHODS ###

    def _get_node_cinterval(self, node):
        return Interval(
            start_offset=node.start_offset, stop_offset=node.stop_offset_high
        )

    def _insert_node(self, node, start_offset):
        if node is None:
            return _CNode(start_offset)
        if start_offset < node.start_offset:
            left_child = self._insert_node(node.left_child, start_offset)
            self._set_node_left_child(node, left_child)
        elif node.start_offset < start_offset:
            right_child = self._insert_node(node.right_child, start_offset)
            self._set_node_right_child(node, right_child)
        return self._rebalance(node)

    def _insert_interval(self, cinterval):
        self._root_node = self._insert_node(self._root_node, cinterval.start_offset)
        node = self._search(self._root_node, cinterval.start_offset)
        node.payload.append(cinterval)
        node.payload.sort(key=lambda x: x.stop_offset)

    @staticmethod
    def _is_interval(expr):
        if hasattr(expr, "start_offset") and hasattr(expr, "stop_offset"):
            return True
        return False

    def _remove_node(self, node, start_offset):
        if node is None:
            return None
        if node.start_offset == start_offset:
            if node.left_child and node.right_child:
                next_node = node.right_child
                while next_node.left_child:
                    next_node = next_node.left_child
                node.start_offset = next_node.start_offset
                node.payload = next_node.payload
                self._set_node_right_child(
                    node, self._remove_node(node.right_child, next_node.start_offset)
                )
            else:
                node = node.left_child or node.right_child
        elif start_offset < node.start_offset:
            left_child = self._remove_node(node.left_child, start_offset)
            self._set_node_left_child(node, left_child)
        elif node.start_offset < start_offset:
            self._set_node_right_child(
                node, self._remove_node(node.right_child, start_offset)
            )
        return self._rebalance(node)

    def _rebalance(self, node):
        if node is None:
            return None
        if 1 < node.balance:
            if 0 <= node.right_child.balance:
                node = self._rotate_right_right(node)
            else:
                node = self._rotate_right_left(node)
        elif node.balance < -1:
            if node.left_child.balance <= 0:
                node = self._rotate_left_left(node)
            else:
                node = self._rotate_left_right(node)
        return node

    def _recurse_find_intervals_intersecting_interval(self, node, cinterval):
        result = []
        if node is None:
            return result
        node_interval = self._get_node_cinterval(node)
        if cinterval.intersects_interval(node_interval):
            subresult = self._recurse_find_intervals_intersecting_interval(
                node.left_child, cinterval
            )
            result.extend(subresult)
            for candidate_interval in node.payload:
                if candidate_interval.intersects_interval(cinterval):
                    result.append(candidate_interval)
            subresult = self._recurse_find_intervals_intersecting_interval(
                node.right_child, cinterval
            )
            result.extend(subresult)
        elif (cinterval.start_offset <= node.start_offset) or (
            cinterval.stop_offset <= node.start_offset
        ):
            subresult = self._recurse_find_intervals_intersecting_interval(
                node.left_child, cinterval
            )
            result.extend(subresult)
        return result

    def _recurse_find_intervals_intersecting_offset(self, node, offset):
        result = []
        if node is None:
            return result
        if node.start_offset <= offset < node.stop_offset_high:
            subresult = self._recurse_find_intervals_intersecting_offset(
                node.left_child, offset
            )
            result.extend(subresult)
            for cinterval in node.payload:
                if offset < cinterval.stop_offset:
                    result.append(cinterval)
            subresult = self._recurse_find_intervals_intersecting_offset(
                node.right_child, offset
            )
            result.extend(subresult)
        elif offset <= node.start_offset:
            subresult = self._recurse_find_intervals_intersecting_offset(
                node.left_child, offset
            )
            result.extend(subresult)
        return result

    def _recurse_find_intervals_stopping_at(self, node, offset):
        result = []
        if node is None:
            return result
        if node.stop_offset_low <= offset <= node.stop_offset_high:
            for cinterval in node.payload:
                if cinterval.stop_offset == offset:
                    result.append(cinterval)
            if node.left_child is not None:
                result.extend(
                    self._recurse_find_intervals_stopping_at(node.left_child, offset)
                )
            if node.right_child is not None:
                result.extend(
                    self._recurse_find_intervals_stopping_at(node.right_child, offset)
                )
        return result

    def _recurse_get_start_offset_after(self, node, offset):
        if node is None:
            return None
        result = None
        if node.start_offset <= offset and node.right_child:
            result = self._recurse_get_start_offset_after(node.right_child, offset)
        elif offset < node.start_offset:
            result = (
                self._recurse_get_start_offset_after(node.left_child, offset) or node
            )
        return result

    def _recurse_get_start_offset_before(self, node, offset):
        if node is None:
            return None
        result = None
        if node.start_offset < offset:
            result = (
                self._recurse_get_start_offset_before(node.right_child, offset) or node
            )
        elif offset <= node.start_offset and node.left_child:
            result = self._recurse_get_start_offset_before(node.left_child, offset)
        return result

    def _recurse_getitem_by_index(self, node, index):
        if node.node_start_index <= index < node.node_stop_index:
            return node.payload[index - node.node_start_index]
        elif node.left_child is not None and index < node.node_start_index:
            return self._recurse_getitem_by_index(node.left_child, index)
        elif node.right_child is not None and node.node_stop_index <= index:
            return self._recurse_getitem_by_index(node.right_child, index)

    def _recurse_getitem_by_slice(self, node, start, stop):
        result = []
        if node is None:
            return result
        if start < node.node_start_index and node.left_child is not None:
            result.extend(self._recurse_getitem_by_slice(node.left_child, start, stop))
        if start < node.node_stop_index and node.node_start_index < stop:
            node_start = start - node.node_start_index
            if node_start < 0:
                node_start = 0
            node_stop = stop - node.node_start_index
            result.extend(node.payload[node_start:node_stop])
        if node.node_stop_index <= stop and node.right_child is not None:
            result.extend(self._recurse_getitem_by_slice(node.right_child, start, stop))
        return result

    def _remove_interval(self, cinterval, old_start_offset=None):
        if not isinstance(cinterval, _CInterval):
            raise ValueError(cinterval)
        start_offset = cinterval.start_offset
        if old_start_offset is not None:
            start_offset = old_start_offset
        node = self._search(self._root_node, start_offset)
        if node is None:
            return
        if cinterval in node.payload:
            node.payload.remove(cinterval)
        if not node.payload:
            self._root_node = self._remove_node(self._root_node, start_offset)

    def _rotate_left_left(self, node):
        next_node = node.left_child
        self._set_node_left_child(node, next_node.right_child)
        self._set_node_right_child(next_node, node)
        return next_node

    def _rotate_left_right(self, node):
        self._set_node_left_child(node, self._rotate_right_right(node.left_child))
        next_node = self._rotate_left_left(node)
        return next_node

    def _rotate_right_left(self, node):
        self._set_node_right_child(node, self._rotate_left_left(node.right_child))
        next_node = self._rotate_right_right(node)
        return next_node

    def _rotate_right_right(self, node):
        next_node = node.right_child
        self._set_node_right_child(node, next_node.left_child)
        self._set_node_left_child(next_node, node)
        return next_node

    def _search(self, node, start_offset):
        if node is None:
            return None
        if node.start_offset == start_offset:
            return node
        elif node.left_child and start_offset < node.start_offset:
            return self._search(node.left_child, start_offset)
        elif node.right_child and node.start_offset < start_offset:
            return self._search(node.right_child, start_offset)
        return None

    def _set_node_left_child(self, node, left_child):
        node.left_child = left_child
        self._update_node_height(node)

    def _set_node_right_child(self, node, right_child):
        node.right_child = right_child
        self._update_node_height(node)

    def _update_node_height(self, node):
        left_height = -1
        right_height = -1
        if node.left_child is not None:
            left_height = node.left_child.height
        if node.right_child is not None:
            right_height = node.right_child.height
        node.height = max(left_height, right_height) + 1
        node.balance = right_height - left_height
        return node.height

    def _update_indices(self, node, parent_stop_index):
        if node is None:
            return
        if node.left_child is not None:
            self._update_indices(node.left_child, parent_stop_index)
            node.node_start_index = node.left_child.subtree_stop_index
            node.subtree_start_index = node.left_child.subtree_start_index
        elif parent_stop_index == -1:
            node.node_start_index = 0
            node.subtree_start_index = 0
        else:
            node.node_start_index = parent_stop_index
            node.subtree_start_index = parent_stop_index
        node.node_stop_index = node.node_start_index + len(node.payload)
        node.subtree_stop_index = node.node_stop_index
        if node.right_child is not None:
            self._update_indices(node.right_child, node.node_stop_index)
            node.subtree_stop_index = node.right_child.subtree_stop_index

    def _update_offsets(self, node):
        if node is None:
            return
        stop_offset_low = min(x.stop_offset for x in node.payload)
        stop_offset_high = max(x.stop_offset for x in node.payload)
        if node.left_child:
            left_child = self._update_offsets(node.left_child)
            if left_child.stop_offset_low < stop_offset_low:
                stop_offset_low = left_child.stop_offset_low
            if stop_offset_high < left_child.stop_offset_high:
                stop_offset_high = left_child.stop_offset_high
        if node.right_child:
            right_child = self._update_offsets(node.right_child)
            if right_child.stop_offset_low < stop_offset_low:
                stop_offset_low = right_child.stop_offset_low
            if stop_offset_high < right_child.stop_offset_high:
                stop_offset_high = right_child.stop_offset_high
        node.stop_offset_low = stop_offset_low
        node.stop_offset_high = stop_offset_high
        return node

    ### PUBLIC METHODS ###

    def add(self, interval):
        if not self._is_interval(interval):
            # raise ValueError(interval)
            return
        cinterval = _CInterval.from_interval(interval)
        self._insert_interval(cinterval)
        self._update_indices(self._root_node, -1)
        self._update_offsets(self._root_node)

    def find_intervals_intersecting_offset(self, offset):
        offset = float(offset)
        cintervals = self._recurse_find_intervals_intersecting_offset(
            self._root_node, offset
        )
        cintervals.sort(key=lambda x: (x.start_offset, x.stop_offset))
        return [cinterval.original_interval for cinterval in cintervals]

    def find_intervals_intersecting_interval(self, interval):
        cinterval = _CInterval.from_interval(interval)
        cintervals = self._recurse_find_intervals_intersecting_interval(
            self._root_node, cinterval
        )
        cintervals.sort(key=lambda x: (x.start_offset, x.stop_offset))
        return [cinterval.original_interval for cinterval in cintervals]

    def find_intervals_starting_at(self, offset):
        results = []
        node = self._search(self._root_node, offset)
        if node is None:
            return results
        results.extend(cinterval.original_interval for cinterval in node.payload)
        return results

    def find_intervals_stopping_at(self, offset):
        cintervals = self._recurse_find_intervals_stopping_at(self._root_node, offset)
        cintervals.sort(key=lambda x: (x.start_offset, x.stop_offset))
        return [cinterval.original_interval for cinterval in cintervals]

    def get_start_offset_after(self, offset):
        node = self._recurse_get_start_offset_after(self._root_node, offset)
        if node is None:
            return None
        return node.start_offset

    def get_start_offset_before(self, offset):
        node = self._recurse_get_start_offset_before(self._root_node, offset)
        if node is None:
            return None
        return node.start_offset

    def index(self, interval):
        if not self._is_interval(interval):
            raise ValueError(interval)
        cinterval = _CInterval.from_interval(interval)
        node = self._search(self._root_node, cinterval.start_offset)
        if node is None:
            raise ValueError("{} not in interval tree.".format(interval))
        if cinterval not in node.payload:
            raise ValueError("{} not in interval tree.".format(interval))
        index = node.payload.index(cinterval) + node.node_start_index
        return index

    def remove(self, interval):
        if interval not in self:
            raise ValueError(interval)
        cinterval = _CInterval.from_interval(interval)
        self._remove_interval(cinterval)
        self._update_indices(self._root_node, -1)
        self._update_offsets(self._root_node)

    def update(self, intervals):
        # for interval in intervals:
        #     if not self._is_interval(interval):
        #         raise ValueError(interval)
        for interval in intervals:
            if not self._is_interval(interval):
                # raise ValueError(interval)
                continue
            cinterval = _CInterval.from_interval(interval)
            self._insert_interval(cinterval)
        self._update_indices(self._root_node, -1)
        self._update_offsets(self._root_node)
