import supriya.osc
from supriya.system.SupriyaValueObject import SupriyaValueObject


class RequestBundle(SupriyaValueObject):
    """
    A Request bundle.

    ::

        >>> request_one = supriya.commands.BufferAllocateRequest(
        ...     buffer_id=23,
        ...     frame_count=512,
        ...     channel_count=1,
        ...     )
        >>> request_two = supriya.commands.BufferAllocateRequest(
        ...     buffer_id=24,
        ...     frame_count=512,
        ...     channel_count=1,
        ...     )
        >>> request_bundle = supriya.commands.RequestBundle(
        ...     timestamp=10.5,
        ...     contents=[request_one, request_two],
        ...     )

    ::

        >>> request_bundle.to_osc_bundle(True)
        OscBundle(
            contents=(
                OscMessage('/b_alloc', 23, 512, 1),
                OscMessage('/b_alloc', 24, 512, 1),
                ),
            timestamp=10.5,
            )

    ::

        >>> request_bundle.to_list(True)
        [10.5, [['/b_alloc', 23, 512, 1], ['/b_alloc', 24, 512, 1]]]

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_contents',
        '_timestamp',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        timestamp=None,
        contents=None,
    ):
        import supriya.commands
        self._timestamp = timestamp
        if contents is not None:
            prototype = (supriya.commands.Request, type(self))
            assert all(isinstance(x, prototype) for x in contents)
            contents = tuple(contents)
        else:
            contents = ()
        self._contents = contents

    ### PUBLIC METHODS ###

    def communicate(self, server=None):
        import supriya.realtime
        server = server or supriya.realtime.Server.get_default_server()
        assert isinstance(server, supriya.realtime.Server)
        assert server.is_running
        message = self.to_osc_bundle()
        server.send_message(message)

    def to_datagram(self):
        return self.to_osc_message().to_datagram()

    def to_list(self, with_textual_osc_command=False):
        return self.to_osc_bundle(with_textual_osc_command).to_list()

    def to_osc_bundle(self, with_textual_osc_command=False):
        contents = []
        for x in self.contents:
            if isinstance(x, type(self)):
                contents.append(x.to_osc_bundle(with_textual_osc_command))
            else:
                contents.append(x.to_osc_message(with_textual_osc_command))
        bundle = supriya.osc.OscBundle(
            timestamp=self.timestamp,
            contents=contents,
            )
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def contents(self):
        return self._contents

    @property
    def timestamp(self):
        return self._timestamp
