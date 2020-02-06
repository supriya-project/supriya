from supriya.system import SupriyaValueObject


class Response(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = ("_osc_message",)

    _address = None

    ### INITIALIZER ###

    def __init__(self, osc_message=None):
        self._osc_message = osc_message

    ### PRIVATE METHODS ###

    @staticmethod
    def _group_items(items, length):
        iterators = [iter(items)] * length
        iterator = zip(*iterators)
        return iterator

    ### PUBLIC METHODS ###

    @classmethod
    def from_osc_message(cls, message):
        import supriya.commands

        return {
            "/b_info": supriya.commands.BufferInfoResponse,
            "/b_set": supriya.commands.BufferSetResponse,
            "/b_setn": supriya.commands.BufferSetContiguousResponse,
            "/c_set": supriya.commands.ControlBusSetResponse,
            "/c_setn": supriya.commands.ControlBusSetContiguousResponse,
            "/d_removed": supriya.commands.SynthDefRemovedResponse,
            "/done": supriya.commands.DoneResponse,
            "/fail": supriya.commands.FailResponse,
            "/g_queryTree.reply": supriya.commands.QueryTreeResponse,
            "/n_end": supriya.commands.NodeInfoResponse,
            "/n_go": supriya.commands.NodeInfoResponse,
            "/n_info": supriya.commands.NodeInfoResponse,
            "/n_move": supriya.commands.NodeInfoResponse,
            "/n_off": supriya.commands.NodeInfoResponse,
            "/n_on": supriya.commands.NodeInfoResponse,
            "/n_set": supriya.commands.NodeSetResponse,
            "/n_setn": supriya.commands.NodeSetContiguousResponse,
            "/status.reply": supriya.commands.StatusResponse,
            "/synced": supriya.commands.SyncedResponse,
            "/tr": supriya.commands.TriggerResponse,
        }[message.address].from_osc_message(message)

    def to_dict(self):
        result = {}
        for key, value in self.__getstate__().items():
            key = key[1:]
            if key == "osc_message":
                continue
            result[key] = value
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def osc_message(self):
        return self._osc_message
