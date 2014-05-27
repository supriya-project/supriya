# -*- encoding: utf-8 -*-


class TimespanSimultaneity(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_timespan_collection',
        '_overlap_timespans',
        '_start_timespans',
        '_start_offset',
        '_stop_timespans',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        timespan_collection=None,
        overlap_timespans=None,
        start_timespans=None,
        start_offset=None,
        stop_timespans=None,
        ):
        from supriya.library import controllib
        prototype = (controllib.TimespanCollection, type(None))
        assert isinstance(timespan_collection, prototype)
        self._timespan_collection = timespan_collection
        self._start_offset = start_offset
        assert isinstance(start_timespans, tuple)
        assert isinstance(stop_timespans, (tuple, type(None)))
        assert isinstance(overlap_timespans, (tuple, type(None)))
        self._start_timespans = start_timespans
        self._stop_timespans = stop_timespans
        self._overlap_timespans = overlap_timespans

    ### SPECIAL METHODS ###

    def __repr__(self):
        return '<{} {} {{{}}}>'.format(
            type(self).__name__,
            self.start_offset,
            len(self.timespans),
            )
    
    ### PUBLIC PROPERTIES ###

    @property
    def next_start_offset(self):
        tree = self._timespan_collection
        if tree is None:
            return None
        start_offset = tree.get_start_offset_after(self.start_offset)
        return start_offset

    @property
    def nextSimultaneity(self):
        tree = self._timespan_collection
        if tree is None:
            return None
        start_offset = tree.get_start_offset_after(self.start_offset)
        if start_offset is None:
            return None
        return tree.get_simultaneity_at(start_offset)

    @property
    def overlap_timespans(self):
        return self._overlap_timespans

    @property
    def previousSimultaneity(self):
        tree = self._timespan_collection
        if tree is None:
            return None
        start_offset = tree.get_start_offset_before(self.start_offset)
        if start_offset is None:
            return None
        return tree.get_simultaneity_at(start_offset)

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def start_timespans(self):
        return self._start_timespans

    @property
    def stop_timespans(self):
        return self._stop_timespans

    @property
    def timespan_collection(self):
        return self._timespan_collection

