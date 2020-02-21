from supriya.commands.Response import Response


class TriggerResponse(Response):

    ### INITIALIZER ###

    def __init__(self, node_id=None, trigger_id=None, trigger_value=None):
        self._node_id = node_id
        self._trigger_id = trigger_id
        self._trigger_value = trigger_value

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, osc_message):
        arguments = osc_message.contents
        response = cls(*arguments)
        return response

    ### PUBLIC PROPERTIES ###

    @property
    def node_id(self):
        return self._node_id

    @property
    def trigger_id(self):
        return self._trigger_id

    @property
    def trigger_value(self):
        return self._trigger_value
