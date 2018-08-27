from supriya.ugens.InfoUGenBase import InfoUGenBase


class BufInfoUGenBase(InfoUGenBase):
    """
    Abstract base class for buffer information ugens.

    Buffer information ugens expose both scalar-rate and control-rate
    constructors, as buffer topology may change after a synth is instantiated.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Buffer UGens'
