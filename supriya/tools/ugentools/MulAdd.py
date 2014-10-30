# -*- encoding: utf-8 -*-
from supriya.tools.synthdeftools.UGen import UGen


class MulAdd(UGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Basic Operator UGens'

    __slots__ = ()

    _ordered_input_names = (
        'source',
        'multiplier',
        'addend',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        addend=0.0,
        multiplier=1.0,
        rate=None,
        source=None,
        ):
        UGen.__init__(
            self,
            addend=addend,
            multiplier=multiplier,
            rate=rate,
            source=source,
            )

    ### PRIVATE METHODS ###

    @staticmethod
    def _inputs_are_valid(
        source,
        multiplier,
        addend,
        ):
        from supriya.tools import synthdeftools
        Rate = synthdeftools.Rate
        if source.rate == Rate.AUDIO:
            return True
        if source.rate == Rate.CONTROL:
            if multiplier.rate in (Rate.CONTROL, Rate.SCALAR):
                if addend.rate in (Rate.CONTROL, Rate.SCALAR):
                    return True
        return False

    @classmethod
    def _new_single(
        cls,
        addend=None,
        multiplier=None,
        rate=None,
        source=None,
        ):
        from supriya.tools import synthdeftools
        if multiplier == 0.0:
            return addend
        minus = multiplier == -1
        no_multiplier = multiplier == 1
        no_addend = addend == 0
        if no_multiplier and no_addend:
            return source
        if minus and no_addend:
            return synthdeftools.Op.negative(source)
        if no_addend:
            return source * multiplier
        if minus:
            return addend - source
        if no_multiplier:
            return source + addend
        if cls._inputs_are_valid(source, multiplier, addend):
            return cls(
                addend=addend,
                multiplier=multiplier,
                rate=rate,
                source=source,
                )
        if cls._inputs_are_valid(multiplier, source, addend):
            return cls(
                addend=addend,
                multiplier=source,
                rate=rate,
                source=multiplier,
                )
        return (source * multiplier) + addend

    ### PUBLIC METHODS ###

    @classmethod
    def new(
        cls,
        source=None,
        multiplier=1.0,
        addend=0.0,
        ):
        from supriya.tools import synthdeftools
        rate = synthdeftools.Rate.from_input((source, multiplier, addend))
        ugen = cls._new_expanded(
            addend=addend,
            multiplier=multiplier,
            rate=rate,
            source=source,
            )
        return ugen