# -*- encoding: utf-8 -*-
import abc
import collections
from supriya.tools import osctools
from supriya.tools.systemtools.SupriyaValueObject import SupriyaValueObject


class Request(SupriyaValueObject):

    ### CLASS VARIABLES ###

    __slots__ = ()

    _prototype = None

    ### INITIALIZER ###

    def __init__(
        self,
        ):
        pass

    ### PRIVATE METHODS ###

    def _coerce_completion_message_input(self, message):
        if message is None:
            return message
        elif isinstance(message, (osctools.OscMessage, osctools.OscBundle)):
            return message
        elif isinstance(message, Request):
            return message.to_osc_message()
        elif isinstance(message, collections.Sequence):
            return osctools.OscMessage(*message)
        raise ValueError(message)

    def _coerce_completion_message_output(self, contents):
        if self.completion_message is not None:
            completion_message = self.completion_message.to_datagram()
            completion_message = bytearray(completion_message)
            contents.append(completion_message)
    

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def to_osc_message(self):
        raise NotImplementedError