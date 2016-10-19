# -*- encoding: utf-8 -*-
from supriya.tools import osctools
from supriya.tools.requesttools.Request import Request


class NodeRunRequest(Request):
    r"""
    A /n_run request.

    ::

        >>> from supriya.tools import requesttools
        >>> request = requesttools.NodeRunRequest(
        ...     node_id_run_flag_pairs=(
        ...         (1000, True),
        ...         (1001, False),
        ...         ),
        ...     )
        >>> request
        NodeRunRequest(
            node_id_run_flag_pairs=(
                (1000, True),
                (1001, False),
                )
            )

    ::

        >>> message = request.to_osc_message()
        >>> message
        OscMessage(12, 1000, 1, 1001, 0)

    ::

        >>> message.address == requesttools.RequestId.NODE_RUN
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_node_id_run_flag_pairs',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        node_id_run_flag_pairs=None,
        ):
        Request.__init__(self)
        if node_id_run_flag_pairs:
            pairs = []
            for node_id, run_flag in node_id_run_flag_pairs:
                node_id = int(node_id)
                run_flag = bool(run_flag)
                pairs.append((node_id, run_flag))
            node_id_run_flag_pairs = tuple(pairs)
        self._node_id_run_flag_pairs = node_id_run_flag_pairs

    ### PUBLIC METHODS ###

    def to_osc_message(self, with_textual_osc_command=False):
        if with_textual_osc_command:
            request_id = self.request_command
        else:
            request_id = int(self.request_id)
        contents = [request_id]
        if self.node_id_run_flag_pairs:
            for node_id, run_flag in self.node_id_run_flag_pairs:
                contents.append(node_id)
                contents.append(int(run_flag))
        message = osctools.OscMessage(*contents)
        return message

    ### PUBLIC PROPERTIES ###

    @property
    def node_id_run_flag_pairs(self):
        return self._node_id_run_flag_pairs

    @property
    def response_specification(self):
        return None

    @property
    def request_id(self):
        from supriya.tools import requesttools
        return requesttools.RequestId.NODE_RUN
