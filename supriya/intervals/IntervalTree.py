from uqbar.objects import get_repr

from supriya.system import SupriyaObject

from .IntervalTreeDriver import IntervalTreeDriver
from .Moment import Moment


class IntervalTree(SupriyaObject):
    """
    A mutable always-sorted collection of intervals.

    ::

        >>> from supriya.intervals import Interval, IntervalTree
        >>> intervals = (
        ...     Interval(0, 3),
        ...     Interval(1, 3),
        ...     Interval(1, 2),
        ...     Interval(2, 5),
        ...     Interval(6, 9),
        ... )
        >>> interval_tree = IntervalTree(intervals)

    """

    ### INITIALIZER ###

    # TODO: Protect datastructure with a R/W lock: https://pypi.org/project/readerwriterlock/

    def __init__(self, intervals=None, accelerated=True):
        self._driver = IntervalTreeDriver(intervals)
        self._accelerated = bool(accelerated)
        if not accelerated:
            return
        try:
            import pyximport  # noqa

            from .IntervalTreeDriverEx import IntervalTreeDriverEx

            self._driver = IntervalTreeDriverEx(intervals)
        except (ImportError, ModuleNotFoundError):
            pass

    ### SPECIAL METHODS ###

    def __and__(self, interval):
        new_intervals = []
        for current_interval in self[:]:
            result = current_interval & interval
            new_intervals.extend(result)
        self[:] = sorted(new_intervals)
        return self

    def __contains__(self, interval):
        """
        Is true if this interval tree contains `interval`. Otherwise
        false.

        ::

            >>> from supriya.intervals import Interval, IntervalTree
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

            >>> from supriya.intervals import Interval, IntervalTree
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

            >>> from supriya.intervals import Interval, IntervalTree
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

            >>> from supriya.intervals import Interval, IntervalTree
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

    def __repr__(self):
        if not len(self):
            return get_repr(self, multiline=False)
        return get_repr(self, multiline=True)

    def __setitem__(self, i, new):
        """
        Sets intervals at index `i` to `new`.

        ::

            >>> from supriya.intervals import Interval, IntervalTree
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

            >>> from supriya.intervals import Interval, IntervalTree
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

        ..  container:: example

            Finds intervals overlapping `offset`.

            ::

                >>> from supriya.intervals import Interval, IntervalTree
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

        ..  container:: example

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

            >>> from supriya.intervals import Interval, IntervalTree
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

            >>> from supriya.intervals import Interval, IntervalTree
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

            >>> from supriya.intervals import Interval, IntervalTree
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

            >>> from supriya.intervals import Interval, IntervalTree
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

            >>> from supriya.intervals import Interval, IntervalTree
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
        Iterates moments in this interval tree in groups of
        `n`.

        ::

            >>> from supriya.intervals import Interval, IntervalTree
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
        assert 0 < n
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

            >>> from supriya.intervals import Interval, IntervalTree
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

    ### PRIVATE PROPERTIES ###

    @property
    def _root_node(self):
        return self._driver._root_node

    @_root_node.setter
    def _root_node(self, node):
        self._driver._root_node = node

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

        if self._root_node is not None:
            return recurse(self._root_node)
        return float("-inf")

    @property
    def earliest_stop_offset(self):
        if self._root_node is not None:
            return self._root_node.stop_offset_low
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

        if self._root_node is not None:
            return recurse(self._root_node)
        return float("-inf")

    @property
    def latest_stop_offset(self):
        if self._root_node is not None:
            return self._root_node.stop_offset_high
        return float("inf")

    @property
    def start_offset(self):
        return self.earliest_start_offset

    @property
    def stop_offset(self):
        return self.latest_stop_offset
