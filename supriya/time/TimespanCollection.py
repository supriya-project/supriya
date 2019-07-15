from supriya.system.SupriyaObject import SupriyaObject
from supriya.time.TimespanCollectionDriver import TimespanCollectionDriver
from supriya.time.TimespanSimultaneity import TimespanSimultaneity


class TimespanCollection(SupriyaObject):
    """
    A mutable always-sorted collection of timespans.

    ::

        >>> import abjad.timespans
        >>> import supriya.time
        >>> timespans = (
        ...     abjad.timespans.Timespan(0, 3),
        ...     abjad.timespans.Timespan(1, 3),
        ...     abjad.timespans.Timespan(1, 2),
        ...     abjad.timespans.Timespan(2, 5),
        ...     abjad.timespans.Timespan(6, 9),
        ...     )
        >>> timespan_collection = supriya.time.TimespanCollection(timespans)

    """

    ### CLASS VARIABLES ###

    ### INITIALIZER ###

    def __init__(self, timespans=None, accelerated=True):
        self._driver = TimespanCollectionDriver(timespans)
        self._accelerated = bool(accelerated)
        if accelerated:
            try:
                import pyximport  # noqa
                from supriya.time.TimespanCollectionDriverEx import (
                    TimespanCollectionDriverEx,
                )

                self._driver = TimespanCollectionDriverEx(timespans)
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
        Is true if this timespan collection contains `timespan`. Otherwise
        false.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> timespans[0] in timespan_collection
            True

        ::

            >>> abjad.timespans.Timespan(-1, 100) in timespan_collection
            False

        Returns boolean.
        """
        return timespan in self._driver

    def __getitem__(self, item):
        """
        Gets timespan at index `item`.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> timespan_collection[-1]
            Timespan(start_offset=Offset(6, 1), stop_offset=Offset(9, 1))

        ::

            >>> for timespan in timespan_collection[:3]:
            ...     timespan
            ...
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 1))
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(2, 1))
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 1))

        Returns timespan or timespans.
        """
        return self._driver[item]

    def __getstate__(self):
        return self._accelerated, tuple(self)

    def __iter__(self):
        """
        Iterates timespans in this timespan collection.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> for timespan in timespan_collection:
            ...     timespan
            ...
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 1))
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(2, 1))
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 1))
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(5, 1))
            Timespan(start_offset=Offset(6, 1), stop_offset=Offset(9, 1))

        Returns generator.
        """
        return iter(self._driver)

    def __len__(self):
        """
        Gets length of this timespan collection.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> len(timespan_collection)
            5

        Returns integer.
        """
        return len(self._driver)

    def __setitem__(self, i, new):
        """
        Sets timespans at index `i` to `new`.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> timespan_collection[:3] = [abjad.timespans.Timespan(100, 200)]

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

            >>> import abjad.timespans
            >>> timespan_collection = supriya.time.TimespanCollection([
            ...     abjad.timespans.Timespan(0, 16),
            ...     abjad.timespans.Timespan(5, 12),
            ...     abjad.timespans.Timespan(-2, 8),
            ...     ])

        ::

            >>> timespan = abjad.timespans.Timespan(5, 10)
            >>> result = timespan_collection - timespan

        ::

            >>> for timespan in timespan_collection:
            ...     timespan
            ...
            Timespan(start_offset=Offset(-2, 1), stop_offset=Offset(5, 1))
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(5, 1))
            Timespan(start_offset=Offset(10, 1), stop_offset=Offset(12, 1))
            Timespan(start_offset=Offset(10, 1), stop_offset=Offset(16, 1))

        Operates in place and returns timespan collection.
        """
        assert self._is_timespan(timespan)
        intersection = self.find_intersection(timespan)
        self.remove(intersection)
        for intersecting_timespan in intersection:
            for x in intersecting_timespan - timespan:
                self.add(x)
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

                >>> import abjad.timespans
                >>> timespans = (
                ...     abjad.timespans.Timespan(0, 3),
                ...     abjad.timespans.Timespan(1, 3),
                ...     abjad.timespans.Timespan(1, 2),
                ...     abjad.timespans.Timespan(2, 5),
                ...     abjad.timespans.Timespan(6, 9),
                ...     )
                >>> timespan_collection = supriya.time.TimespanCollection(timespans)

            ::

                >>> for x in timespan_collection.find_intersection(1.5):
                ...     x
                ...
                Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 1))
                Timespan(start_offset=Offset(1, 1), stop_offset=Offset(2, 1))
                Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 1))

        ..  container:: example

            Finds timespans overlapping `timespan`.

            ::

                >>> timespans = (
                ...     abjad.timespans.Timespan(0, 3),
                ...     abjad.timespans.Timespan(1, 3),
                ...     abjad.timespans.Timespan(1, 2),
                ...     abjad.timespans.Timespan(2, 5),
                ...     abjad.timespans.Timespan(6, 9),
                ...     )
                >>> timespan_collection = supriya.time.TimespanCollection(timespans)

            ::

                >>> timespan = abjad.timespans.Timespan(2, 4)
                >>> for x in timespan_collection.find_intersection(timespan):
                ...     x
                ...
                Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 1))
                Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 1))
                Timespan(start_offset=Offset(2, 1), stop_offset=Offset(5, 1))

        """
        if self._is_timespan(timespan_or_offset):
            return self._driver.find_timespans_intersecting_timespan(timespan_or_offset)
        return self._driver.find_timespans_intersecting_offset(timespan_or_offset)

    def find_timespans_starting_at(self, offset):
        return self._driver.find_timespans_starting_at(offset)

    def find_timespans_stopping_at(self, offset):
        return self._driver.find_timespans_stopping_at(offset)

    def get_simultaneity_at(self, offset):
        """
        Gets simultaneity at `offset`.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> timespan_collection.get_simultaneity_at(1)
            <TimespanSimultaneity(1 <<3>>)>

        ::

            >>> timespan_collection.get_simultaneity_at(6.5)
            <TimespanSimultaneity(6.5 <<1>>)>

        """
        stop_timespans = self.find_timespans_stopping_at(offset)
        start_timespans, overlap_timespans = [], []
        for timespan in self.find_intersection(offset):
            if timespan.start_offset == offset:
                start_timespans.append(timespan)
            else:
                overlap_timespans.append(timespan)
        simultaneity = TimespanSimultaneity(
            timespan_collection=self,
            overlap_timespans=overlap_timespans,
            start_timespans=start_timespans,
            start_offset=offset,
            stop_timespans=stop_timespans,
        )
        return simultaneity

    def get_offset_after(self, offset):
        """
        Gets first start or stop offset after ``offset``, otherwise None.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> for i in range(-1, 11):
            ...     print(i, timespan_collection.get_offset_after(i))
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
        Gets start offst in this timespan collection after `offset`.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> timespan_collection.get_start_offset_after(-1)
            0.0

        ::

            >>> timespan_collection.get_start_offset_after(0)
            1.0

        ::

            >>> timespan_collection.get_start_offset_after(1)
            2.0

        ::

            >>> timespan_collection.get_start_offset_after(2)
            6.0

        ::

            >>> timespan_collection.get_start_offset_after(6) is None
            True

        """
        return self._driver.get_start_offset_after(float(offset))

    def get_start_offset_before(self, offset):
        """
        Gets start offst in this timespan collection before `offset`.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> timespan_collection.get_start_offset_before(7)
            6.0

        ::

            >>> timespan_collection.get_start_offset_before(6)
            2.0

        ::

            >>> timespan_collection.get_start_offset_before(2)
            1.0

        ::

            >>> timespan_collection.get_start_offset_before(1)
            0.0

        ::

            >>> timespan_collection.get_start_offset_before(0) is None
            True

        """
        return self._driver.get_start_offset_before(float(offset))

    def index(self, timespan):
        return self._driver.index(timespan)

    def add(self, timespan):
        self._driver.insert([timespan])

    def update(self, timespans):
        self._driver.insert(timespans)

    def iterate_simultaneities(self, reverse=False):
        """
        Iterates simultaneities in this timespan collection.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> for x in timespan_collection.iterate_simultaneities():
            ...     x
            ...
            <TimespanSimultaneity(0.0 <<1>>)>
            <TimespanSimultaneity(1.0 <<3>>)>
            <TimespanSimultaneity(2.0 <<3>>)>
            <TimespanSimultaneity(6.0 <<1>>)>

        ::

            >>> for x in timespan_collection.iterate_simultaneities(
            ...     reverse=True):
            ...     x
            ...
            <TimespanSimultaneity(6.0 <<1>>)>
            <TimespanSimultaneity(2.0 <<3>>)>
            <TimespanSimultaneity(1.0 <<3>>)>
            <TimespanSimultaneity(0.0 <<1>>)>

        Returns generator.
        """

        if reverse:
            start_offset = self.latest_start_offset
            simultaneity = self.get_simultaneity_at(start_offset)
            yield simultaneity
            simultaneity = simultaneity.previous_simultaneity
            while simultaneity is not None:
                yield simultaneity
                simultaneity = simultaneity.previous_simultaneity
        else:
            start_offset = self.earliest_start_offset
            simultaneity = self.get_simultaneity_at(start_offset)
            yield simultaneity
            simultaneity = simultaneity.next_simultaneity
            while simultaneity is not None:
                yield simultaneity
                simultaneity = simultaneity.next_simultaneity

    def iterate_simultaneities_nwise(self, n=3, reverse=False):
        """
        Iterates simultaneities in this timespan collection in groups of
        `n`.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> for x in timespan_collection.iterate_simultaneities_nwise(n=2):
            ...     x
            ...
            [<TimespanSimultaneity(0.0 <<1>>)>, <TimespanSimultaneity(1.0 <<3>>)>]
            [<TimespanSimultaneity(1.0 <<3>>)>, <TimespanSimultaneity(2.0 <<3>>)>]
            [<TimespanSimultaneity(2.0 <<3>>)>, <TimespanSimultaneity(6.0 <<1>>)>]

        ::

            >>> for x in timespan_collection.iterate_simultaneities_nwise(
            ...     n=2, reverse=True):
            ...     x
            ...
            [<TimespanSimultaneity(2.0 <<3>>)>, <TimespanSimultaneity(6.0 <<1>>)>]
            [<TimespanSimultaneity(1.0 <<3>>)>, <TimespanSimultaneity(2.0 <<3>>)>]
            [<TimespanSimultaneity(0.0 <<1>>)>, <TimespanSimultaneity(1.0 <<3>>)>]

        Returns generator.
        """
        n = int(n)
        assert 0 < n
        if reverse:
            for simultaneity in self.iterate_simultaneities(reverse=True):
                simultaneities = [simultaneity]
                while len(simultaneities) < n:
                    next_simultaneity = simultaneities[-1].next_simultaneity
                    if next_simultaneity is None:
                        break
                    simultaneities.append(next_simultaneity)
                if len(simultaneities) == n:
                    yield simultaneities
        else:
            for simultaneity in self.iterate_simultaneities():
                simultaneities = [simultaneity]
                while len(simultaneities) < n:
                    previous_simultaneity = simultaneities[-1].previous_simultaneity
                    if previous_simultaneity is None:
                        break
                    simultaneities.append(previous_simultaneity)
                if len(simultaneities) == n:
                    yield list(reversed(simultaneities))

    def remove(self, timespans):
        """
        Removes timespans from this timespan collection.

        ::

            >>> import abjad.timespans
            >>> timespans = (
            ...     abjad.timespans.Timespan(0, 3),
            ...     abjad.timespans.Timespan(1, 3),
            ...     abjad.timespans.Timespan(1, 2),
            ...     abjad.timespans.Timespan(2, 5),
            ...     abjad.timespans.Timespan(6, 9),
            ...     )
            >>> timespan_collection = supriya.time.TimespanCollection(timespans)

        ::

            >>> timespan_collection.remove(timespans[1:-1])

        ::

            >>> for timespan in timespan_collection:
            ...     timespan
            ...
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(3, 1))
            Timespan(start_offset=Offset(6, 1), stop_offset=Offset(9, 1))

        """
        self._driver.remove(timespans)

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
