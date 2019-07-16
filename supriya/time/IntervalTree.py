from uqbar.objects import get_repr

from supriya.system.SupriyaObject import SupriyaObject
from .Moment import Moment
from .IntervalTreeDriver import IntervalTreeDriver


class IntervalTree(SupriyaObject):
    """
    A mutable always-sorted collection of timespans.

    ::

        >>> from supriya.time import Interval, IntervalTree
        >>> from supriya.time import Interval, IntervalTree
        >>> timespans = (
        ...     Interval(0, 3),
        ...     Interval(1, 3),
        ...     Interval(1, 2),
        ...     Interval(2, 5),
        ...     Interval(6, 9),
        ...     )
        >>> interval_tree = IntervalTree(timespans)

    """

    ### INITIALIZER ###

    def __init__(self, timespans=None, accelerated=True):
        self._driver = IntervalTreeDriver(timespans)
        self._accelerated = bool(accelerated)
        if not accelerated:
            return
        try:
            import pyximport  # noqa
            from .IntervalTreeDriverEx import IntervalTreeDriverEx

            self._driver = IntervalTreeDriverEx(timespans)
        except (ImportError, ModuleNotFoundError):
            pass

    ### SPECIAL METHODS ###

    def __and__(self, timespan):
        new_timespans = []
        for current_timespan in self[:]:
            result = current_timespan & timespan
            new_timespans.extend(result)
        self[:] = sorted(new_timespans)
        return self

    def __contains__(self, timespan):
        """
        Is true if this interval tree contains `timespan`. Otherwise
        false.

        ::

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

        ::

            >>> timespans[0] in interval_tree
            True

        ::

            >>> Interval(-1, 100) in interval_tree
            False

        Returns boolean.
        """
        return timespan in self._driver

    def __getitem__(self, item):
        """
        Gets timespan at index `item`.

        ::

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

        ::

            >>> interval_tree[-1]
            Interval(start_offset=6.0, stop_offset=9.0)

        ::

            >>> for timespan in interval_tree[:3]:
            ...     timespan
            ...
            Interval(start_offset=0.0, stop_offset=3.0)
            Interval(start_offset=1.0, stop_offset=2.0)
            Interval(start_offset=1.0, stop_offset=3.0)

        Returns timespan or timespans.
        """
        return self._driver[item]

    def __getstate__(self):
        return self._accelerated, tuple(self)

    def __iter__(self):
        """
        Iterates timespans in this interval tree.

        ::

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

        ::

            >>> for timespan in interval_tree:
            ...     timespan
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

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

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
        Sets timespans at index `i` to `new`.

        ::

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

        ::

            >>> interval_tree[:3] = [Interval(100, 200)]

        Returns none.
        """
        if isinstance(i, int):
            self.remove(self[i])
            self.add(new)
        elif isinstance(i, slice):
            for timespan in self[i]:
                self.remove(timespan)
            self.update(new)
        else:
            message = "Indices must be ints or slices, got {}".format(i)
            raise TypeError(message)

    def __setstate__(self, state):
        accelerated, timespans = state
        self.__init__(timespans=timespans, accelerated=accelerated)

    def __sub__(self, timespan):
        """
        Delete material that intersects `timespan`:

        ::

            >>> from supriya.time import Interval, IntervalTree
            >>> interval_tree = IntervalTree([
            ...     Interval(0, 16),
            ...     Interval(5, 12),
            ...     Interval(-2, 8),
            ...     ])

        ::

            >>> timespan = Interval(5, 10)
            >>> result = interval_tree - timespan

        ::

            >>> for timespan in interval_tree:
            ...     timespan
            ...
            Interval(start_offset=-2.0, stop_offset=5.0)
            Interval(start_offset=0.0, stop_offset=5.0)
            Interval(start_offset=10.0, stop_offset=12.0)
            Interval(start_offset=10.0, stop_offset=16.0)

        Operates in place and returns interval tree.
        """
        if not self._is_timespan(timespan):
            raise ValueError(timespan)
        intersection = self.find_intersection(timespan)
        to_update = []
        for intersecting_timespan in intersection:
            self.remove(intersecting_timespan)
            for x in intersecting_timespan - timespan:
                to_update.append(x)
        self.update(to_update)
        return self

    ### PRIVATE METHODS ###

    @staticmethod
    def _is_timespan(expr):
        if hasattr(expr, "start_offset") and hasattr(expr, "stop_offset"):
            return True
        return False

    ### PUBLIC METHODS ###

    def find_intersection(self, timespan_or_offset):
        """
        Find timespans intersecting a timespan or offset.

        ..  container:: example

            Finds timespans overlapping `offset`.

            ::

                >>> from supriya.time import Interval, IntervalTree
                >>> timespans = (
                ...     Interval(0, 3),
                ...     Interval(1, 3),
                ...     Interval(1, 2),
                ...     Interval(2, 5),
                ...     Interval(6, 9),
                ...     )
                >>> interval_tree = IntervalTree(timespans)

            ::

                >>> for x in interval_tree.find_intersection(1.5):
                ...     x
                ...
                Interval(start_offset=0.0, stop_offset=3.0)
                Interval(start_offset=1.0, stop_offset=2.0)
                Interval(start_offset=1.0, stop_offset=3.0)

        ..  container:: example

            Finds timespans overlapping `timespan`.

            ::

                >>> timespans = (
                ...     Interval(0, 3),
                ...     Interval(1, 3),
                ...     Interval(1, 2),
                ...     Interval(2, 5),
                ...     Interval(6, 9),
                ...     )
                >>> interval_tree = IntervalTree(timespans)

            ::

                >>> timespan = Interval(2, 4)
                >>> for x in interval_tree.find_intersection(timespan):
                ...     x
                ...
                Interval(start_offset=0.0, stop_offset=3.0)
                Interval(start_offset=1.0, stop_offset=3.0)
                Interval(start_offset=2.0, stop_offset=5.0)

        """
        if self._is_timespan(timespan_or_offset):
            return self._driver.find_timespans_intersecting_timespan(timespan_or_offset)
        return self._driver.find_timespans_intersecting_offset(timespan_or_offset)

    def find_timespans_starting_at(self, offset):
        return self._driver.find_timespans_starting_at(offset)

    def find_timespans_stopping_at(self, offset):
        return self._driver.find_timespans_stopping_at(offset)

    def get_moment_at(self, offset):
        """
        Gets moment at `offset`.

        ::

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

        ::

            >>> interval_tree.get_moment_at(1)
            <Moment(1 <<3>>)>

        ::

            >>> interval_tree.get_moment_at(6.5)
            <Moment(6.5 <<1>>)>

        """
        stop_timespans = self.find_timespans_stopping_at(offset)
        start_timespans, overlap_timespans = [], []
        for timespan in self.find_intersection(offset):
            if timespan.start_offset == offset:
                start_timespans.append(timespan)
            else:
                overlap_timespans.append(timespan)
        moment = Moment(
            interval_tree=self,
            overlap_timespans=overlap_timespans,
            start_timespans=start_timespans,
            start_offset=offset,
            stop_timespans=stop_timespans,
        )
        return moment

    def get_offset_after(self, offset):
        """
        Gets first start or stop offset after ``offset``, otherwise None.

        ::

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

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

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

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

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

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

    def index(self, timespan):
        return self._driver.index(timespan)

    def add(self, timespan):
        self._driver.add(timespan)

    def update(self, timespans):
        self._driver.update(timespans)

    def iterate_simultaneities(self, reverse=False):
        """
        Iterates simultaneities in this interval tree.

        ::

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

        ::

            >>> for x in interval_tree.iterate_simultaneities():
            ...     x
            ...
            <Moment(0.0 <<1>>)>
            <Moment(1.0 <<3>>)>
            <Moment(2.0 <<3>>)>
            <Moment(6.0 <<1>>)>

        ::

            >>> for x in interval_tree.iterate_simultaneities(
            ...     reverse=True):
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

    def iterate_simultaneities_nwise(self, n=3, reverse=False):
        """
        Iterates simultaneities in this interval tree in groups of
        `n`.

        ::

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

        ::

            >>> for x in interval_tree.iterate_simultaneities_nwise(n=2):
            ...     x
            ...
            [<Moment(0.0 <<1>>)>, <Moment(1.0 <<3>>)>]
            [<Moment(1.0 <<3>>)>, <Moment(2.0 <<3>>)>]
            [<Moment(2.0 <<3>>)>, <Moment(6.0 <<1>>)>]

        ::

            >>> for x in interval_tree.iterate_simultaneities_nwise(
            ...     n=2, reverse=True):
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
            for moment in self.iterate_simultaneities(reverse=True):
                simultaneities = [moment]
                while len(simultaneities) < n:
                    next_moment = simultaneities[-1].next_moment
                    if next_moment is None:
                        break
                    simultaneities.append(next_moment)
                if len(simultaneities) == n:
                    yield simultaneities
        else:
            for moment in self.iterate_simultaneities():
                simultaneities = [moment]
                while len(simultaneities) < n:
                    previous_moment = simultaneities[-1].previous_moment
                    if previous_moment is None:
                        break
                    simultaneities.append(previous_moment)
                if len(simultaneities) == n:
                    yield list(reversed(simultaneities))

    def remove(self, timespan):
        """
        Removes timespan from this interval tree.

        ::

            >>> from supriya.time import Interval, IntervalTree
            >>> timespans = (
            ...     Interval(0, 3),
            ...     Interval(1, 3),
            ...     Interval(1, 2),
            ...     Interval(2, 5),
            ...     Interval(6, 9),
            ...     )
            >>> interval_tree = IntervalTree(timespans)

        ::

            >>> for timespan in timespans[1:-1]:
            ...     interval_tree.remove(timespan)
            ...

        ::

            >>> for timespan in interval_tree:
            ...     timespan
            ...
            Interval(start_offset=0.0, stop_offset=3.0)
            Interval(start_offset=6.0, stop_offset=9.0)

        """
        self._driver.remove(timespan)

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
        for timespan in self:
            offsets.add(timespan.start_offset)
            offsets.add(timespan.stop_offset)
        return tuple(sorted(offsets))

    @property
    def all_start_offsets(self):
        start_offsets = set()
        for timespan in self:
            start_offsets.add(timespan.start_offset)
        return tuple(sorted(start_offsets))

    @property
    def all_stop_offsets(self):
        stop_offsets = set()
        for timespan in self:
            stop_offsets.add(timespan.stop_offset)
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

    @property
    def timespans(self):
        return list(self)
