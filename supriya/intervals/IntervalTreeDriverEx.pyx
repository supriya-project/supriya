from supriya.intervals.Moment import Moment
from supriya.system import SupriyaObject


cdef class _CInterval:

    cdef readonly float start_offset
    cdef readonly float stop_offset
    cdef readonly object original_interval

    def __cinit__(self, start_offset, stop_offset, original_interval):
        self.start_offset = start_offset
        self.stop_offset = stop_offset
        self.original_interval = original_interval

    def __richcmp__(_CInterval self, _CInterval other, int op):
        if op == 0:  # <
            if self.start_offset < other.start_offset:
                return True
            if self.start_offset > other.start_offset:
                return False
            if self.stop_offset < other.stop_offset:
                return True
            return False
        if op == 2:  # ==
            if self.start_offset != other.start_offset:
                return False
            if self.stop_offset != other.stop_offset:
                return False
            if self.original_interval != other.original_interval:
                return False
            return True

    @classmethod
    def from_interval(cls, interval):
        start_offset = float(interval.start_offset)
        stop_offset = float(interval.stop_offset)
        return cls(
            start_offset,
            stop_offset,
            interval,
            )

    cpdef bint intersects_interval(_CInterval self, _CInterval other):
        return (
            (
                other.start_offset <= self.start_offset and
                self.start_offset < other.stop_offset
            ) or (
                self.start_offset <= other.start_offset and
                other.start_offset < self.stop_offset
                )
            )


cdef class _CNode:

    cdef public int balance
    cdef public int height
    cdef public _CNode left_child
    cdef public int node_start_index
    cdef public int node_stop_index
    cdef public object payload
    cdef public _CNode right_child
    cdef public float start_offset
    cdef public float stop_offset_high
    cdef public float stop_offset_low
    cdef public int subtree_start_index
    cdef public int subtree_stop_index

    def __init__(self, start_offset):
        self.balance = 0
        self.height = 0
        self.left_child = None
        self.node_start_index = -1
        self.node_stop_index = -1
        self.payload = []
        self.right_child = None
        self.start_offset = start_offset
        self.stop_offset_high = start_offset
        self.stop_offset_low = start_offset
        self.subtree_start_index = -1
        self.subtree_stop_index = -1


cdef class IntervalTreeDriverEx:
    """
    A mutable always-sorted collection of intervals.
    """

    ### CLASS VARIABLES ###

    cdef public object _root_node

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

    def __getitem__(self, i):
        if isinstance(i, int):
            if self._root_node is None:
                raise IndexError
            if i < 0:
                i = self._root_node.subtree_stop_index + i
            if i < 0 or self._root_node.subtree_stop_index <= i:
                raise IndexError
            cinterval = self._recurse_getitem_by_index(self._root_node, i)
            return cinterval.original_interval
        elif isinstance(i, slice):
            if self._root_node is None:
                return []
            indices = i.indices(self._root_node.subtree_stop_index)
            start, stop = indices[0], indices[1]
            cintervals = self._recurse_getitem_by_slice(self._root_node, start, stop)
            return self._unbox_cintervals(cintervals)
        raise TypeError('Indices must be integers or slices, got {}'.format(i))

    def __iter__(self):
        cdef _CNode current
        cdef _CInterval cinterval
        stack = []
        current = self._root_node
        while True:
            while current is not None:
                stack.append(current)
                current = current.left_child
            if not stack:
                return
            current = stack.pop()
            for i in range(len(current.payload)):
                cinterval = current.payload[i]
                yield cinterval.original_interval
            while current.right_child is None and stack:
                current = stack.pop()
                for i in range(len(current.payload)):
                    cinterval = current.payload[i]
                    yield cinterval.original_interval
            current = current.right_child

    def __len__(self):
        if self._root_node is None:
            return 0
        return self._root_node.subtree_stop_index

    ### PRIVATE METHODS ###

    cdef _CNode _insert_node(
        self,
        _CNode node,
        float start_offset,
        ):
        cdef _CNode child_node
        if node is None:
            return _CNode(start_offset)
        if start_offset < node.start_offset:
            child_node = self._insert_node(node.left_child, start_offset)
            self._set_node_left_child(node, child_node)
        elif node.start_offset < start_offset:
            child_node = self._insert_node(node.right_child, start_offset)
            self._set_node_right_child(node, child_node)
        return self._rebalance(node)

    cdef void _insert_interval(
        self,
        _CInterval cinterval,
        ):
        cdef _CNode node
        self._root_node = self._insert_node(
            self._root_node,
            cinterval.start_offset,
            )
        node = self._search(self._root_node, cinterval.start_offset)
        node.payload.append(cinterval)
        node.payload.sort(key=lambda x: x.stop_offset)

    @staticmethod
    def _is_interval(expr):
        if hasattr(expr, 'start_offset') and hasattr(expr, 'stop_offset'):
            return True
        return False

    cdef _CNode _rebalance(
        self,
        _CNode node,
        ):
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

    cdef object _recurse_find_intervals_intersecting_offset(
        self,
        _CNode node,
        float offset,
        ):
        cdef _CInterval cinterval
        result = []
        if node is None:
            return result
        if node.start_offset <= offset < node.stop_offset_high:
            subresult = self._recurse_find_intervals_intersecting_offset(
                node.left_child, offset)
            result.extend(subresult)
            for i in range(len(node.payload)):
                cinterval = node.payload[i]
                if offset < cinterval.stop_offset:
                    result.append(cinterval)
            subresult = self._recurse_find_intervals_intersecting_offset(
                node.right_child, offset)
            result.extend(subresult)
        elif offset <= node.start_offset:
            subresult = self._recurse_find_intervals_intersecting_offset(
                node.left_child, offset)
            result.extend(subresult)
        return result

    cdef object _recurse_find_intervals_intersecting_interval(
        self,
        _CNode node,
        _CInterval cinterval,
        ):
        cdef _CInterval candidate_interval, node_interval
        result = []
        if node is None:
            return result
        node_interval = _CInterval(
            node.start_offset,
            node.stop_offset_high,
            node,
            )
        if cinterval.intersects_interval(node_interval):
            subresult = self._recurse_find_intervals_intersecting_interval(
                node.left_child, cinterval)
            result.extend(subresult)
            for i in range(len(node.payload)):
                candidate_interval = node.payload[i]
                if candidate_interval.intersects_interval(cinterval):
                    result.append(candidate_interval)
            subresult = self._recurse_find_intervals_intersecting_interval(
                node.right_child, cinterval)
            result.extend(subresult)
        elif (cinterval.start_offset <= node.start_offset) or \
            (cinterval.stop_offset <= node.start_offset):
            subresult = self._recurse_find_intervals_intersecting_interval(
                node.left_child, cinterval)
            result.extend(subresult)
        return result

    cdef object _recurse_find_intervals_stopping_at(
        self,
        _CNode node,
        float offset,
        ):
        cdef _CInterval cinterval
        result = []
        if node is None:
            return result
        if node.stop_offset_low <= offset <= node.stop_offset_high:
            for i in range(len(node.payload)):
                cinterval = node.payload[i]
                if cinterval.stop_offset == offset:
                    result.append(cinterval)
            if node.left_child is not None:
                result.extend(self._recurse_find_intervals_stopping_at(
                    node.left_child, offset))
            if node.right_child is not None:
                result.extend(self._recurse_find_intervals_stopping_at(
                    node.right_child, offset))
        return result

    cdef float _recurse_get_offset_after(
        self,
        _CNode node,
        float offset,
        int depth=1,
    ):
        if node is None:
            # print(("    " * depth) + "None")
            return offset
        result = offset
        # print(("    " * depth) + "Node: {} {} {}".format(node.start_offset, node.stop_offset_low, node.stop_offset_high))
        if node.start_offset > offset:
            # print(("    " * depth) + "After")
            result = node.start_offset
            if offset < node.stop_offset_low < result:
                result = node.stop_offset_low
            # print(("    " * depth) + "Checking Left")
            candidate = self._recurse_get_offset_after(node.left_child, offset, depth + 1)
            if offset != result:
                if offset < candidate < result:
                    result = candidate
            elif offset < candidate:
                result = candidate
        elif node.start_offset <= offset and (
            node.stop_offset_high > offset or node.stop_offset_high > offset
        ):
            # print(("    " * depth) + "Before or Equal")
            for interval in node.payload:
                if interval.stop_offset > offset:
                    result = interval.stop_offset
                    # print(("    " * depth) + "Found: {}".format(result))
                    break
            # print(("    " * depth) + "Checking Right")
            candidate = self._recurse_get_offset_after(node.right_child, offset, depth + 1)
            if offset != result:
                if offset < candidate < result:
                    result = candidate
            elif offset < candidate:
                result = candidate
            # print(("    " * depth) + "Checking Left")
            candidate = self._recurse_get_offset_after(node.left_child, offset, depth + 1)
            if offset != result:
                if offset < candidate < result:
                    result = candidate
            elif offset < candidate:
                result = candidate
        else:
            # print(("    " * depth) + "Nope")
            pass
        # print(("    " * depth) + "Result: {}".format(result))
        return result

    cdef _CNode _recurse_get_start_offset_after(
        self,
        _CNode node,
        float offset,
    ):
        result = None
        if node is None:
            return result
        if node.start_offset <= offset and node.right_child:
            result = self._recurse_get_start_offset_after(
                node.right_child, offset)
        elif offset < node.start_offset:
            result = self._recurse_get_start_offset_after(
                node.left_child, offset) or node
        return result

    cdef _CNode _recurse_get_start_offset_before(
        self,
        _CNode node,
        float offset,
    ):
        result = None
        if node is None:
            return result
        if node.start_offset < offset:
            result = self._recurse_get_start_offset_before(
                node.right_child, offset) or node
        elif offset <= node.start_offset and node.left_child:
            result = self._recurse_get_start_offset_before(
                node.left_child, offset)
        return result

    cdef _CInterval _recurse_getitem_by_index(
        self,
        _CNode node, 
        int index,
        ):
        if node.node_start_index <= index < node.node_stop_index:
            return node.payload[index - node.node_start_index]
        elif node.left_child and index < node.node_start_index:
            return self._recurse_getitem_by_index(node.left_child, index)
        elif node.right_child and node.node_stop_index <= index:
            return self._recurse_getitem_by_index(node.right_child, index)

    cdef object _recurse_getitem_by_slice(
        self,
        _CNode node,
        int start,
        int stop,
        ):
        cdef int node_start, node_stop
        result = []
        if node is None:
            return result
        if start < node.node_start_index and node.left_child:
            result.extend(self._recurse_getitem_by_slice(
                node.left_child, start, stop))
        if start < node.node_stop_index and node.node_start_index < stop:
            node_start = start - node.node_start_index
            if node_start < 0:
                node_start = 0
            node_stop = stop - node.node_start_index
            result.extend(node.payload[node_start:node_stop])
        if node.node_stop_index <= stop and node.right_child:
            result.extend(self._recurse_getitem_by_slice(
                node.right_child, start, stop))
        return result

    cdef _CNode _remove_node(
        self,
        _CNode node,
        float start_offset,
        ):
        cdef _CNode next_node, child_node
        if node is None:
            return
        if node.start_offset == start_offset:
            if node.left_child and node.right_child:
                next_node = node.right_child
                while next_node.left_child is not None:
                    next_node = next_node.left_child
                node.start_offset = next_node.start_offset
                node.payload = next_node.payload
                self._set_node_right_child(node, self._remove_node(
                    node.right_child,
                    next_node.start_offset,
                    ))
            else:
                node = node.left_child or node.right_child
        elif start_offset < node.start_offset:
            child_node = self._remove_node(node.left_child, start_offset)
            self._set_node_left_child(node, child_node)
        elif node.start_offset < start_offset:
            child_node = self._remove_node(node.right_child, start_offset)
            self._set_node_right_child(node, child_node)
        return self._rebalance(node)

    cdef void _remove_interval(
        self,
        _CInterval cinterval,
        ):
        cdef _CNode node
        node = self._search(self._root_node, cinterval.start_offset)
        if node is None:
            return
        if cinterval in node.payload:
            node.payload.remove(cinterval)
        if not node.payload:
            self._root_node = self._remove_node(
                self._root_node,
                cinterval.start_offset,
                )

    cdef _CNode _rotate_left_left(
        self,
        _CNode node
        ):
        next_node = node.left_child
        self._set_node_left_child(node, next_node.right_child)
        self._set_node_right_child(next_node, node)
        return next_node

    cdef _CNode _rotate_left_right(
        self,
        _CNode node,
        ):
        self._set_node_left_child(
            node, self._rotate_right_right(node.left_child))
        next_node = self._rotate_left_left(node)
        return next_node

    cdef _CNode _rotate_right_left(
        self,
        _CNode node,
        ):
        self._set_node_right_child(
            node, self._rotate_left_left(node.right_child))
        next_node = self._rotate_right_right(node)
        return next_node

    cdef _CNode _rotate_right_right(
        self,
        _CNode node,
        ):
        next_node = node.right_child
        self._set_node_right_child(node, next_node.left_child)
        self._set_node_left_child(next_node, node)
        return next_node

    cdef _CNode _search(
        self,
        _CNode node,
        float start_offset,
        ):
        if node is None:
            return None
        if node.start_offset == start_offset:
            return node
        elif (
            node.left_child is not None and 
            start_offset < node.start_offset
            ):
            return self._search(node.left_child, start_offset)
        elif (
            node.right_child is not None and 
            node.start_offset < start_offset
            ):
            return self._search(node.right_child, start_offset)
        return None

    cdef void _set_node_left_child(
        self,
        _CNode node,
        _CNode left_child,
        ):
        node.left_child = left_child
        self._update_node_height(node)

    cdef void _set_node_right_child(
        self,
        _CNode node,
        _CNode right_child,
        ):
        node.right_child = right_child
        self._update_node_height(node)

    cdef object _unbox_cintervals(
        self,
        cintervals,
        ):
        cdef _CInterval cinterval
        cintervals.sort(key=lambda x: (x.start_offset, x.stop_offset))
        return [cinterval.original_interval for cinterval in cintervals]

    cdef void _update_node_height(
        self,
        _CNode node,
        ):
        cdef int left_height, right_height
        left_height = -1
        right_height = -1
        if node.left_child is not None:
            left_height = node.left_child.height
        if node.right_child is not None:
            right_height = node.right_child.height
        node.height = max(left_height, right_height) + 1
        node.balance = right_height - left_height

    cdef void _update_indices(
        self,
        _CNode node,
        int parent_stop_index,
        ):
        if node is None:
            return
        if node.left_child is not None:
            self._update_indices(
                node.left_child,
                parent_stop_index,
                )
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
            self._update_indices(
                node.right_child,
                node.node_stop_index,
                )
            node.subtree_stop_index = node.right_child.subtree_stop_index

    cdef _CNode _update_offsets(
        self, 
        _CNode node,
        ):
        cdef _CNode child_node
        cdef _CInterval cinterval
        cdef float stop_offset_low, stop_offset_hight
        if node is None:
            return
        stop_offset_low = float('inf')
        stop_offset_high = float('-inf')
        for i in range(len(node.payload)):
            cinterval = node.payload[i]
            if cinterval.stop_offset < stop_offset_low:
                stop_offset_low = cinterval.stop_offset
            if cinterval.stop_offset > stop_offset_high:
                stop_offset_high = cinterval.stop_offset
        if node.left_child is not None:
            child_node = self._update_offsets(
                node.left_child,
                )
            if child_node.stop_offset_low < stop_offset_low:
                stop_offset_low = child_node.stop_offset_low
            if stop_offset_high < child_node.stop_offset_high:
                stop_offset_high = child_node.stop_offset_high
        if node.right_child is not None:
            child_node = self._update_offsets(
                node.right_child,
                )
            if child_node.stop_offset_low < stop_offset_low:
                stop_offset_low = child_node.stop_offset_low
            if stop_offset_high < child_node.stop_offset_high:
                stop_offset_high = child_node.stop_offset_high
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

    def find_intervals_starting_at(self, offset):
        results = []
        node = self._search(self._root_node, offset)
        if node is None:
            return results
        return self._unbox_cintervals(node.payload)

    def find_intervals_stopping_at(self, offset):
        cintervals = self._recurse_find_intervals_stopping_at(
            self._root_node, offset)
        return self._unbox_cintervals(cintervals)

    def find_intervals_intersecting_offset(self, offset):
        offset = float(offset)
        cintervals = self._recurse_find_intervals_intersecting_offset(
            self._root_node, offset)
        return self._unbox_cintervals(cintervals)

    def find_intervals_intersecting_interval(self, interval):
        cinterval = _CInterval.from_interval(interval)
        assert isinstance(cinterval, _CInterval)
        cintervals = self._recurse_find_intervals_intersecting_interval(
            self._root_node, cinterval)
        return self._unbox_cintervals(cintervals)

    def get_offset_after(self, offset):
        # print("Searching for: {}".format(offset))
        result = None
        if self._root_node is not None:
            result = self._recurse_get_offset_after(self._root_node, offset)
            if result == offset:
                result = None
        return result

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
        assert self._is_interval(interval)
        cinterval = _CInterval.from_interval(interval)
        node = self._search(self._root_node, cinterval.start_offset)
        if node is None:
            raise ValueError('{} not in interval tree.'.format(interval))
        if cinterval not in node.payload:
            raise ValueError('{} not in interval tree.'.format(interval))
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
