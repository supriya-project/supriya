from supriya.system import SupriyaObject


class Moment(SupriyaObject):
    """
    A moment of intervals in a interval tree.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_interval_tree",
        "_overlap_intervals",
        "_start_intervals",
        "_start_offset",
        "_stop_intervals",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        interval_tree=None,
        overlap_intervals=None,
        start_intervals=None,
        start_offset=None,
        stop_intervals=None,
    ):
        self._interval_tree = interval_tree
        self._start_offset = start_offset
        self._start_intervals = start_intervals
        self._stop_intervals = stop_intervals
        self._overlap_intervals = overlap_intervals

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets the repr of this moment.
        """
        return "<{}({} <<{}>>)>".format(
            type(self).__name__,
            str(self.start_offset),
            len(self.start_intervals) + len(self.overlap_intervals),
        )

    ### PUBLIC PROPERTIES ###

    @property
    def next_moment(self):
        """
        Gets the next moment in this moment's interval
        collection.
        """
        # TODO: This doesn't take into account stop offsets
        tree = self._interval_tree
        if tree is None:
            return None
        start_offset = tree.get_start_offset_after(self.start_offset)
        if start_offset is None:
            return None
        return tree.get_moment_at(start_offset)

    @property
    def next_start_offset(self):
        """
        Gets the next moment start offset in this moment's
        interval tree.
        """
        tree = self._interval_tree
        if tree is None:
            return None
        start_offset = tree.get_start_offset_after(self.start_offset)
        return start_offset

    @property
    def overlap_intervals(self):
        """
        Gets the intervals in this moment which overlap this
        moment's start offset.
        """
        return self._overlap_intervals

    @property
    def previous_moment(self):
        """
        Gets the previous moment in this moment's interval
        collection.
        """
        # TODO: This doesn't take into account stop offsets
        tree = self._interval_tree
        if tree is None:
            return None
        start_offset = tree.get_start_offset_before(self.start_offset)
        if start_offset is None:
            return None
        return tree.get_moment_at(start_offset)

    @property
    def previous_start_offset(self):
        """
        Gets the previous moment start offset in this moment's
        interval tree.
        """
        tree = self._interval_tree
        if tree is None:
            return None
        start_offset = tree.get_start_offset_before(self.start_offset)
        return start_offset

    @property
    def start_offset(self):
        """
        Gets this moment's start offset.
        """
        return self._start_offset

    @property
    def start_intervals(self):
        """
        Gets the intervals in this moment which start at this
        moment's start offset.
        """
        return self._start_intervals

    @property
    def stop_intervals(self):
        """
        Gets the intervals in this moment which stop at this
        moment's start offset.
        """
        return self._stop_intervals

    @property
    def interval_tree(self):
        """
        Gets this moment's interval tree.
        """
        return self._interval_tree
