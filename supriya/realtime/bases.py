import abc

from supriya.system import SupriyaObject


class ServerObject(SupriyaObject):
    """
    A proxy of an object on a server.

    Server objects can be allocated and freed.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_server",)

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        self._server = None

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def allocate(self, server):
        import supriya.realtime

        if self.is_allocated and self.server is server:
            return
        assert self.server is None, (self, self.server)
        assert isinstance(server, supriya.realtime.Server)
        assert server.is_running
        self._server = server

    @abc.abstractmethod
    def free(self):
        self._server = None

    ### PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def is_allocated(self):
        raise NotImplementedError

    @property
    def server(self):
        return self._server
