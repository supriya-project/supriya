import abc
import collections
import enum


class UGen(object):
    r'''A UGen.
    '''

    ### CLASS VARIABLES ###

    class Rate(enum.IntEnum):
        AUDIO_RATE = 2
        CONTROL_RATE = 1
        SCALAR_RATE = 0

    _special_index = 0

    __slots__ = ()

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        raise NotImplementedError

    ### PRIVATE METHODS ###

    @staticmethod
    def _compute_binary_rate(ugen_specification_a, ugen_specification_b):
        if ugen_specification_a.calculation_rate == UGen.Rate.AUDIO_RATE:
            return UGen.RATE.AUDIO_RATE
        if hasattr(ugen_specification_b, 'calculation_rate') and \
            ugen_specification_b.calculation_rate == UGen.RAte.AUDIO_RATE:
            return UGen.Rate.AUDIO_RATE
        if ugen_specification_a.calculation_rate == UGen.Rate.CONTROL_RATE:
            return UGen.Rate.CONTROL_RATE
        if hasattr(ugen_specification_b, 'calculation_rate') and \
            ugen_specification_b.calculation_rate == UGen.Rate.CONTROL_RATE:
            return UGen.Rate.CONTROL_RATE
        return UGen.Rate.SCALAR_RATE

    @staticmethod
    def _expand_multichannel(arguments):
        r'''Expands ugens into multichannel arrays.

        ::

            >>> import supriya
            >>> arguments = (0, [1, 2], [3, 4, 5])
            >>> supriya.synthdefs.UGen._expand_multichannel(arguments)
            [[0, 1, 3], [0, 2, 4], [0, 1, 5]]

        '''
        maximum_length = 1
        for argument in arguments:
            if isinstance(argument, collections.Sequence):
                maximum_length = max(maximum_length, len(argument))
        result = []
        for i in range(maximum_length):
            result.append([])
            for argument in arguments:
                if isinstance(argument, collections.Sequence):
                    result[i].append(argument[i % len(argument)])
                else:
                    result[i].append(argument)
        return result

    @classmethod
    def _new(cls, calculation_rate, special_index, **kwargs):
        assert isinstance(calculation_rate, UGen.Rate)
        pass

    ### PUBLIC METHODS ###

    @classmethod
    def ar(cls, **kwargs):
        ugen_specification = cls._new(
            UGen.Rate.AUDIO_RATE,
            cls.special_index,
            **kwargs
            )
        return ugen_specification

    @classmethod
    def kr(cls, **kwargs):
        ugen_specification = cls._new(
            UGen.Rate.CONTROL_RATE,
            cls.special_index,
            **kwargs
            )
        return ugen_specification
