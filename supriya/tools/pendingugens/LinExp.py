# -*- encoding: utf-8 -*-
from supriya.tools.ugentools.PureUGen import PureUGen


class LinExp(PureUGen):

    ### CLASS VARIABLES ###

    __documentation_section__ = None

    __slots__ = ()

    _ordered_input_names = (
        )

    _valid_calculation_rates = None

    ### INITIALIZER ###

    def __init__(
        self,
        calculation_rate=None,
        dsthi=2,
        dstlo=1,
        source=0,
        srchi=1,
        srclo=0,
        ):
        PureUGen.__init__(
            self,
            calculation_rate=calculation_rate,
            dsthi=dsthi,
            dstlo=dstlo,
            source=source,
            srchi=srchi,
            srclo=srclo,
            )

    ### PUBLIC METHODS ###

    @classmethod
    def ar(
        cls,
        dsthi=2,
        dstlo=1,
        source=0,
        srchi=1,
        srclo=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            dsthi=dsthi,
            dstlo=dstlo,
            source=source,
            srchi=srchi,
            srclo=srclo,
            )
        return ugen

    @classmethod
    def kr(
        cls,
        dsthi=2,
        dstlo=1,
        source=0,
        srchi=1,
        srclo=0,
        ):
        from supriya.tools import synthdeftools
        calculation_rate = None
        ugen = cls._new_expanded(
            calculation_rate=calculation_rate,
            dsthi=dsthi,
            dstlo=dstlo,
            source=source,
            srchi=srchi,
            srclo=srclo,
            )
        return ugen
