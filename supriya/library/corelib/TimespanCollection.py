# -*- encoding: utf-8 -*-
import collections


class TimespanCollection(object):
    r'''A mutable always-sorted collection of timespans.

    ::

        >>> from abjad import *
        >>> from supriya import *
        >>> timespans = (
        ...     timespantools.Timespan(0, 3),
        ...     timespantools.Timespan(1, 3),
        ...     timespantools.Timespan(1, 2),
        ...     timespantools.Timespan(2, 5),
        ...     timespantools.Timespan(6, 9),
        ...     )
        >>> timespan_collection = corelib.TimespanCollection(timespans)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_root_node',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        timespans=None,
        ):
        self._root_node = None
        if timespans is not None and timespans:
            self.insert(timespans)

    ### SPECIAL METHODS ###

    def __contains__(self, timespan):
        r'''Is true if this timespan collection contains `timespan`. Otherwise
        false.

        ::

            >>> timespans = (
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(1, 3),
            ...     timespantools.Timespan(1, 2),
            ...     timespantools.Timespan(2, 5),
            ...     timespantools.Timespan(6, 9),
            ...     )
            >>> timespan_collection = corelib.TimespanCollection(timespans)

        ::

            >>> timespans[0] in timespan_collection
            True

        ::

            >>> timespantools.Timespan(-1, 100) in timespan_collection
            False

        Returns boolean.
        '''
        assert TimespanCollection._is_timespan(timespan)
        candidates = self.find_timespans_starting_at(timespan.start_offset)
        result = timespan in candidates
        return result

    def __getitem__(self, i):
        r'''Gets timespan at index `i`.

        ::

            >>> timespans = (
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(1, 3),
            ...     timespantools.Timespan(1, 2),
            ...     timespantools.Timespan(2, 5),
            ...     timespantools.Timespan(6, 9),
            ...     )
            >>> timespan_collection = corelib.TimespanCollection(timespans)

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
        '''
        def recurse_by_index(node, index):
            if node.node_start_index <= index < node.node_stop_index:
                return node.payload[index - node.node_start_index]
            elif node.left_child and index < node.node_start_index:
                return recurse_by_index(node.left_child, index)
            elif node.right_child and node.node_stop_index <= index:
                return recurse_by_index(node.right_child, index)

        def recurse_by_slice(node, start, stop):
            result = []
            if node is None:
                return result
            if start < node.node_start_index and node.left_child:
                result.extend(recurse_by_slice(node.left_child, start, stop))
            if start < node.node_stop_index and node.node_start_index < stop:
                node_start = start - node.node_start_index
                if node_start < 0:
                    node_start = 0
                node_stop = stop - node.node_start_index
                result.extend(node.payload[node_start:node_stop])
            if node.node_stop_index <= stop and node.right_child:
                result.extend(recurse_by_slice(node.right_child, start, stop))
            return result

        if isinstance(i, int):
            if self._root_node is None:
                raise IndexError
            if i < 0:
                i = self._root_node.subtree_stop_index + i
            if i < 0 or self._root_node.subtree_stop_index <= i:
                raise IndexError
            return recurse_by_index(self._root_node, i)
        elif isinstance(i, slice):
            if self._root_node is None:
                return []
            indices = i.indices(self._root_node.subtree_stop_index)
            start, stop = indices[0], indices[1]
            return recurse_by_slice(self._root_node, start, stop)

        raise TypeError('Indices must be integers or slices, got {}'.format(i))

    def __iter__(self):
        r'''Iterates timespans in this timespan collection.

        ::

            >>> timespans = (
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(1, 3),
            ...     timespantools.Timespan(1, 2),
            ...     timespantools.Timespan(2, 5),
            ...     timespantools.Timespan(6, 9),
            ...     )
            >>> timespan_collection = corelib.TimespanCollection(timespans)

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
        '''

        def recurse(node):
            if node is not None:
                if node.left_child is not None:
                    for timespan in recurse(node.left_child):
                        yield timespan
                for timespan in node.payload:
                    yield timespan
                if node.right_child is not None:
                    for timespan in recurse(node.right_child):
                        yield timespan
        return recurse(self._root_node)

    def __len__(self):
        r'''Gets length of this timespan collection.

        ::

            >>> timespans = (
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(1, 3),
            ...     timespantools.Timespan(1, 2),
            ...     timespantools.Timespan(2, 5),
            ...     timespantools.Timespan(6, 9),
            ...     )
            >>> timespan_collection = corelib.TimespanCollection(timespans)

        ::

            >>> len(timespan_collection)
            5

        Returns integer.
        '''
        if self._root_node is None:
            return 0
        return self._root_node.subtree_stop_index

    def __setitem__(self, i, new):
        r'''Sets timespans at index `i` to `new`.

        ::

            >>> timespans = (
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(1, 3),
            ...     timespantools.Timespan(1, 2),
            ...     timespantools.Timespan(2, 5),
            ...     timespantools.Timespan(6, 9),
            ...     )
            >>> timespan_collection = corelib.TimespanCollection(timespans)

        ::

            >>> timespan_collection[:3] = [timespantools.Timespan(100, 200)]

        Returns none.
        '''
        if isinstance(i, (int, slice)):
            old = self[i]
            self.remove(old)
            self.insert(new)
        else:
            message = 'Indices must be ints or slices, got {}'.format(i)
            raise TypeError(message)

    ### PRIVATE METHODS ###

    def _insert_node(self, node, start_offset):
        from supriya.library import corelib
        if node is None:
            return corelib.TimespanCollectionNode(start_offset)
        if start_offset < node.start_offset:
            node.left_child = self._insert_node(node.left_child, start_offset)
        elif node.start_offset < start_offset:
            node.right_child = self._insert_node(node.right_child, start_offset)
        return self._rebalance(node)

    def _insert_timespan(self, timespan):
        self._root_node = self._insert_node(
            self._root_node,
            timespan.start_offset,
            )
        node = self._search(self._root_node, timespan.start_offset)
        node.payload.append(timespan)
        node.payload.sort(key=lambda x: x.stop_offset)

    @staticmethod
    def _is_timespan(expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return True
        return False

    def _rebalance(self, node):
        if node is not None:
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
            assert -1 <= node.balance <= 1
        return node

    def _remove_node(self, node, start_offset):
        if node is not None:
            if node.start_offset == start_offset:
                if node.left_child and node.right_child:
                    next_node = node.right_child
                    while next_node.left_child:
                        next_node = next_node.left_child
                    node._start_offset = next_node._start_offset
                    node._payload = next_node._payload
                    node.right_child = self._remove_node(
                        node.right_child,
                        next_node.start_offset,
                        )
                else:
                    node = node.left_child or node.right_child
            elif start_offset < node.start_offset:
                node.left_child = self._remove_node(
                    node.left_child,
                    start_offset,
                    )
            elif node.start_offset < start_offset:
                node.right_child = self._remove_node(
                    node.right_child,
                    start_offset,
                    )
        return self._rebalance(node)

    def _remove_timespan(self, timespan, old_start_offset=None):
        start_offset = timespan.start_offset
        if old_start_offset is not None:
            start_offset = old_start_offset
        node = self._search(self._root_node, start_offset)
        if node is None:
            return
        if timespan in node.payload:
            node.payload.remove(timespan)
        if not node.payload:
            self._root_node = self._remove_node(
                self._root_node,
                start_offset,
                )
        if isinstance(timespan, TimespanCollection):
            timespan._parents.remove(self)

    def _rotate_left_left(self, node):
        next_node = node.left_child
        node.left_child = next_node.right_child
        next_node.right_child = node
        return next_node

    def _rotate_left_right(self, node):
        node.left_child = self._rotate_right_right(node.left_child)
        next_node = self._rotate_left_left(node)
        return next_node

    def _rotate_right_left(self, node):
        node.right_child = self._rotate_left_left(node.right_child)
        next_node = self._rotate_right_right(node)
        return next_node

    def _rotate_right_right(self, node):
        next_node = node.right_child
        node.right_child = next_node.left_child
        next_node.left_child = node
        return next_node

    def _search(self, node, start_offset):
        if node is not None:
            if node.start_offset == start_offset:
                return node
            elif node.left_child and start_offset < node.start_offset:
                return self._search(node.left_child, start_offset)
            elif node.right_child and node.start_offset < start_offset:
                return self._search(node.right_child, start_offset)
        return None

    def _update_indices(
        self,
        node,
        ):
        def recurse(
            node,
            parent_stop_index=None,
            ):
            if node is None:
                return
            if node.left_child is not None:
                recurse(
                    node.left_child,
                    parent_stop_index=parent_stop_index,
                    )
                node._node_start_index = node.left_child.subtree_stop_index
                node._subtree_start_index = node.left_child.subtree_start_index
            elif parent_stop_index is None:
                node._node_start_index = 0
                node._subtree_start_index = 0
            else:
                node._node_start_index = parent_stop_index
                node._subtree_start_index = parent_stop_index
            node._node_stop_index = node.node_start_index + len(node.payload)
            node._subtree_stop_index = node.node_stop_index
            if node.right_child is not None:
                recurse(
                    node.right_child,
                    parent_stop_index=node.node_stop_index,
                    )
                node._subtree_stop_index = node.right_child.subtree_stop_index
        recurse(node)

    def _update_offsets(
        self,
        node,
        ):
        if node is None:
            return
        stop_offset_low = min(x.stop_offset for x in node.payload)
        stop_offset_high = max(x.stop_offset for x in node.payload)
        if node.left_child:
            left_child = self._update_offsets(
                node.left_child,
                )
            if left_child.stop_offset_low < stop_offset_low:
                stop_offset_low = left_child.stop_offset_low
            if stop_offset_high < left_child.stop_offset_high:
                stop_offset_high = left_child.stop_offset_high
        if node.right_child:
            right_child = self._update_offsets(
                node.right_child,
                )
            if right_child.stop_offset_low < stop_offset_low:
                stop_offset_low = right_child.stop_offset_low
            if stop_offset_high < right_child.stop_offset_high:
                stop_offset_high = right_child.stop_offset_high
        node._stop_offset_low = stop_offset_low
        node._stop_offset_high = stop_offset_high
        return node

    ### PUBLIC METHODS ###

    def find_timespans_starting_at(self, offset):
        results = []
        node = self._search(self._root_node, offset)
        if node is not None:
            results.extend(node.payload)
        return tuple(results)

    def find_timespans_stopping_at(self, offset):
        def recurse(node, offset):
            result = []
            if node is not None:
                if node.stop_offset_low <= offset <= node.stop_offset_high:
                    for timespan in node.payload:
                        if timespan.stop_offset == offset:
                            result.append(timespan)
                    if node.left_child is not None:
                        result.extend(recurse(node.left_child, offset))
                    if node.right_child is not None:
                        result.extend(recurse(node.right_child, offset))
            return result
        results = recurse(self._root_node, offset)
        results.sort(key=lambda x: (x.start_offset, x.stop_offset))
        return tuple(results)

    def find_timespans_overlapping(self, offset):
        def recurse(node, offset, indent=0):
            result = []
            if node is not None:
                if node.start_offset < offset < node.stop_offset_high:
                    result.extend(recurse(node.left_child, offset, indent + 1))
                    for timespan in node.payload:
                        if offset < timespan.stop_offset:
                            result.append(timespan)
                    result.extend(recurse(node.right_child, offset, indent + 1))
                elif offset <= node.start_offset:
                    result.extend(recurse(node.left_child, offset, indent + 1))
            return result
        results = recurse(self._root_node, offset)
        results.sort(key=lambda x: (x.start_offset, x.stop_offset))
        return tuple(results)

    def get_simultaneity_at(self, offset):
        from supriya.library import corelib
        start_timespans = self.find_timespans_starting_at(offset)
        stop_timespans = self.find_timespans_stopping_at(offset)
        overlap_timespans = self.find_timespans_overlapping(offset)
        simultaneity = corelib.TimespanSimultaneity(
            timespan_collection=self,
            overlap_timespans=overlap_timespans,
            start_timespans=start_timespans,
            start_offset=offset,
            stop_timespans=stop_timespans,
            )
        return simultaneity

    def get_simultaneity_at_or_before(self, offset):
        simultaneity = self.get_simultaneity_at(offset)
        if not simultaneity.start_timespans:
            simultaneity = simultaneity.previous_simultaneity
        return simultaneity

    def get_start_offset_after(self, offset):
        def recurse(node, offset):
            if node is None:
                return None
            result = None
            if node.start_offset <= offset and node.right_child:
                result = recurse(node.right_child, offset)
            elif offset < node.start_offset:
                result = recurse(node.left_child, offset) or node
            return result
        result = recurse(self._root_node, offset)
        if result is None:
            return None
        return result.start_offset

    def get_start_offset_before(self, offset):
        def recurse(node, offset):
            if node is None:
                return None
            result = None
            if node.start_offset < offset:
                result = recurse(node.right_child, offset) or node
            elif offset <= node.start_offset and node.left_child:
                result = recurse(node.left_child, offset)
            return result
        result = recurse(self._root_node, offset)
        if result is None:
            return None
        return result.start_offset

    def index(self, timespan):
        assert self._is_timespan(timespan)
        node = self._search(self._root_node, timespan.start_offset)
        if node is None or timespan not in node.payload:
            raise ValueError('{} not in timespan collection.'.format(timespan))
        index = node.payload.index(timespan) + node.node_start_index
        return index

    def insert(self, timespans):
        r'''Inserts `timespans` into this timespan collection.

        ::

            >>> timespan_collection = corelib.TimespanCollection()
            >>> timespan_collection.insert(timespantools.Timespan(1, 3))
            >>> timespan_collection.insert((
            ...     timespantools.Timespan(0, 4),
            ...     timespantools.Timespan(2, 6),
            ...     ))

        ::

            >>> for x in timespan_collection:
            ...     x
            ...
            Timespan(start_offset=Offset(0, 1), stop_offset=Offset(4, 1))
            Timespan(start_offset=Offset(1, 1), stop_offset=Offset(3, 1))
            Timespan(start_offset=Offset(2, 1), stop_offset=Offset(6, 1))

        `timespans` may be a single timespan or an iterable of timespans.

        Returns none.
        '''
        if self._is_timespan(timespans):
            timespans = [timespans]
        for timespan in timespans:
            if not self._is_timespan(timespan):
                continue
            self._insert_timespan(timespan)
        self._update_indices(self._root_node)
        self._update_offsets(self._root_node)

    def iterate_simultaneities(
        self,
        reverse=False,
        ):
        r'''Iterates simultaneities in this timespan collection.

        ::

            >>> timespans = (
            ...     timespantools.Timespan(0, 3),
            ...     timespantools.Timespan(1, 3),
            ...     timespantools.Timespan(1, 2),
            ...     timespantools.Timespan(2, 5),
            ...     timespantools.Timespan(6, 9),
            ...     )
            >>> timespan_collection = corelib.TimespanCollection(timespans)

        ::

            >>> for x in timespan_collection.iterate_simultaneities():
            ...     x
            ...
            <TimespanSimultaneity(0 <<1>>)>
            <TimespanSimultaneity(1 <<3>>)>
            <TimespanSimultaneity(2 <<3>>)>
            <TimespanSimultaneity(6 <<1>>)>

        ::

            >>> for x in timespan_collection.iterate_simultaneities(
            ...     reverse=True):
            ...     x
            ...
            <TimespanSimultaneity(6 <<1>>)>
            <TimespanSimultaneity(2 <<3>>)>
            <TimespanSimultaneity(1 <<3>>)>
            <TimespanSimultaneity(0 <<1>>)>

        Returns generator.
        '''

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

    def iterate_simultaneities_nwise(
        self,
        n=3,
        reverse=False,
        ):
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
                    yield tuple(simultaneities)
        else:
            for simultaneity in self.iterate_simultaneities():
                simultaneities = [simultaneity]
                while len(simultaneities) < n:
                    previous_simultaneity = simultaneities[-1].previous_simultaneity
                    if previous_simultaneity is None:
                        break
                    simultaneities.append(previous_simultaneity)
                if len(simultaneities) == n:
                    yield tuple(reversed(simultaneities))

    def remove(self, timespans):
        if self._is_timespan(timespans):
            timespans = [timespans]
        for timespan in timespans:
            if not self._is_timespan(timespan):
                continue
            self._remove_timespan(timespan)
        self._update_indices(self._root_node)
        self._update_offsets(self._root_node)

    def split_at(self, offsets):
        if not isinstance(offsets, collections.Iterable):
            offsets = [offsets]
        for offset in offsets:
            overlaps = self.find_timespans_overlapping(offset)
            if not overlaps:
                continue
            for overlap in overlaps:
                self.remove(overlap)
                shards = overlap.split_at(offset)
                self.insert(shards)

    ### PUBLIC PROPERTIES ###

    @property
    def all_offsets(self):
        def recurse(node):
            result = set()
            if node is not None:
                if node.left_child is not None:
                    result.update(recurse(node.left_child))
                result.add(node.start_offset)
                #result.add(node.stop_offset_low)
                #result.add(node.stop_offset_high)
                if node.right_child is not None:
                    result.update(recurse(node.right_child))
            return result
        return tuple(sorted(recurse(self._root_node)))

    @property
    def all_start_offsets(self):
        def recurse(node):
            result = []
            if node is not None:
                if node.left_child is not None:
                    result.extend(recurse(node.left_child))
                result.append(node.start_offset)
                if node.right_child is not None:
                    result.extend(recurse(node.right_child))
            return result
        return tuple(recurse(self._root_node))

    @property
    def all_stop_offsets(self):
        def recurse(node):
            result = set()
            if node is not None:
                if node.left_child is not None:
                    result.update(recurse(node.left_child))
                result.add(node.stop_offset_low)
                result.add(node.stop_offset_high)
                if node.right_child is not None:
                    result.update(recurse(node.right_child))
            return result
        return tuple(sorted(recurse(self._root_node)))

    @property
    def earliest_start_offset(self):
        def recurse(node):
            if node.left_child is not None:
                return recurse(node.left_child)
            return node.start_offset
        if self._root_node is not None:
            return recurse(self._root_node)
        return float('-inf')

    @property
    def earliest_stop_offset(self):
        if self._root_node is not None:
            return self._root_node.stop_offset_low
        return float('inf')

    @property
    def latest_start_offset(self):
        def recurse(node):
            if node.right_child is not None:
                return recurse(node._right_child)
            return node.start_offset
        if self._root_node is not None:
            return recurse(self._root_node)
        return float('-inf')

    @property
    def latest_stop_offset(self):
        if self._root_node is not None:
            return self._root_node.stop_offset_high
        return float('inf')

    @property
    def start_offset(self):
        return self.earliest_start_offset

    @property
    def stop_offset(self):
        return self.latest_stop_offset

