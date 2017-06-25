from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class EventProduct(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = (
        'event',
        'index',
        'is_stop',
        'uuid',
        'requests',
        'timestamp',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        event=None,
        index=0,
        is_stop=False,
        requests=None,
        timestamp=0,
        uuid=None,
        ):
        self.event = event
        self.index = index
        self.is_stop = is_stop
        self.uuid = uuid
        self.requests = requests
        self.timestamp = timestamp

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) != type(expr):
            return False
        if self._get_sort_bundle() != expr._get_sort_bundle():
            return False
        return (
            self.event == expr.event and
            self.uuid == expr.uuid and
            self.requests == expr.requests
            )

    def __lt__(self, expr):
        if type(self) != type(expr):
            raise TypeError()
        return self._get_sort_bundle() < expr._get_sort_bundle()

    ### PRIVATE METHODS ###

    def _get_sort_bundle(self):
        return (
            self.timestamp,
            self.index,
            self.is_stop,
            )
