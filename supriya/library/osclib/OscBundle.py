class OscBundle(object):

    ### CLASS VARIABLES ###

    __slots__ = (
        '_timestamp',
        '_contents',
        )

    _bundle_prefix = b'#bundle\x00'

    ### INITIALIZER ###

    def __init__(
        self,
        timestamp=None,
        contents=None,
        ):
        from supriya.library import osclib
        self._timestamp = timestamp
        if contents is not None:
            prototype = (osclib.OscMessage, osclib.OscBundle)
            assert all(isinstance(x, prototype) for x in contents)
            contents = tuple(contents)
        else:
            contents = ()
        self._contents = contents

    ### PUBLIC METHODS ###

    @staticmethod
    def datagram_is_bundle(datagram):
        return datagram.startswith(OscBundle._bundle_prefix)

    @staticmethod
    def from_datagram(datagram):
        assert OscBundle.datagram_is_bundle(datagram)
        
    def to_datagram(self):
        pass

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        return self._contents

    @property
    def timestamp(self):
        return self._timestamp
