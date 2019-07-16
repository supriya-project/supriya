from .Interval import Interval


class _CInterval:

    __slots__ = ("start_offset", "stop_offset", "original_interval")

    def __init__(self, start_offset, stop_offset, original_interval):
        self.start_offset = float(start_offset)
        self.stop_offset = float(stop_offset)
        self.original_interval = original_interval

    def __eq__(self, cinterval):
        assert isinstance(cinterval, type(self)), cinterval
        if self.start_offset != cinterval.start_offset:
            return False
        if self.stop_offset != cinterval.stop_offset:
            return False
        if self.original_interval != cinterval.original_interval:
            return False
        return True

    def __ne__(self, cinterval):
        assert isinstance(cinterval, type(self)), cinterval
        return not self.__eq__(cinterval)

    def __lt__(self, cinterval):
        assert isinstance(cinterval, type(self)), cinterval
        if self.start_offset < cinterval.start_offset:
            return True
        if self.start_offset > cinterval.start_offset:
            return False
        if self.stop_offset < cinterval.stop_offset:
            return True
        return False

    def __repr__(self):
        return "<_CInterval {}:{}>".format(self.start_offset, self.stop_offset)

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

    __slots__ = (
        "balance",
        "height",
        "left_child",
        "node_start_index",
        "node_stop_index",
        "payload",
        "right_child",
        "start_offset",
        "stop_offset_high",
        "stop_offset_low",
        "subtree_start_index",
        "subtree_stop_index",
    )

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

    ### CLASS VARIABLES ###

    __slots__ = ("_root_node",)

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
        assert isinstance(cinterval, _CInterval)
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
        assert self._is_interval(interval)
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
