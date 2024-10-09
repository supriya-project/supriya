from .components import Component


class Connection(Component):
    pass


class Receive(Connection):
    pass


class Direct(Component):
    pass


class DirectIn(Direct):
    pass


class DirectOut(Direct):
    pass


class Send(Connection):

    async def delete(self):
        pass
