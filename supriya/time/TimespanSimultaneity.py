from supriya.system.SupriyaObject import SupriyaObject


class TimespanSimultaneity(SupriyaObject):
    """
    A simultaneity of timespans in a interval tree.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_interval_tree",
        "_overlap_timespans",
        "_start_timespans",
        "_start_offset",
        "_stop_timespans",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        interval_tree=None,
        overlap_timespans=None,
        start_timespans=None,
        start_offset=None,
        stop_timespans=None,
    ):
        self._interval_tree = interval_tree
        self._start_offset = start_offset
        self._start_timespans = start_timespans
        self._stop_timespans = stop_timespans
        self._overlap_timespans = overlap_timespans

    ### SPECIAL METHODS ###

    def __repr__(self):
        """
        Gets the repr of this simultaneity.
        """
        return "<{}({} <<{}>>)>".format(
            type(self).__name__,
            str(self.start_offset),
            len(self.start_timespans) + len(self.overlap_timespans),
        )

    ### PUBLIC PROPERTIES ###

    @property
    def next_simultaneity(self):
        """
        Gets the next simultaneity in this simultaneity's timespan
        collection.
        """
        # TODO: This doesn't take into account stop offsets
        tree = self._interval_tree
        if tree is None:
            return None
        start_offset = tree.get_start_offset_after(self.start_offset)
        if start_offset is None:
            return None
        return tree.get_simultaneity_at(start_offset)

    @property
    def next_start_offset(self):
        """
        Gets the next simultaneity start offset in this simultaneity's
        interval tree.
        """
        tree = self._interval_tree
        if tree is None:
            return None
        start_offset = tree.get_start_offset_after(self.start_offset)
        return start_offset

    @property
    def overlap_timespans(self):
        """
        Gets the timespans in this simultaneity which overlap this
        simultaneity's start offset.
        """
        return self._overlap_timespans

    @property
    def previous_simultaneity(self):
        """
        Gets the previous simultaneity in this simultaneity's timespan
        collection.
        """
        # TODO: This doesn't take into account stop offsets
        tree = self._interval_tree
        if tree is None:
            return None
        start_offset = tree.get_start_offset_before(self.start_offset)
        if start_offset is None:
            return None
        return tree.get_simultaneity_at(start_offset)

    @property
    def previous_start_offset(self):
        """
        Gets the previous simultaneity start offset in this simultaneity's
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
        Gets this simultaneity's start offset.
        """
        return self._start_offset

    @property
    def start_timespans(self):
        """
        Gets the timespans in this simultaneity which start at this
        simultaneity's start offset.
        """
        return self._start_timespans

    @property
    def stop_timespans(self):
        """
        Gets the timespans in this simultaneity which stop at this
        simultaneity's start offset.
        """
        return self._stop_timespans

    @property
    def interval_tree(self):
        """
        Gets this simultaneity's interval tree.
        """
        return self._interval_tree
